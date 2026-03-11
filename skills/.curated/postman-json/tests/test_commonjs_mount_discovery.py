import tempfile
import unittest
from pathlib import Path

from scripts.sync_postman_collection import extract_mounts


class CommonJsMountDiscoveryTests(unittest.TestCase):
    def test_extract_mounts_resolves_commonjs_require_router_alias(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");

const app = express();
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
        self.assertEqual(mounts[0]["router_name"], "usersRouter")
        self.assertEqual(mounts[0]["mount_path"], "/users")
        self.assertEqual(mounts[0]["route_file"], route_file.resolve())

    def test_extract_mounts_supports_root_mount_single_argument(self) -> None:
        server_text = """\
const express = require("express");
const usersRouter = require("./routes/users");

const app = express();
app.use(usersRouter);
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


if __name__ == "__main__":
    unittest.main()
