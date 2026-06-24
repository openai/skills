# Docker and Kubernetes DevOps Mastery Notes

## Mental Model

Docker packages a process and filesystem. Compose coordinates local services. Kubernetes reconciles desired state through controllers. Debug by finding which layer owns the failure.

## Layer Map

```text
source code
Dockerfile/image
container process
Compose service
Kubernetes pod
service/endpoints
ingress/gateway
external client
```

## Safety Boundaries

Always know the active context before mutating state. Treat remote clusters as shared until proven otherwise. Ask before deleting, pruning, restarting production workloads, scaling down, or rolling back.

## Failure Diagnosis

- Build failure: context, base image, package install, platform.
- Start failure: command, env, filesystem, permissions.
- Readiness failure: probes, startup time, dependencies.
- Traffic failure: ports, selectors, endpoints, ingress, DNS.
- Scheduling failure: resources, taints, PVCs.

## Review Standard

A complete DevOps change proves:

- versions/context captured
- build/render/apply command recorded
- logs or health request prove state
- manifests remain declarative
- secrets are not embedded
- destructive actions are disclosed
