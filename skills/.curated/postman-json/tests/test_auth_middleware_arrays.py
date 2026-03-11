import tempfile
import unittest
from pathlib import Path

from scripts.sync_postman_collection import build_request, parse_route_endpoints


class AuthMiddlewareArrayTests(unittest.TestCase):
    def test_parse_route_endpoints_detects_auth_middleware_inside_array_argument(self) -> None:
        route_text = """\
import express from "express";

const router = express.Router();

router.get("/secure", [authMiddleware], (req, res) => {
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

        secure_endpoint = next(
            endpoint for endpoint in endpoints if endpoint["path"] == "/users/secure"
        )
        self.assertTrue(secure_endpoint["auth_required"])

        request = build_request(secure_endpoint)
        self.assertEqual(request["auth"]["type"], "bearer")


if __name__ == "__main__":
    unittest.main()
