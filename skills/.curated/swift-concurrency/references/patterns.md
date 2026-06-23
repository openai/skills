# Swift Concurrency Patterns

Use these templates as starting points and adapt names, error types, and logging.

## Timeout Wrapper

Proposal anchors: `SE-0304`, `SE-0329`, `SE-0374`

```swift
enum TimeoutError: Error { case timedOut }

func withTimeout<T>(
    _ nanoseconds: UInt64,
    operation: @Sendable @escaping () async throws -> T
) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask { try await operation() }
        group.addTask {
            try await Task.sleep(nanoseconds: nanoseconds)
            throw TimeoutError.timedOut
        }

        let first = try await group.next()!
        group.cancelAll()
        return first
    }
}
```

## Actor Cache With In-Flight Deduplication

Proposal anchors: `SE-0306`, `SE-0313`

```swift
actor UserCache {
    private var storage: [String: User] = [:]
    private var inFlight: [String: Task<User, Error>] = [:]

    func user(id: String, fetch: @Sendable @escaping (String) async throws -> User) async throws -> User {
        if let cached = storage[id] { return cached }
        if let task = inFlight[id] { return try await task.value }

        let task = Task { try await fetch(id) }
        inFlight[id] = task
        defer { inFlight[id] = nil }

        let result = try await task.value
        storage[id] = result
        return result
    }
}
```

## Bounded Parallel Map

Proposal anchors: `SE-0304`, `SE-0381`, `SE-0442`

```swift
func mapConcurrent<Input: Sendable, Output: Sendable>(
    _ input: [Input],
    maxConcurrent: Int,
    transform: @Sendable @escaping (Input) async throws -> Output
) async throws -> [Output] {
    precondition(maxConcurrent > 0)
    var iterator = input.makeIterator()
    var results: [Output] = []

    return try await withThrowingTaskGroup(of: Output.self) { group in
        for _ in 0..<maxConcurrent {
            guard let value = iterator.next() else { break }
            group.addTask { try await transform(value) }
        }

        while let result = try await group.next() {
            results.append(result)
            if let next = iterator.next() {
                group.addTask { try await transform(next) }
            }
        }

        return results
    }
}
```

## Callback to Async Bridge

Proposal anchors: `SE-0300`, `SE-0297`

```swift
func loadProfile(id: String) async throws -> Profile {
    try await withCheckedThrowingContinuation { continuation in
        legacyClient.loadProfile(id: id) { result in
            switch result {
            case .success(let profile):
                continuation.resume(returning: profile)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
    }
}
```

## Delegate Events to AsyncThrowingStream

Proposal anchors: `SE-0314`, `SE-0388`, `SE-0468`

```swift
final class DownloadEventsAdapter: NSObject, URLSessionDownloadDelegate {
    private var continuation: AsyncThrowingStream<Progress, Error>.Continuation?

    func stream() -> AsyncThrowingStream<Progress, Error> {
        AsyncThrowingStream { continuation in
            self.continuation = continuation
        }
    }

    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didWriteData bytesWritten: Int64,
                    totalBytesWritten: Int64, totalBytesExpectedToWrite: Int64) {
        guard totalBytesExpectedToWrite > 0 else { return }
        continuation?.yield(.init(totalBytesWritten: totalBytesWritten,
                                  totalBytesExpected: totalBytesExpectedToWrite))
    }

    func finish() {
        continuation?.finish()
    }

    func fail(_ error: Error) {
        continuation?.finish(throwing: error)
    }
}
```
