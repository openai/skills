### Deployment Pipeline Logic
Our CI/CD process follows a strict hierarchy:

Code Push: Triggered on every commit to main.

Lint & Test: Runs automatically.

If tests fail, the pipeline halts and notifies the dev.

If tests pass, it moves to the Build stage.

Docker Build: Creates a container image and pushes to ECR.

Staging Deploy: Deploys to the k8s staging cluster.

Manual Approval: A senior dev must click 'Approve' before the final production push.
