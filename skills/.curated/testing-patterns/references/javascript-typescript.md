# JavaScript And TypeScript Testing

Load this reference when the repository uses Node.js, TypeScript, React, Vite, Next.js, Jest, Vitest, React Testing Library, Playwright, or MSW.

## Default Tool Choices

- Reuse the repo's existing framework first.
- Prefer Vitest for Vite-first repos and Jest for repos already invested in Jest.
- Prefer React Testing Library for component behavior.
- Prefer MSW for network mocking when the code exercises fetch or HTTP flows.
- Prefer Playwright for browser E2E or visual tests when the repository already uses it.

## Query And Assertion Priorities

For React Testing Library, prefer:

1. `getByRole`
2. `getByLabelText`
3. `getByPlaceholderText`
4. `getByText`
5. `getByTestId` as a last resort

Assert user-visible outcomes before inspecting implementation details.

## Common Patterns

### Arrange / Act / Assert

```ts
it("applies a valid discount", () => {
  const items = [{ price: 100 }, { price: 50 }];

  const result = calculateTotal(items, 0.1);

  expect(result).toBe(135);
});
```

### Async UI Tests

```tsx
const user = userEvent.setup();
render(<DataLoader />);

await user.click(screen.getByRole("button", { name: /load/i }));

await waitFor(() => {
  expect(screen.getByText("Data loaded")).toBeInTheDocument();
});
```

### Network Mocking With MSW

```ts
export const handlers = [
  http.get("/api/users", () =>
    HttpResponse.json([
      { id: 1, name: "John" },
      { id: 2, name: "Jane" },
    ]),
  ),
];
```

## Snapshot Guidance

- Use snapshots sparingly for stable, intentionally broad rendering contracts.
- Do not snapshot giant trees when a few targeted assertions would explain the behavior better.
- Prefer explicit semantic assertions over snapshot churn.

## E2E Guidance

- Reserve E2E coverage for critical flows such as authentication, checkout, onboarding, or cross-page workflows.
- Keep E2E fixtures realistic but minimal.
- If the task is exploratory browser automation rather than repository tests, use [$playwright](/Users/Kiosk/.codex/skills/playwright/SKILL.md) instead of adding test files.
