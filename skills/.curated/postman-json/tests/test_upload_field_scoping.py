import tempfile
import unittest
from pathlib import Path

from scripts.sync_postman_collection import build_request, parse_route_endpoints


class UploadFieldScopingTests(unittest.TestCase):
    def test_upload_fields_are_scoped_to_each_route_call(self) -> None:
        route_text = """\
import express from "express";

const router = express.Router();

router.post("/avatar", upload.single("avatar"), (req, res) => {
  res.json({ ok: true });
});

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

        by_path = {entry["path"]: entry for entry in endpoints}
        upload_endpoint = by_path["/users/avatar"]
        non_upload_endpoint = by_path["/users/me"]

        self.assertEqual(upload_endpoint["upload_fields"], ["avatar"])
        self.assertTrue(upload_endpoint["needs_file"])
        self.assertEqual(non_upload_endpoint["upload_fields"], [])
        self.assertFalse(non_upload_endpoint["needs_file"])

    def test_upload_fields_extracts_multer_fields_array_names(self) -> None:
        route_text = """\
import express from "express";

const router = express.Router();

router.post(
  "/documents",
  upload.fields([{ name: "avatar" }, { name: "coverImage", maxCount: 1 }]),
  (req, res) => {
    res.json({ ok: true });
  }
);

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

        by_path = {entry["path"]: entry for entry in endpoints}
        upload_endpoint = by_path["/users/documents"]

        self.assertEqual(upload_endpoint["upload_fields"], ["avatar", "coverImage"])
        self.assertTrue(upload_endpoint["needs_file"])

        request = build_request(upload_endpoint)
        form_data = request["body"]["formdata"]
        file_keys = [field["key"] for field in form_data if field["type"] == "file"]
        self.assertEqual(file_keys, ["avatar", "coverImage"])
        self.assertNotIn("file", file_keys)


if __name__ == "__main__":
    unittest.main()
