import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
TEMPLATES_DIR = ROOT / "templates"
DATA_DIR = ROOT / "data"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"


def clean_dist():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    DIST_DIR.mkdir(parents=True, exist_ok=True)


def copy_static():
    target = DIST_DIR / "static"
    shutil.copytree(STATIC_DIR, target, dirs_exist_ok=True)


def load_data():
    with open(DATA_DIR / "prompts.yml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


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
