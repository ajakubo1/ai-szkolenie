import shutil
from pathlib import Path

import bleach
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
DATA_DIR = ROOT / "data"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"

MARKDOWN_ALLOWED_TAGS = {
    "a",
    "blockquote",
    "br",
    "code",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "ul",
}
MARKDOWN_ALLOWED_ATTRIBUTES = {"a": ["href", "title"]}
MARKDOWN_ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def clean_dist():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    DIST_DIR.mkdir(parents=True, exist_ok=True)


def copy_static():
    target = DIST_DIR / "static"
    shutil.copytree(STATIC_DIR, target, dirs_exist_ok=True)


def load_data():
    with open(DATA_DIR / "prompts.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    for section in data["sections"]:
        for prompt in section["prompts"]:
            load_markdown_prompt(prompt)

    return data


def load_markdown_prompt(prompt):
    markdown_file = prompt.get("markdown_file")
    if markdown_file is None:
        return

    if "text" in prompt:
        raise ValueError(
            f"Prompt {prompt['number']} cannot define both 'text' and 'markdown_file'."
        )

    markdown_path = Path(markdown_file)
    if markdown_path.is_absolute() or markdown_path.suffix.lower() != ".md":
        raise ValueError(
            f"Prompt {prompt['number']} must reference a relative .md file in data/."
        )

    data_root = DATA_DIR.resolve()
    source_path = (DATA_DIR / markdown_path).resolve()
    try:
        source_path.relative_to(data_root)
    except ValueError as error:
        raise ValueError(
            f"Prompt {prompt['number']} references a Markdown file outside data/."
        ) from error

    if not source_path.is_file():
        raise ValueError(
            f"Prompt {prompt['number']} Markdown file does not exist: {markdown_file}"
        )

    source = source_path.read_text(encoding="utf-8")
    rendered_html = markdown.markdown(source, extensions=["fenced_code", "sane_lists"])
    prompt["markdown_html"] = Markup(
        bleach.clean(
            rendered_html,
            tags=MARKDOWN_ALLOWED_TAGS,
            attributes=MARKDOWN_ALLOWED_ATTRIBUTES,
            protocols=MARKDOWN_ALLOWED_PROTOCOLS,
            strip=True,
        )
    )


def render_index(data):
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "xml", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("index.html.j2")
    html = template.render(**data)

    output_file = DIST_DIR / "index.html"
    output_file.write_text(html, encoding="utf-8")


def main():
    clean_dist()
    copy_static()

    data = load_data()
    render_index(data)

    print(f"Webpage generated in {DIST_DIR}")


if __name__ == "__main__":
    main()
