import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build


class MarkdownPromptTests(unittest.TestCase):
    def test_load_data_renders_markdown_and_removes_raw_html(self):
        data = build.load_data()
        prompt = data["sections"][1]["prompts"][0]

        self.assertIn("<ol>", prompt["markdown_html"])
        self.assertIn("<h2>Tekst</h2>", prompt["markdown_html"])

    def test_markdown_prompt_rejects_path_outside_data_directory(self):
        prompt = {"number": 99, "markdown_file": "../outside.md"}

        with self.assertRaisesRegex(ValueError, "outside data"):
            build.load_markdown_prompt(prompt)

    def test_markdown_prompt_rejects_missing_file(self):
        prompt = {"number": 99, "markdown_file": "prompts/missing.md"}

        with self.assertRaisesRegex(ValueError, "does not exist"):
            build.load_markdown_prompt(prompt)

    def test_markdown_prompt_rejects_non_markdown_file(self):
        prompt = {"number": 99, "markdown_file": "prompts/prompt.txt"}

        with self.assertRaisesRegex(ValueError, "relative .md"):
            build.load_markdown_prompt(prompt)

    def test_markdown_prompt_sanitizes_raw_html(self):
        with tempfile.TemporaryDirectory() as directory:
            data_directory = Path(directory)
            markdown_path = data_directory / "prompt.md"
            markdown_path.write_text("<script>alert('xss')</script>", encoding="utf-8")

            with patch.object(build, "DATA_DIR", data_directory):
                prompt = {"number": 99, "markdown_file": "prompt.md"}
                build.load_markdown_prompt(prompt)

        self.assertNotIn("<script", prompt["markdown_html"])
        self.assertNotIn("</script>", prompt["markdown_html"])
