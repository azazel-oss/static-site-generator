from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value) -> bool:
        if self.text != value.text:
            return False
        if self.text_type != value.text_type:
            return False
        if self.url != value.url:
            return False
        return True

    def __repr__(self) -> str:
        if self.url:
            return f"TextNode({self.text}, {self.text_type}, {self.url})"
        return f"TextNode({self.text}, {self.text_type})"


def textnode_to_htmlnode(textnode: TextNode):
    if textnode.text_type == text_type_text:
        return LeafNode(tag=None, value=textnode.text)
    if textnode.text_type == text_type_bold:
        return LeafNode(tag="b", value=textnode.text)
    if textnode.text_type == text_type_italic:
        return LeafNode(tag="i", value=textnode.text)
    if textnode.text_type == text_type_code:
        return LeafNode(tag="code", value=textnode.text)
    if textnode.text_type == text_type_link:
        return LeafNode(tag="a", value=textnode.text, props={"href": textnode.url})
    if textnode.text_type == text_type_image:
        return LeafNode(
            tag="img", value=None, props={"src": textnode.url, "alt": textnode.text}
        )
    raise ValueError(f"Invalid text type: {textnode.text_type}")
