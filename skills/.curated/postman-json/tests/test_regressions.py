import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from scripts.sync_postman_collection import (
    build_generated_tree,
    build_request,
    discover_server_file,
    extract_body_fields,
    extract_mounts,
    load_collection,
    main,
    parse_js_string_literal,
    parse_route_endpoints,
)


def _collect_request_items(items):
    collected = []
    for item in items:
        if isinstance(item, dict) and "request" in item:
            collected.append(item)
            continue
        if isinstance(item, dict):
            nested = item.get("item")
            if isinstance(nested, list):
                collected.extend(_collect_request_items(nested))
    return collected


class RegressionTests(unittest.TestCase):
    def test_collection_name_flag_overrides_existing_collection_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            output_file = project_root / "postman.json"
            route_file.parent.mkdir(parents=True, exist_ok=True)

            server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("./routes/users");
const app = express();
app.use("/users", usersRouter);
""",
                encoding="utf-8",
            )
            route_file.write_text(
                """\
const express = require("express");
const router = express.Router();
router.get("/me", (req, res) => res.json({ ok: true }));
module.exports = router;
""",
                encoding="utf-8",
            )

            first_code = main(
                [
                    "--project-root",
                    str(project_root),
                    "--output",
                    str(output_file),
                    "--collection-name",
                    "First Name",
                ]
            )
            self.assertEqual(first_code, 0)

            second_code = main(
                [
                    "--project-root",
                    str(project_root),
                    "--output",
                    str(output_file),
                    "--collection-name",
                    "Second Name",
                ]
            )
            self.assertEqual(second_code, 0)

            collection = json.loads(output_file.read_text(encoding="utf-8"))

        self.assertEqual(collection["info"]["name"], "Second Name")

    def test_extract_mounts_does_not_treat_single_call_expression_as_router(self) -> None:
        server_text = """\
const express = require("express");
const cors = require("./middlewares/cors");
const app = express();
app.use(cors());
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            middleware_file = project_root / "middlewares/cors.js"
            middleware_file.parent.mkdir(parents=True, exist_ok=True)
            middleware_file.write_text(
                "module.exports = () => (req, res, next) => next();\n",
                encoding="utf-8",
            )
            server_file.write_text(server_text, encoding="utf-8")

            mounts = extract_mounts(server_file, server_text)

        self.assertEqual(mounts, [])

    def test_parse_route_endpoints_returns_empty_for_unreadable_route_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            route_file = project_root / "routes/missing.js"
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                endpoints = parse_route_endpoints(
                    route_file=route_file,
                    mount_path="/",
                    project_root=project_root,
                    requirement_cache={},
                )

        self.assertEqual(endpoints, [])
        self.assertIn("Warning: cannot read route file", stderr.getvalue())

    def test_parse_route_endpoints_ignores_non_express_router_variable(self) -> None:
        route_text = """\
const router = createRouter();
router.get("/not-express", (req, res) => {
  res.json({ ok: true });
});
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            route_file = project_root / "routes/not-express.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(route_text, encoding="utf-8")

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                endpoints = parse_route_endpoints(
                    route_file=route_file,
                    mount_path="/users",
                    project_root=project_root,
                    requirement_cache={},
                )

        self.assertEqual(endpoints, [])
        self.assertIn("Warning: no router identifiers detected", stderr.getvalue())

    def test_extract_mounts_ignores_non_express_app_identifier(self) -> None:
        server_text = """\
const usersRouter = require("./routes/users");
const app = createApp();
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

        self.assertEqual(mounts, [])

    def test_body_fields_include_inline_middleware_fields(self) -> None:
        route_text = """\
const express = require("express");
const router = express.Router();
router.post(
  "/login",
  (req, res, next) => {
    const { tenant } = req.body;
    next();
  },
  (req, res) => {
    res.json({ ok: true });
  }
);
module.exports = router;
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            route_file = project_root / "routes/users.js"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text(route_text, encoding="utf-8")

            endpoints = parse_route_endpoints(
                route_file=route_file,
                mount_path="/users",
                project_root=project_root,
                requirement_cache={},
            )

        self.assertEqual(len(endpoints), 1)
        self.assertIn("tenant", endpoints[0]["body_fields"])

    def test_parse_js_string_literal_unescapes_slashes(self) -> None:
        self.assertEqual(parse_js_string_literal("'/api\\/v1/users'"), "/api/v1/users")

    def test_extract_body_fields_supports_bracket_notation(self) -> None:
        source_text = """\
const userId = req.body["userId"];
const status = req.body['status'];
"""
        fields = extract_body_fields(source_text)
        self.assertIn("userId", fields)
        self.assertIn("status", fields)

    def test_discover_server_file_fallback_scans_skills_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "skills" / "api-entry.js"
            route_file = project_root / "routes" / "users.js"
            server_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.parent.mkdir(parents=True, exist_ok=True)
            route_file.write_text("module.exports = {};\n", encoding="utf-8")
            server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("../routes/users");
const app = express();
app.use("/users", usersRouter);
""",
                encoding="utf-8",
            )

            discovered = discover_server_file(project_root, explicit_server_file=None)

        self.assertEqual(discovered, server_file.resolve())

    def test_build_generated_tree_normalizes_windows_relative_paths(self) -> None:
        endpoint = {
            "method": "GET",
            "path": "/users/me",
            "path_postman": "/users/me",
            "route_file_relative": "routes\\users.js",
            "middleware_names": [],
            "body_fields": [],
            "upload_fields": [],
            "needs_file": False,
            "auth_required": False,
        }
        tree = build_generated_tree([endpoint], "source")
        self.assertEqual(tree["item"][0]["name"], "routes")
        self.assertEqual(tree["item"][0]["item"][0]["name"], "users")

    def test_load_collection_warns_on_schema_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            collection_path = Path(temp_dir) / "collection.json"
            collection_path.write_text(
                json.dumps(
                    {
                        "info": {
                            "name": "Example",
                            "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json",
                        },
                        "item": [],
                        "variable": [],
                    }
                ),
                encoding="utf-8",
            )
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                load_collection(collection_path, "Example")

        self.assertIn("Warning: existing collection uses schema", stderr.getvalue())

    def test_build_request_outputs_structured_url(self) -> None:
        endpoint = {
            "method": "GET",
            "path": "/users/:userId",
            "path_postman": "/users/{{userId}}",
            "route_file_relative": "routes/users.js",
            "body_fields": [],
            "upload_fields": [],
            "needs_file": False,
            "auth_required": False,
        }
        request = build_request(endpoint)
        self.assertIsInstance(request["url"], dict)
        self.assertEqual(request["url"]["raw"], "{{baseUrl}}/users/{{userId}}")
        self.assertEqual(request["url"]["path"], ["users", "{{userId}}"])

    def test_main_warns_when_mount_yields_no_endpoints(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            output_file = project_root / "postman.json"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("./routes/users");
const app = express();
app.use("/users", usersRouter);
""",
                encoding="utf-8",
            )
            route_file.write_text("module.exports = {};\n", encoding="utf-8")

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                exit_code = main(
                    [
                        "--project-root",
                        str(project_root),
                        "--output",
                        str(output_file),
                    ]
                )

        self.assertEqual(exit_code, 1)
        self.assertIn("Warning: no endpoints found in", stderr.getvalue())

    def test_main_deduplicates_duplicate_method_path_endpoints(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/users.js"
            output_file = project_root / "postman.json"
            route_file.parent.mkdir(parents=True, exist_ok=True)
            server_file.write_text(
                """\
const express = require("express");
const usersRouter = require("./routes/users");
const alias = usersRouter;
const app = express();
app.use("/users", usersRouter);
app.use("/users", alias);
""",
                encoding="utf-8",
            )
            route_file.write_text(
                """\
const express = require("express");
const router = express.Router();
router.get("/me", (req, res) => {
  res.json({ ok: true });
});
module.exports = router;
""",
                encoding="utf-8",
            )

            exit_code = main(
                [
                    "--project-root",
                    str(project_root),
                    "--output",
                    str(output_file),
                ]
            )
            self.assertEqual(exit_code, 0)
            collection = json.loads(output_file.read_text(encoding="utf-8"))

        requests = _collect_request_items(collection["item"])
        self.assertEqual(len(requests), 1)


if __name__ == "__main__":
    unittest.main()
