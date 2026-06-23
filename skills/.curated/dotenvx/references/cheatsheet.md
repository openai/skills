# Dotenvx Cheatsheet

## Quickstart

```sh
echo "HELLO=World" > .env
dotenvx run -- node index.js
```

```js
require('@dotenvx/dotenvx').config()
```

## Run Anywhere

```sh
dotenvx run -- python3 index.py
dotenvx run -- deno run --allow-env index.ts
dotenvx run -- bun index.js
dotenvx run -- next dev
```

Use `-f` for non-default env files:

```sh
dotenvx run -f .env.production -- node index.js
```

## Multiple Environments

```sh
dotenvx run -f .env.local -f .env -- node index.js
dotenvx run -f .env.local -f .env --overload -- node index.js
dotenvx run --convention=nextjs -- node index.js
DOTENV_ENV=development dotenvx run --convention=flow -- node index.js
```

## Encryption

```sh
dotenvx encrypt
dotenvx ext gitignore --pattern .env.keys
DOTENV_PRIVATE_KEY="..." dotenvx run -- node index.js
DOTENV_PRIVATE_KEY_PRODUCTION="..." dotenvx run -- node index.js
```

Combine multiple encrypted files by setting multiple private keys.

## Advanced

```sh
dotenvx get KEY
dotenvx set KEY value
dotenvx encrypt -f .env.production
dotenvx decrypt -f .env.production
dotenvx rotate -f .env.production
dotenvx keypair -f .env.production
dotenvx ls
```

```sh
dotenvx run --env HELLO=World -- node index.js
dotenvx run --strict -- node index.js
dotenvx run --ignore=MISSING_ENV_FILE -- node index.js
dotenvx run --log-level=debug -- node index.js
```

## Ops

```sh
curl -sfS https://dotenvx.sh/ops | sh
dotenvx ops login
dotenvx ops backup
dotenvx ops status
```
