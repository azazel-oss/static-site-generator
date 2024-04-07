class HTMLNode:
    def __init__(
        self, tag=None, value=None, children=None, props: None | dict = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            representation = ""
            for key, value in self.props.items():
                representation += f' {key}="{value}"'
            return representation
        else:
            return ""

    def __repr__(self):
        return f"HTMLNode({self.tag, self.value, self.children, self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props: None | dict = None) -> None:
        super().__init__(tag=tag, value=value, props=props, children=None)

    def to_html(self):
        if not self.tag:
            return self.value
        if not self.value:
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props: None | dict = None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid element: No tag provided")

        if not self.children:
            raise ValueError("Invalid parent element: No children")

        children_html = ""

        for element in self.children:
            children_html += element.to_html()

        return f"<{self.tag}>{children_html}</{self.tag}>"
