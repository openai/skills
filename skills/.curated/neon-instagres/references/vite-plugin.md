# vite-plugin-db Reference

## Installation

```bash
npm install vite-plugin-db --save-dev
```

## Configuration

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import { postgres } from "vite-plugin-db";

export default defineConfig({
  plugins: [postgres()],
});
```

### Options

```typescript
postgres({
  envFile: "./.env",          // Path to env file (default: ./.env)
  envKey: "DATABASE_URL",     // Env variable name (default: DATABASE_URL)
  seed: "./schema.sql",       // Optional: SQL file to seed database
})
```

## Behavior

1. On `vite dev`, checks if `DATABASE_URL` exists in env file
2. If missing, provisions a new Instagres database
3. Writes connection string to the env file
4. Logs the claim URL to console

## Framework Compatibility

Works with any Vite-based framework:
- React
- Vue
- Svelte
- SolidJS
- Astro
- Nuxt
- SvelteKit
- Remix (Vite mode)

## Plugin Order

**Important**: Place `postgres()` first in the plugins array. Vite plugins execute in order, and the database should be provisioned before other plugins that may depend on `DATABASE_URL`.

## Example with React

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { postgres } from "vite-plugin-db";

export default defineConfig({
  plugins: [postgres(), react()],
});
```

Then run `npm run dev` - the plugin handles database provisioning automatically.
