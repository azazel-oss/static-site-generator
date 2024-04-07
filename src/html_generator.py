from markdown_block import markdown_to_html_node
import os
import pathlib


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.strip("# ")
    raise ValueError


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        source_content = ""
        for line in file:
            source_content += line

    print(source_content)
    with open(template_path, "r") as file:
        template_data = ""
        for line in file:
            template_data += line

    title = extract_title(source_content)
    content = markdown_to_html_node(source_content).to_html()

    template_data = template_data.replace("{{ Title }}", title)
    template_data = template_data.replace("{{ Content }}", content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template_data)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    markdown_files = os.listdir(dir_path_content)
    for entry in markdown_files:
        if os.path.isfile(os.path.join(dir_path_content, entry)):
            file_html_name = os.path.join(
                dest_dir_path, pathlib.Path(entry.strip(".md") + ".html")
            )
            generate_page(
                os.path.join(dir_path_content, entry), template_path, file_html_name
            )
        else:
            file_html_name = os.path.join(
                dest_dir_path, entry, pathlib.Path("index.html")
            )
            generate_page(
                os.path.join(dir_path_content, entry, pathlib.Path("index.md")),
                template_path,
                file_html_name,
            )
