# COPR API v3 With curl

Use this guide when `copr-cli` is insufficient and a direct API call is needed.

## 1. Load Auth From `~/.config/copr`

```sh
COPR_CONFIG="${COPR_CONFIG:-$HOME/.config/copr}"
COPR_URL="$(awk -F '=' '/^[[:space:]]*copr_url[[:space:]]*=/{gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2); print $2; exit}' "$COPR_CONFIG")"
COPR_LOGIN="$(awk -F '=' '/^[[:space:]]*login[[:space:]]*=/{gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2); print $2; exit}' "$COPR_CONFIG")"
COPR_TOKEN="$(awk -F '=' '/^[[:space:]]*token[[:space:]]*=/{gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2); print $2; exit}' "$COPR_CONFIG")"
```

`python-copr` uses `(login, token)` as HTTP basic auth credentials, so mirror that with:

```sh
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" "$COPR_URL/api_3/auth-check"
```

## 2. Common Read Calls

```sh
# List projects for owner (ownername can be @group)
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" \
  "$COPR_URL/api_3/project/list?ownername=@copr"

# Get one project
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" \
  "$COPR_URL/api_3/project/?ownername=@copr&projectname=copr-dev"

# List builds in project
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" \
  "$COPR_URL/api_3/build/list?ownername=@copr&projectname=copr-dev"

# Get one build
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" \
  "$COPR_URL/api_3/build/123456"

# List packages in project
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" \
  "$COPR_URL/api_3/package/list?ownername=@copr&projectname=copr-dev"
```

## 3. Common Write Calls

```sh
# Cancel build
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" -X PUT \
  "$COPR_URL/api_3/build/cancel/123456"

# Regenerate repos
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" -X POST \
  "$COPR_URL/api_3/project/regenerate-repos/@copr/copr-dev"
```

## 4. JSON Body Examples

```sh
# Create project
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" \
  -H 'Content-Type: application/json' \
  -X POST "$COPR_URL/api_3/project/add/@copr" \
  -d '{
    "name": "my-project",
    "chroots": ["fedora-rawhide-x86_64"],
    "description": "example"
  }'

# Trigger URL build
curl -sS -u "$COPR_LOGIN:$COPR_TOKEN" \
  -H 'Content-Type: application/json' \
  -X POST "$COPR_URL/api_3/build/create/url" \
  -d '{
    "ownername": "@copr",
    "projectname": "copr-dev",
    "pkgs": ["https://example.org/package.src.rpm"]
  }'
```

## 5. Endpoint Discovery

- Browse quick path list: `references/copr-api-v3-paths.txt`
- Inspect full schema: `references/copr-api-v3-swagger.json`
- Refresh live schema:

```sh
curl -fsSL "$COPR_URL/api_3/swagger.json" -o ./copr-api-v3-swagger.json
```
