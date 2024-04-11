ex_text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
ex_text_two = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""


def split_block_markdown(text):
    blocks = []
    block_of_text = []
    for i in text.split("\n"):
        i = i.strip()
        if i == "":
            if block_of_text != []:
                blocks.append("\n".join(block_of_text))
            block_of_text = []
            continue
        block_of_text.append(i)
    return blocks


def main():
    for i in split_block_markdown(ex_text):
        print(i)
        print("-----------------")
    print("==============================================")
    for i in split_block_markdown(ex_text_two):
        print(i)
        print("-----------------")


if __name__ == "__main__":
    main()
