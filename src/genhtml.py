import os
import shutil
from block_md import markdown_to_html_node


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    else:
        raise Exception("Markdown missing title header")


def get_file_content(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content


def generate_page(src_path: str, template_path, dest_path):
    if not src_path.endswith(".md"):
        raise Exception("not .md file")
    print(f"Generating page from {src_path} to {dest_path} using {template_path}")

    md_file_content = get_file_content(src_path)
    template_file_content = get_file_content(template_path)

    html_node = markdown_to_html_node(md_file_content)
    title = extract_title(md_file_content)

    html_content = template_file_content.replace("{{ Title }}", title)
    html_content = html_content.replace("{{ Content }}", html_node.to_html())

    # if not os.path.exists(dest_path):
    #     os.makedirs(dest_path)
    with open(dest_path, "w") as f:
        f.write(html_content)


def generate_pages_recursive(src_path_content, template_path, dest_dir_path):
    print(
        f"generating page from {src_path_content} to {dest_dir_path} using {template_path}"
    )
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    src_dir = os.scandir(src_path_content)

    for f in src_dir:
        dst_f = os.path.join(dest_dir_path, f.name)
        if f.is_file():
            generate_page(f.path, template_path, dst_f.replace(".md", ".html"))
        else:
            generate_pages_recursive(f.path, template_path, dst_f)

        # print(f"source:{f.path} --> destination: {dst_f}")

    pass


dir_path = "content"
template = "template.html"
dst_path = "public"

generate_pages_recursive(dir_path, template, dst_path)
