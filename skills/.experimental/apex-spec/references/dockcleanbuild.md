# dockcleanbuild

Perform a full Docker cleanup and rebuild cycle: clear build cache, remove stale images,
stop and remove the project's containers (preserving volumes/data), rebuild all images
from scratch with no cache, bring containers back up, and clean up leftover artifacts.

Note: Docker commands MAY require `sudo` if you are not in the `docker` group.

## Rules

1. **Preserve volumes** - Never remove Docker volumes or their data; only containers and images are cleaned
2. **No cache on rebuild** - All image builds must use `--no-cache` to ensure a clean build
3. **Build order matters** - Build the primary Dockerfile (repo image) first, then any secondary Dockerfiles (e.g., Dockerfile.local, Dockerfile.dev, or other customizations)
4. **Report everything** - Surface ALL issues, warnings, errors, deprecation notices, and update notices regardless of severity -- even cosmetic or expected ones
5. **Read-only on spec system** - Never modify state.json, session specs, or task checklists
6. **Sudo required** - Prefix all docker/docker-compose commands with `sudo`

## Steps

### 1. Clean Docker build cache

Run `sudo docker builder prune -af` to remove all build cache entries.

Report the amount of space reclaimed.

### 2. Remove stale images

Run `sudo docker image prune -f` to remove dangling images.

Report the number of images removed and space reclaimed.

### 3. Stop and remove project containers

Identify the project's Docker Compose file(s) (`docker-compose.yml`, `docker-compose.yaml`,
`compose.yml`, `compose.yaml`, or variants).

Run `sudo docker compose down` (without `-v` to preserve volumes) to stop and remove
the project's containers and networks.

Report which containers were stopped and removed.

### 4. Build from source

Run the project's build step if one exists (e.g., `npm run build`, `cargo build`, etc.).
If no build step is apparent, skip this step and note it.

### 5. Rebuild Docker images from scratch

First, build the primary Dockerfile:
```bash
sudo docker compose build --no-cache
```

If additional Dockerfiles exist (e.g., `Dockerfile.local`, `Dockerfile.dev`,
`Dockerfile.production`), build each one:
```bash
sudo docker build --no-cache -f <Dockerfile> -t <appropriate-tag> .
```

Report the full build output for each image, including any warnings or notices.

### 6. Bring containers back up

Run `sudo docker compose up -d` to start the containers in detached mode.

Verify containers are running with `sudo docker compose ps`.

**If any container fails to start, investigate the root cause (port conflicts,
missing dependencies, config errors, etc.), resolve it, and retry
`sudo docker compose up -d` until ALL containers are running or healthy.
Do not proceed until every service is up.**

Report the status of each container.

### 7. Final cleanup

Run `sudo docker image prune -f` to remove any intermediate or dangling images
left over from the build process.

Report the number of images cleaned and space reclaimed.

## Output

Provide a full report including:
- Space reclaimed from cache and image cleanup
- Containers stopped/removed
- Build output for each Dockerfile (including ALL warnings, errors, notices)
- Container status after restart
- Final cleanup results
- Any issues encountered at any step, no matter how minor
