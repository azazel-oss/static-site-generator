from textnode import (
    TextNode,
    text_type_code,
    text_type_text,
    text_type_italic,
    text_type_image,
    text_type_link,
    text_type_bold,
)
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        node_components = node.text.split(delimiter)
        for i in range(len(node_components)):
            new_node = None
            if node_components[i] == "":
                continue
            if i % 2:
                new_node = TextNode(node_components[i], text_type)
            else:
                new_node = TextNode(node_components[i], text_type_text)
            new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_images(text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        for i in range(len(matches)):
            split_delimiter = f"![{matches[i][0]}]({matches[i][1]})"
            splits = text.split(split_delimiter, 1)
            text = text[len(split_delimiter) + len(splits[0]) :]
            if len(splits[0]) > 0:
                new_nodes.append(TextNode(splits[0], text_type_text))
            new_nodes.append(TextNode(matches[i][0], text_type_image, matches[i][1]))
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        matches = extract_markdown_links(text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        for i in range(len(matches)):
            split_delimiter = f"[{matches[i][0]}]({matches[i][1]})"
            splits = text.split(split_delimiter, 1)
            text = text[len(split_delimiter) + len(splits[0]) :]
            if len(splits[0]) > 0:
                new_nodes.append(TextNode(splits[0], text_type_text))
            new_nodes.append(TextNode(matches[i][0], text_type_link, matches[i][1]))
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    bold_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    italic_nodes = split_nodes_delimiter(bold_nodes, "*", text_type_italic)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", text_type_code)
    images_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(images_nodes)
    return link_nodes
