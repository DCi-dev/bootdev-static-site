# src/text_node_converter.py

from textnode import TextNode, TextType # Import TextNode and TextType
from htmlnode import LeafNode           # Import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Converts a TextNode object to a LeafNode object based on its type.

    Args:
        text_node: The TextNode object to convert.

    Returns:
        A LeafNode object representing the HTML equivalent of the TextNode.

    Raises:
        Exception: If the TextNode has an invalid or unhandled TextType.
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINK:
        # Link needs an 'a' tag, the text as value, and the url as the 'href' prop
        # Ensure url is not None, though TextNode allows it, links require it
        if text_node.url is None:
             raise ValueError("Link text node missing URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        # Image needs an 'img' tag, empty string value, and url as 'src' prop
        # The text becomes the 'alt' prop
        # Ensure url is not None, though TextNode allows it, images require it
        if text_node.url is None:
             raise ValueError("Image text node missing URL")
        # Although TextNode takes 'text' as content, for an <img> tag
        # the text is actually the alt attribute, and the value is empty.
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    # If the text_type is none of the above
    raise Exception(f"Invalid text node type: {text_node.text_type}")
