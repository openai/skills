import json
import tempfile
import unittest
from pathlib import Path

from scripts.sync_postman_collection import main


class CollectionVariableTests(unittest.TestCase):
    def test_sync_creates_generic_token_variable_when_auth_is_referenced(self) -> None:
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

router.post("/secure", authMiddleware, (req, res) => {
  const { email } = req.body;
  res.json({ ok: true, email });
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

        variables = {entry["key"] for entry in collection.get("variable", [])}
        self.assertIn("baseUrl", variables)
        self.assertIn("token", variables)

    def test_sync_creates_route_param_variables_when_referenced(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            server_file = project_root / "server.js"
            route_file = project_root / "routes/orders.js"
            output_file = project_root / "postman.json"
            route_file.parent.mkdir(parents=True, exist_ok=True)

            server_file.write_text(
                """\
const express = require("express");
const ordersRouter = require("./routes/orders");
const app = express();

app.use("/shops", ordersRouter);
""",
                encoding="utf-8",
            )
            route_file.write_text(
                """\
const express = require("express");
const router = express.Router();

router.get("/:shopId/orders/:orderId", (req, res) => {
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

        variables = {entry["key"] for entry in collection.get("variable", [])}
        self.assertIn("baseUrl", variables)
        self.assertIn("shopId", variables)
        self.assertIn("orderId", variables)


if __name__ == "__main__":
    unittest.main()
