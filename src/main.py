from copystatic import copy_folder
from html_generator import generate_pages_recursive


def main():
    copy_folder("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")
    pass


if __name__ == "__main__":
    main()
