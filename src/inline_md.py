from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_image,
    text_type_link,
    text_type_code,
)
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type):
    # function assumes no nested delimiters in the text
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise Exception("Invalid Markdown: No closing delimiter")
        delimited_text = node.text.split(delimiter)
        in_delimited_space = False
        for item in delimited_text:
            if item == "":
                in_delimited_space = not in_delimited_space
                continue
            if not in_delimited_space:
                new_nodes.append(TextNode(item, text_type_text))
            else:
                new_nodes.append(TextNode(item, text_type))
            in_delimited_space = not in_delimited_space
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        rem_text = node.text
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue
        for img_tup in images:
            split_text = rem_text.split(f"![{img_tup[0]}]({img_tup[1]})", 1)
            if split_text[0] == "":
                new_nodes.append(TextNode(img_tup[0], text_type_image, img_tup[1]))
            else:
                new_nodes.extend(
                    [
                        TextNode(split_text[0], text_type_text),
                        TextNode(img_tup[0], text_type_image, img_tup[1]),
                    ]
                )
            rem_text = split_text[1]

        if rem_text:
            new_nodes.append(TextNode(rem_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        rem_text = node.text
        images = extract_markdown_links(node.text)
        if images == []:
            new_nodes.append(node)
            continue
        for img_tup in images:
            split_text = rem_text.split(f"[{img_tup[0]}]({img_tup[1]})", 1)
            if split_text[0] == "":
                new_nodes.append(TextNode(img_tup[0], text_type_link, img_tup[1]))
            else:
                new_nodes.extend(
                    [
                        TextNode(split_text[0], text_type_text),
                        TextNode(img_tup[0], text_type_link, img_tup[1]),
                    ]
                )
            rem_text = split_text[1]

        if rem_text:
            new_nodes.append(TextNode(rem_text, text_type_text))

    return new_nodes


def text_to_textnodes(text):
    delimiter_dict = {
        "**": text_type_bold,
        "*": text_type_italic,
        "`": text_type_code,
    }
    node = [TextNode(text, text_type_text)]
    for delimiter in delimiter_dict:
        node = split_nodes_delimiter(node, delimiter, delimiter_dict[delimiter])
    node = split_nodes_image(node)
    node = split_nodes_link(node)

    return node
