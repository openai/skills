# Examples

## Example 1: "Build me a SaaS dashboard" (Path A, 3 variants)

User says: "Build me a SaaS analytics dashboard on Anima"

**Actions:**
1. Generate 3 prompt variants. Each describes mood and audience, not CSS values:
   - V1: "SaaS analytics dashboard for a B2B product team. Clean, minimal feel. Sidebar navigation, KPI cards for MRR, churn rate, and active users, a revenue trend chart, and a recent activity feed. Professional but approachable. Lots of whitespace."
   - V2: "SaaS analytics dashboard for a data-driven startup. Dark theme, bold accent colors, high information density. Top navigation bar, real-time metrics grid, and an interactive data visualization section. Feels like a mission control center."
   - V3: "SaaS analytics dashboard inspired by Linear's design language. Quiet, focused, monochrome with one accent color. Left sidebar with icon navigation, compact metric tiles, activity feed, and a usage heatmap. Feels like a tool you'd use daily without fatigue."
2. Launch all 3 `playground-create` calls in parallel (p2c, react, tailwind)
3. As each returns, call `playground-publish` (webapp mode)
4. Browse each live URL and take a screenshot
5. Return all 3 screenshots with live URLs

**Result:** Three live dashboards, each with a different visual take, delivered within ~10 minutes.

## Example 2: Single build + publish (Path A)

User says: "Build me a SaaS dashboard with a sidebar, analytics cards, and a recent activity table"

**Actions:**
1. Call `playground-create(type="p2c", prompt="SaaS analytics dashboard for a product team tracking growth metrics. Sidebar navigation, analytics cards for key KPIs, and a recent activity table showing user actions. Clean and professional, easy to scan at a glance.", framework="react", styling="tailwind")`
2. Receive `{ sessionId, playgroundUrl }`
3. Call `playground-publish(sessionId="...", mode="webapp")`
4. Take a full-page screenshot via ScreenshotOne
5. Return screenshot and live URL

**Result:** Live dashboard at a public URL, delivered in ~10 minutes. No codebase needed.

## Example 3: Clone a website (Path A)

User says: "Clone the Linear homepage"

**Actions:**
1. Call `playground-create(type="l2c", url="https://linear.app", framework="react", styling="tailwind", language="typescript", uiLibrary="shadcn")`
2. Receive `{ sessionId, playgroundUrl }`
3. Call `playground-publish(sessionId="...", mode="webapp")`
4. Take a screenshot, return with live URL

**Result:** Linear's visual structure recreated as a live site, ready for content replacement.

## Example 4: Implement a Figma design into an existing project (Path B)

User says: "Implement this Figma component: https://figma.com/design/kL9xQn2VwM8pYrTb4ZcHjF/DesignSystem?node-id=42-15"

**Actions:**
1. Parse URL: fileKey=`kL9xQn2VwM8pYrTb4ZcHjF`, nodeId=`42:15` (convert `-` to `:`)
2. Detect project stack: React + CSS Modules + TypeScript + MUI
3. Call `codegen-figma_to_code(fileKey="kL9xQn2VwM8pYrTb4ZcHjF", nodesId=["42:15"], framework="react", styling="css_modules", language="typescript", uiLibrary="mui", assetsBaseUrl="./assets")`
4. Download snapshots and assets, use `guidelines` for design context, implement into project

**Result:** Component matching the Figma design, using MUI and CSS Modules.

## Example 5: Pull playground code into a project (Path B)

User says: "Download the playground we created and integrate it into my project"

**Actions:**
1. Call `project-download_from_playground(playgroundUrl="https://dev.animaapp.com/chat/abc123xyz")`
2. Download and extract the zip
3. Adapt code to the project's stack, components, and design tokens

**Result:** Playground code integrated into the existing project.

## Example 6: Publishing as a design system package

User says: "Publish this as our design system npm package"

**Actions:**
1. Retrieve `sessionId` from the previous `playground-create` call
2. Ask user for package name and version if not provided
3. Call `playground-publish(sessionId="abc123xyz", mode="designSystem", packageName="@acme/design-system", packageVersion="1.0.0")`
4. Receive `{ success, packageUrl, packageName, packageVersion }`

**Result:** "Published @acme/design-system@1.0.0. Install with `npm install @acme/design-system`."
