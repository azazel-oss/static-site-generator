import re
from htmlnode import LeafNode, ParentNode
from textnode import textnode_to_htmlnode
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip() == "":
            continue
        result.append(block.strip())
    return result


def block_to_block_type(block):
    if re.search(r"^#+", block):
        return block_type_heading
    if re.search(r"^```[\s\S]*```$", block):
        return block_type_code
    if block.startswith("> "):
        for line in block.split("\n"):
            if line.strip().startswith("> "):
                continue
            else:
                return block_type_paragraph
        return block_type_quote
    if block.startswith("- "):
        for line in block.split("\n"):
            if re.search(r"^\s*-\s\S*", line):
                continue
            else:
                return block_type_paragraph
        return block_type_unordered_list
    if block.startswith("* "):
        for line in block.split("\n"):
            if re.search(r"^\*\s\S*", line):
                continue
            else:
                return block_type_paragraph
        return block_type_unordered_list
    if block.startswith("1. "):
        i = 1
        for line in block.split("\n"):
            if not line.strip().startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    return block_type_paragraph


def paragraph_to_htmlnode(block):
    new_text = []
    lines = block.split("\n")
    for line in lines:
        new_text.append(line.strip())
    nodes = text_to_textnodes(" ".join(new_text))
    children = []
    for node in nodes:
        children.append(textnode_to_htmlnode(node))
    parent = ParentNode(tag="p", children=children)
    return parent


def heading_to_htmlnode(block):
    i = 0
    for char in block:
        if char == "#":
            i += 1
        else:
            break
    heading = LeafNode(tag=f"h{i}", value=block.strip("#").strip())
    return heading


def code_to_htmlnode(block):
    code = LeafNode(tag="code", value=block)
    parent = ParentNode(tag="pre", children=[code])
    return parent


def quote_to_htmlnode(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.strip().strip("> "))
    quote = LeafNode(tag="blockquote", value=" ".join(new_lines))
    return quote


def ordered_list_to_htmlnode(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_nodes = text_to_textnodes(line.strip()[2:].strip())
        something = []
        for ele in line_nodes:
            something.append(textnode_to_htmlnode(ele))
        list_item = ParentNode(tag="li", children=something)
        children.append(list_item)
    parent = ParentNode(tag="ol", children=children)
    return parent


def unordered_list_to_htmlnode(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        line_nodes = text_to_textnodes(line.strip("* ").strip("- "))
        something = []
        for ele in line_nodes:
            something.append(textnode_to_htmlnode(ele))
        list_item = ParentNode(tag="li", children=something)
        children.append(list_item)
    parent = ParentNode(tag="ul", children=children)
    return parent


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_with_type = []
    for block in blocks:
        block_type = block_to_block_type(block)
        blocks_with_type.append((block, block_type))
    children_nodes = []
    for ele in blocks_with_type:
        block = ele[0]
        block_type = ele[1]
        if block_type == block_type_paragraph:
            children_nodes.append(paragraph_to_htmlnode(block))
        if block_type == block_type_code:
            children_nodes.append(code_to_htmlnode(block))
        if block_type == block_type_quote:
            children_nodes.append(quote_to_htmlnode(block))
        if block_type == block_type_heading:
            children_nodes.append(heading_to_htmlnode(block))
        if block_type == block_type_unordered_list:
            children_nodes.append(unordered_list_to_htmlnode(block))
        if block_type == block_type_ordered_list:
            children_nodes.append(ordered_list_to_htmlnode(block))

    parent = ParentNode(tag="div", children=children_nodes)
    return parent
