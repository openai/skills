# Docker and Kubernetes DevOps Workflows

Use this reference for complete container and cluster workflows.

## Contents

- [Dockerfile Review](#dockerfile-review)
- [Compose Workflow](#compose-workflow)
- [Kubernetes Debugging](#kubernetes-debugging)
- [Rollout Workflow](#rollout-workflow)
- [Helm Workflow](#helm-workflow)
- [Security Checks](#security-checks)
- [Final Artifact](#final-artifact)

## Dockerfile Review

Check:

- base image and platform
- lockfile/package install order
- `.dockerignore`
- non-root user
- build vs runtime dependencies
- exposed port
- health/readiness command
- secret handling

Build proof:

```bash
docker build --progress=plain -t local/app-check .
docker run --rm local/app-check <smoke command>
```

## Compose Workflow

```bash
docker compose config
docker compose build
docker compose up
docker compose ps
docker compose logs --tail=100 <service>
docker compose exec <service> <health command>
```

If a service depends on another, verify application readiness, not just container start order.

## Kubernetes Debugging

Inspect in this order:

```bash
kubectl config current-context
kubectl get pods -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --tail=100
kubectl logs <pod> -n <namespace> --previous
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

Failure map:

- `ImagePullBackOff`: image name, tag, registry auth, platform.
- `CrashLoopBackOff`: command, env, config, startup probe, previous logs.
- `Pending`: resources, PVC, taints, node selectors.
- No traffic: selectors, endpoints, readiness, ingress, DNS, network policy.

## Rollout Workflow

```bash
kubectl apply -f manifest.yaml
kubectl rollout status deploy/<name> -n <namespace>
kubectl get deploy,rs,po,svc,ingress -n <namespace>
```

If rollout fails:

```bash
kubectl rollout history deploy/<name> -n <namespace>
kubectl rollout undo deploy/<name> -n <namespace>
```

Ask before undoing in shared or production-like contexts.

## Helm Workflow

```bash
helm lint chart/
helm template release chart/ -f values.yaml
helm upgrade --install release chart/ -f values.yaml --namespace <namespace>
helm status release -n <namespace>
```

For review, prefer values changes over rendered manifest edits.

## Security Checks

- Avoid privileged containers unless required.
- Avoid hostPath unless required.
- Use secrets/config maps intentionally.
- Set resource requests/limits.
- Use read-only root filesystem when practical.
- Keep production secrets out of images and Compose files.

## Final Artifact

Final notes should include:

```text
context/namespace:
image tag:
build command:
deploy/apply command:
logs/health proof:
destructive commands:
remaining risks:
```
