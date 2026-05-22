# Source Evidence

Use this file as the evidence anchor for the workflow coverage in this skill. Container and cluster work is operationally risky, so the skill emphasizes inspection, minimal reproduction, and proof of readiness.

## Retrieved Sources

- `OpenHands/OpenHands`: Docker development workflows, dev containers, runtime images, Docker runtime configuration, Kubernetes config template fields, Helm compatibility notes, and lock evidence for Docker SDK / Kubernetes client versions.
- `meta-llama/llama-stack`: Docker distribution images, local-to-production deployment framing, health endpoint usage, and Kubernetes client lock evidence.
- `letta-ai/letta`: Docker SDK dependency evidence.
- `openai/openai-agents-python`: sandbox/container agent references.

## Workflows Reflected In The Skill

### Environment Inspection

OpenHands development docs and runtime configuration show Docker and Kubernetes as active developer/runtime environments. The skill therefore requires version/context capture and state inspection before mutation:

- Docker and Compose versions;
- active Kubernetes context and namespace;
- current containers, pods, services, ingress, and events;
- explicit warning before acting on shared or production-like contexts.

### Container Build And Runtime Proof

Source repos use Docker for development containers, runtime sandboxes, and distribution images. The skill requires agents to prove a container starts and responds:

- build with the project Dockerfile;
- run the smallest local command;
- inspect logs;
- hit a health endpoint or root endpoint;
- avoid broad cleanup commands unless requested.

### Kubernetes Diagnosis

OpenHands configuration includes ingress domains, image pull secrets, resource requests/limits, node selectors, tolerations, and privileged runtime settings. The skill covers these as first-class diagnosis points for failing pods and unreachable services.

### Deployment Review

Llama Stack distribution docs emphasize deployment choices without application API changes. The skill therefore requires final notes that include context, namespace, image tag, applied command, logs/health evidence, and any state-changing action.

## Review Standard

Reject Docker/Kubernetes guidance that jumps straight to `apply`, `delete`, `restart`, or cleanup. A useful workflow must inspect the environment, reproduce locally where possible, make minimal declarative changes, and prove readiness with logs plus a request or health check.
