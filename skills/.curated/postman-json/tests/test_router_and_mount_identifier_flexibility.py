import tempfile
import unittest
from pathlib import Path

from scripts.sync_postman_collection import (
    discover_server_file,
    extract_mounts,
    parse_route_endpoints,
)


class RouterAndMountIdentifierFlexibilityTests(unittest.TestCase):
    def test_parse_route_endpoints_supports_non_router_variable_name(self) -> None:
        route_text = """\
import express from "express";

const usersRouter = express.Router();
usersRouter.get("/me", (req, res) => {
  res.json({ ok: true });
});

export default usersRouter;
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            route_file = project_root / "src/routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(route_text, encoding="utf-8")

            endpoints = parse_route_endpoints(
                route_file=route_file,
                mount_path="/users",
                project_root=project_root,
                requirement_cache={},
            )

        self.assertEqual(len(endpoints), 1)
        self.assertEqual(endpoints[0]["method"], "GET")
        self.assertEqual(endpoints[0]["path"], "/users/me")

    def test_parse_route_endpoints_supports_router_alias_registered_as_router(self) -> None:
        route_text = """\
import express from "express";

const usersRouter = express.Router();
const router = usersRouter;

router.get("/me", (req, res) => {
  res.json({ ok: true });
});

export default router;
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            route_file = project_root / "src/routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(route_text, encoding="utf-8")

            endpoints = parse_route_endpoints(
                route_file=route_file,
                mount_path="/users",
                project_root=project_root,
                requirement_cache={},
            )

        self.assertEqual(len(endpoints), 1)
        self.assertEqual(endpoints[0]["method"], "GET")
        self.assertEqual(endpoints[0]["path"], "/users/me")

    def test_parse_route_endpoints_scans_only_mounted_router_alias_chain(self) -> None:
        route_text = """\
import express from "express";

const usersRouter = express.Router();
const router = usersRouter;
const adminRouter = express.Router();

router.get("/me", (req, res) => {
  res.json({ ok: true });
});
adminRouter.get("/stats", (req, res) => {
  res.json({ ok: true });
});
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            route_file = project_root / "src/routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(route_text, encoding="utf-8")

            endpoints = parse_route_endpoints(
                route_file=route_file,
                mount_path="/users",
                project_root=project_root,
                requirement_cache={},
                mounted_router_name="usersRouter",
            )

        self.assertEqual(len(endpoints), 1)
        self.assertEqual(endpoints[0]["method"], "GET")
        self.assertEqual(endpoints[0]["path"], "/users/me")

    def test_extract_mounts_supports_non_app_express_instance_name(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");

const api = express();
api.use("/users", usersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["mount_path"], "/users")
        self.assertEqual(mounts[0]["route_file"], route_file.resolve())

    def test_extract_mounts_supports_app_alias_of_express_instance(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");

const api = express();
const app = api;
app.use("/users", usersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["mount_path"], "/users")
        self.assertEqual(mounts[0]["route_file"], route_file.resolve())

    def test_extract_mounts_resolves_named_esm_router_import(self) -> None:
        server_text = """\
import express from "express";
import { usersRouter } from "./routes/users.js";

const app = express();
app.use("/users", usersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(
                """\
import express from "express";

const router = express.Router();
export { router as usersRouter };
""",
                encoding="utf-8",
            )
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["router_name"], "usersRouter")
        self.assertEqual(mounts[0]["mount_path"], "/users")
        self.assertEqual(mounts[0]["route_file"], route_file.resolve())

    def test_extract_mounts_non_literal_multi_argument_mount_falls_back_to_root(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");

const app = express();
const apiPrefix = "/users";
app.use(apiPrefix, usersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["router_name"], "usersRouter")
        self.assertEqual(mounts[0]["mount_path"], "/")
        self.assertEqual(mounts[0]["route_file"], route_file.resolve())

    def test_extract_mounts_supports_multiple_router_callbacks(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");
const ordersRouter = require("./routes/orders");

const app = express();
app.use("/api", usersRouter, ordersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            users_route_file = project_root / "routes/users.js"
            orders_route_file = project_root / "routes/orders.js"
            users_route_file.parent.mkdir(parents=True, exist_ok=True)
            users_route_file.write_text("module.exports = {};\n", encoding="utf-8")
            orders_route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 2)
        by_router = {mount["router_name"]: mount for mount in mounts}
        self.assertEqual(by_router["usersRouter"]["mount_path"], "/api")
        self.assertEqual(by_router["usersRouter"]["route_file"], users_route_file.resolve())
        self.assertEqual(by_router["ordersRouter"]["mount_path"], "/api")
        self.assertEqual(by_router["ordersRouter"]["route_file"], orders_route_file.resolve())

    def test_extract_mounts_supports_middleware_then_router_multi_arg_use(self) -> None:
        server_text = """\
const express = require("express");
const authMiddleware = require("./middleware/auth");
const usersRouter = require("./routes/users");

const app = express();
app.use(authMiddleware, usersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            middleware_file = project_root / "middleware/auth.js"
            users_route_file = project_root / "routes/users.js"
            middleware_file.parent.mkdir(parents=True, exist_ok=True)
            users_route_file.parent.mkdir(parents=True, exist_ok=True)
            middleware_file.write_text(
                "module.exports = (req, res, next) => next();\n", encoding="utf-8"
            )
            users_route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        by_router = {mount["router_name"]: mount for mount in mounts}
        self.assertEqual(by_router["usersRouter"]["mount_path"], "/")
        self.assertEqual(by_router["usersRouter"]["route_file"], users_route_file.resolve())

    def test_extract_mounts_ignores_middleware_call_expr_but_keeps_router_callback(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");

const app = express();
app.use(cors(), usersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            users_route_file = project_root / "routes/users.js"
            users_route_file.parent.mkdir(parents=True, exist_ok=True)
            users_route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["router_name"], "usersRouter")
        self.assertEqual(mounts[0]["mount_path"], "/")
        self.assertEqual(mounts[0]["route_file"], users_route_file.resolve())

    def test_extract_mounts_ignores_require_call_expr_but_keeps_router_callback(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");

const app = express();
app.use(require("./middleware/auth")(), usersRouter);
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            users_route_file = project_root / "routes/users.js"
            auth_file = project_root / "middleware/auth.js"
            users_route_file.parent.mkdir(parents=True, exist_ok=True)
            auth_file.parent.mkdir(parents=True, exist_ok=True)
            users_route_file.write_text("module.exports = {};\n", encoding="utf-8")
            auth_file.write_text(
                "module.exports = () => (req, res, next) => next();\n", encoding="utf-8"
            )
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["router_name"], "usersRouter")
        self.assertEqual(mounts[0]["mount_path"], "/")
        self.assertEqual(mounts[0]["route_file"], users_route_file.resolve())

    def test_extract_mounts_supports_inline_require_final_argument(self) -> None:
        server_text = """\
const express = require("express");
const api = express();

api.use("/users", require("./routes/users"));
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["mount_path"], "/users")
        self.assertEqual(mounts[0]["route_file"], route_file.resolve())

    def test_inline_require_mount_uses_exported_router_name_for_endpoint_parsing(self) -> None:
        server_text = """\
const express = require("express");
const api = express();
api.use("/users", require("./routes/users"));
"""
        route_text = """\
import express from "express";

const router = express.Router();
const adminRouter = express.Router();
router.get("/me", (req, res) => {
  res.json({ ok: true });
});
adminRouter.get("/stats", (req, res) => {
  res.json({ ok: true });
});
export default router;
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(route_text, encoding="utf-8")
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)
            endpoints = parse_route_endpoints(
                route_file=route_file,
                mount_path=mounts[0]["mount_path"],
                project_root=project_root,
                requirement_cache={},
                mounted_router_name=mounts[0]["router_name"],
            )

        self.assertEqual(len(mounts), 1)
        self.assertEqual(mounts[0]["router_name"], "router")
        self.assertEqual(len(endpoints), 1)
        self.assertEqual(endpoints[0]["path"], "/users/me")

    def test_discover_server_file_fallback_supports_non_app_instance_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "index.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(
                """\
const express = require("express");
const router = express.Router();
router.use((req, res, next) => next());
module.exports = router;
""",
                encoding="utf-8",
            )
            server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("./routes/users");
const api = express();
api.use("/users", usersRouter);
""",
                encoding="utf-8",
            )

            discovered = discover_server_file(project_root, explicit_server_file=None)

        self.assertEqual(discovered, server_file.resolve())

    def test_discover_server_file_fallback_supports_app_alias_mounts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "index.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("./routes/users");
const api = express();
const app = api;
app.use("/users", usersRouter);
""",
                encoding="utf-8",
            )

            discovered = discover_server_file(project_root, explicit_server_file=None)

        self.assertEqual(discovered, server_file.resolve())

    def test_discover_server_file_excluded_dirs_are_scoped_to_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "build" / "repo"
            project_root.mkdir(parents=True, exist_ok=True)
            server_file = project_root / "index.js"
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("./routes/users");
const app = express();
app.use("/users", usersRouter);
""",
                encoding="utf-8",
            )

            discovered = discover_server_file(project_root, explicit_server_file=None)

        self.assertEqual(discovered, server_file.resolve())

    def test_discover_server_file_fallback_ignores_non_express_app_use_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            frontend_file = project_root / "main.js"
            express_server_file = project_root / "src/api-entry.js"
            express_server_file.parent.mkdir(parents=True, exist_ok=True)

            frontend_file.write_text(
                """\
const app = createApp(App);
app.use(router);
""",
                encoding="utf-8",
            )
            express_server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("../routes/users");
const api = express();
const app = api;
app.use("/users", usersRouter);
""",
                encoding="utf-8",
            )

            discovered = discover_server_file(project_root, explicit_server_file=None)

        self.assertEqual(discovered, express_server_file.resolve())


if __name__ == "__main__":
    unittest.main()
