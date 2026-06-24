---
name: docker-kubernetes-devops
description: Build, run, debug, harden, or deploy containerized applications with Docker, Docker Compose, Kubernetes, kubectl, Helm, or KIND. Use when working on Dockerfiles, Compose stacks, image builds, container logs, local clusters, manifests, services, ingress, secrets, health checks, or deployment failures.
---

# Docker and Kubernetes DevOps

Use this skill for container and Kubernetes work. Preserve the user's environment: inspect before pruning, deleting, restarting services, or changing cluster state.

## Validated Version Evidence

This guidance was checked against mined repositories using Docker Python SDK 7.1.0 and Kubernetes Python clients 33.1.0 and 35.0.0. The operational workflow depends primarily on installed Docker, Compose, kubectl, Helm, and cluster versions, so capture those before applying version-sensitive advice:

```bash
docker version
docker compose version
kubectl version --client
helm version --short
```

For Kubernetes API-client code, also record package versions:

```bash
python - <<'PY'
from importlib.metadata import PackageNotFoundError, version
for package in ["docker", "kubernetes"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "not installed")
PY
```

## What This Skill Delivers

Use this skill to make a container or Kubernetes workload build, start, and prove readiness without damaging the user's environment. A complete run produces:

- The active Docker/Kubernetes/Helm context and versions.
- The exact build/run/apply command used.
- Logs, describe output, health check, or request output proving the workload state.
- A minimal manifest/Dockerfile/Compose/Helm values change when code changes are needed.
- A final note calling out any destructive or cluster-mutating command.

## Standalone Quick Start

For Docker-only apps, prefer the smallest local proof:

```bash
docker build -t local/app-check .
docker run --rm --detach --name app-check -p 8080:8080 local/app-check
docker logs --tail=100 app-check
curl -f http://localhost:8080/health || curl -f http://localhost:8080/
docker stop app-check
```

For Compose apps:

```bash
docker compose config
docker compose up --build
docker compose ps
docker compose logs --tail=100
```

For Kubernetes apps, inspect before changing and prefer a local KIND/minikube context unless the user explicitly targets a remote cluster.

## Workflow

1. Identify the target: local Docker, Compose, local Kubernetes, or remote Kubernetes.
2. Inspect current state before acting:

```bash
docker ps
docker compose ps
kubectl config current-context
kubectl get pods -A
```

3. Read the Dockerfile, Compose files, manifests, Helm chart, and deployment docs.
4. Reproduce with the smallest local command before changing deployment configuration.
5. Validate the running service with logs, health checks, and an actual request.

For Kubernetes, treat the active context as a safety boundary. If `kubectl config current-context` points at a shared or production-like cluster, ask before applying, restarting, scaling, or deleting anything.

## Docker

- Keep image layers deterministic and cache-friendly.
- Use `.dockerignore` to avoid copying secrets, build artifacts, virtualenvs, and large data.
- Prefer non-root runtime users when the app supports it.
- Separate build-time and runtime dependencies with multi-stage builds when useful.
- Add health checks only when they reflect real readiness.
- Do not run broad cleanup commands unless the user asks or disk pressure requires it.

## Docker Compose

- Check service names, ports, volumes, environment variables, and dependency readiness.
- Use `docker compose logs --tail=100 <service>` and `docker compose exec <service> ...` for targeted debugging.
- Distinguish container start order from application readiness.
- Keep development-only services and production settings separate.

## Kubernetes

- Confirm context and namespace before applying or deleting resources.
- Use `kubectl describe` and events before changing manifests.
- For a failing pod, start with `kubectl describe pod <pod> -n <namespace>`, `kubectl logs <pod> -n <namespace> --previous` when it is restarting, and `kubectl get events -n <namespace> --sort-by=.lastTimestamp`.
- Check probes, resource requests/limits, image pull secrets, config maps, secrets, service selectors, and ingress routing.
- For local testing, KIND is appropriate when the task needs Kubernetes semantics rather than just containers.
- Prefer declarative changes to manifests or Helm values over imperative cluster drift.

## References

Open `references/workflows.md` for detailed Dockerfile, Compose, Kubernetes, Helm, rollout, networking, storage, security, and incident-debugging workflows.

Open `references/mastery.md` for container/Kubernetes mental models, safety boundaries, deployment failure diagnosis, and review standards.

Open `references/source-evidence.md` when checking whether this skill covers workflows observed in mined/source repository evidence.

Kubernetes proof loop:

```bash
kubectl get deploy,po,svc,ingress -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --tail=100
kubectl port-forward svc/<service> 8080:<service-port> -n <namespace>
curl -f http://localhost:8080/health || curl -f http://localhost:8080/
```

## Debugging Checklist

- Image build fails: inspect build context, base image, package manager cache, and platform.
- Container exits: inspect command, env vars, working directory, permissions, and logs.
- Service unreachable: inspect port mapping, service selector, readiness, ingress, and network policy.
- Pod pending: inspect resources, node selectors, taints, PVCs, and image pull status.
- CrashLoopBackOff: inspect previous logs and startup probes.

## Done Criteria

- The relevant container or workload starts.
- Logs and health/readiness checks support the result.
- Any destructive or state-changing command is called out in the final notes.
- The final notes include context, namespace, image tag, and proof command output.
