import os
import shutil
from genhtml import generate_pages_recursive


def copytree(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    scr_dir = os.scandir(src)
    for f in scr_dir:
        dst_f = os.path.join(dst, f.name)
        print(f"copying {f.path} -> {dst_f}")
        if f.is_file():
            shutil.copy(f.path, dst_f)
        else:
            copytree(f.path, dst_f)


def main():
    from_path = "content"
    template = "template.html"
    dest_path = "public"
    if os.path.exists("public"):
        shutil.rmtree("public")
    copytree("static", "public")
    generate_pages_recursive(from_path, template, dest_path)


main()
