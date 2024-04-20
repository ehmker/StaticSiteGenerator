from htmlnode import (
    HTMLNode,
    ParentNode,
    LeafNode,
)
from inline_md import text_to_textnodes
from textnode import text_node_to_html_node

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
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unord_list = "unordered_list"
block_type_ord_list = "ordered_list"


def markdown_to_html_node(markdown):
    md_blocks = split_block_markdown(markdown)
    # print(md_blocks)
    children_nodes = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        children_nodes.append(markdown_block_to_html_node(block, block_type))

    return ParentNode("div", children_nodes)


def markdown_block_to_html_node(md_block, md_block_type):
    def build_inline_html_nodes(md):
        inline_html_nodes = []
        for node in text_to_textnodes(md):
            inline_html_nodes.append(text_node_to_html_node(node))
        return inline_html_nodes

    def build_list_item_nodes(md):
        list_items = []
        lines = md.split("\n")

        for line in lines:
            line = line.strip()
            li = line.split(" ", 1)[1]
            inline_nodes = build_inline_html_nodes(li)
            list_items.append(ParentNode("li", inline_nodes))

            # md = md.replace(" * ", " - ")
            # lines = md.strip("-* ").split(" - ")
            # for line in lines:
            #     inline_nodes = build_inline_html_nodes(line)
            #     list_items.append(ParentNode("li", inline_nodes))

        return list_items

    def build_paragraph(md):
        md = md.replace("\n", " ")
        inline_nodes = build_inline_html_nodes(md)
        paragraph_node = ParentNode("p", inline_nodes)
        return paragraph_node

    def build_heading(md):
        heading_sections = md.split(" ", 1)
        inline_nodes = build_inline_html_nodes(heading_sections[1])
        heading_tag = f"h{len(heading_sections[0])}"
        heading_node = ParentNode(heading_tag, inline_nodes)
        return heading_node

    def build_code(md):
        md = md.strip("```")
        code_node = ParentNode("pre", [LeafNode("code", md)])
        return code_node

    def build_quote(md):
        lines = md.split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].strip().strip("> ")
        inline_nodes = build_inline_html_nodes(" ".join(lines))
        quote_node = ParentNode("blockquote", inline_nodes)
        return quote_node

    def build_ordered_list(md):
        list_items = build_list_item_nodes(md)
        ordered_list_node = ParentNode("ol", list_items)
        return ordered_list_node

    def build_unordered_list(md):
        list_items = build_list_item_nodes(md)
        unordered_list_node = ParentNode("ul", list_items)
        return unordered_list_node

    if md_block_type == block_type_paragraph:
        return build_paragraph(md_block)
    if md_block_type == block_type_heading:
        return build_heading(md_block)
    if md_block_type == block_type_code:
        return build_code(md_block)
    if md_block_type == block_type_quote:
        return build_quote(md_block)
    if md_block_type == block_type_ord_list:
        return build_ordered_list(md_block)
    if md_block_type == block_type_unord_list:
        return build_unordered_list(md_block)


def split_block_markdown(text):
    blocks_of_text = text.split("\n\n")
    blocks = []
    for block in blocks_of_text:
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks
    # blocks = []
    # block_of_text = []
    # text = text.strip().split("\n")
    # for i in text:
    #     i = i.strip()
    #     if i == "":
    #         if block_of_text != []:
    #             blocks.append("\n".join(block_of_text))
    #             # blocks.append(block_of_text)
    #         block_of_text = []
    #         continue
    #     block_of_text.append(i)
    # if block_of_text != []:
    #     blocks.append("\n".join(block_of_text))
    # return blocks


def block_to_block_type(md_block):
    def block_is_heading(md: str):
        return (
            md.startswith("# ")
            or md.startswith("## ")
            or md.startswith("### ")
            or md.startswith("#### ")
            or md.startswith("##### ")
            or md.startswith("###### ")
        )

    def block_is_quote(md):
        for line in md.split("\n"):
            line = line.strip()
            if line[0] != ">":
                return False
        return True

    def block_is_unord(md):
        for line in md.split("\n"):
            if line.strip()[0:2] not in ["* ", "- "]:
                return False
        return True

    def block_is_ord(md):
        n = 1
        for line in md.split("\n"):
            line = line.strip()
            if not line.startswith(f"{n}. "):
                return False
            n += 1
        return True

    if block_is_heading(md_block):
        return block_type_heading
    if md_block[0:3] == "```" and md_block[-3:] == "```":
        return block_type_code
    if block_is_quote(md_block):
        return block_type_quote
    if block_is_unord(md_block):
        return block_type_unord_list
    if block_is_ord(md_block):
        return block_type_ord_list
    return block_type_paragraph


# def main():
#     # """# This is a heading

#     # This is a paragraph of text. It has some **bold** and *italic* words inside of it.

#     # * This is a list item
#     # * This is another list item
#     # """

#     # node = markdown_to_html_node(md)
#     # print("node =", node, "\n\n")
#     # html = node.to_html()
#     # print(html, "\n")
#     # print(
#     #     "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
#     # )


# if __name__ == "__main__":
#     main()
