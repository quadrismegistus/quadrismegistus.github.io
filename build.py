#!/usr/bin/env python
import html
import os
import subprocess

ROOT = os.path.dirname(__file__)
THEME_PATH = os.path.join(ROOT, "theme.html")
NAV_LINKS_PATH = os.path.join(ROOT, "nav_links.txt")

with open(THEME_PATH) as theme_f:
    theme = theme_f.read()


def discover_pages():
    pages = []
    for root, dirs, files in os.walk(ROOT, topdown=True):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        if "README.md" in files:
            rel = os.path.relpath(root, ROOT)
            pages.append("" if rel == "." else rel.replace(os.sep, "/"))
    pages.sort(key=lambda p: (p != "", p.lower()))
    return pages


def read_title(readme_path, fallback):
    with open(readme_path) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("# "):
                return "Ryan Heuser - " + stripped[2:].strip()
    return fallback


def fallback_title(rel_path):
    if not rel_path:
        return "Ryan Heuser"
    return "Ryan Heuser - " + rel_path.split("/")[-1].replace("-", " ").replace("_", " ").title()


def page_href(rel_path):
    return "/" if not rel_path else f"/{rel_path}/"


def load_nav_links():
    nav_items = []
    current_group = None
    with open(NAV_LINKS_PATH) as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.startswith("[") and stripped.endswith("]"):
                label = stripped[1:-1].strip()
                current_group = {"type": "group", "label": label, "links": []}
                nav_items.append(current_group)
                continue

            rel_path, label = (part.strip() for part in stripped.split("|", 1))
            link_item = {"type": "link", "path": rel_path, "label": label}
            if current_group is not None:
                current_group["links"].append(link_item)
            else:
                nav_items.append(link_item)
    return nav_items


def build_nav(nav_items, current_path):
    # items = ["<h2>Pages</h2>", "<ul>"]
    items = ["<ul>"]
    for item in nav_items:
        if item["type"] == "link":
            rel_path = item["path"]
            label = html.escape(item["label"])
            href = page_href(rel_path)
            active = ' class="active"' if rel_path == current_path else ""
            items.append(f'  <li><a{active} href="{href}">{label}</a></li>')
            continue

        group_label = html.escape(item["label"])
        items.append('  <li class="nav-group">')
        items.append(f'    <span class="nav-group-label">{group_label}</span>')
        items.append("    <ul>")
        for link in item["links"]:
            rel_path = link["path"]
            label = html.escape(link["label"])
            href = page_href(rel_path)
            active = ' class="active"' if rel_path == current_path else ""
            items.append(f'      <li><a{active} href="{href}">{label}</a></li>')
        items.append("    </ul>")
        items.append("  </li>")
    items.append("</ul>")
    return "\n".join(items)


def render_markdown(page_root):
    content = subprocess.check_output(["pandoc", "README.md"], cwd=page_root, text=True)
    return content.replace("&lt;", "<").replace("&gt;", ">")


pages = discover_pages()
nav_links = load_nav_links()
titles = {}

for rel_path in pages:
    readme = os.path.join(ROOT, rel_path, "README.md") if rel_path else os.path.join(ROOT, "README.md")
    titles[rel_path] = read_title(readme, fallback_title(rel_path))

for rel_path in pages:
    page_root = os.path.join(ROOT, rel_path) if rel_path else ROOT
    content = render_markdown(page_root)
    nav = build_nav(nav_links, rel_path)
    title = html.escape(titles[rel_path])
    total = theme.replace("[[TITLE]]", title).replace("[[NAV]]", nav).replace("[[CONTENT]]", content)

    with open(os.path.join(page_root, "index.html"), "w") as of:
        of.write(total)
