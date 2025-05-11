# src/textnode.py

from enum import Enum
# Add this import: textnode.py needs to know about HTMLNode
from htmlnode import HTMLNode


# Define the TextType enumeration
class TextType(Enum):
    """
    Enumeration for different types of inline text nodes.
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

# Define the TextNode class
class TextNode:
    """
    Represents an inline text node with content, type, and optional URL.
    """
    def __init__(self, text, text_type, url=None):
        """
        Initializes a TextNode object.

        Args:
            text (str): The text content of the node.
            text_type (TextType): The type of the text node (an enum member).
            url (str, optional): The URL for links or images. Defaults to None.
        """
        if not isinstance(text, str):
             raise TypeError("text must be a string")
        if not isinstance(text_type, TextType):
             raise TypeError("text_type must be a TextType enum member")
        if url is not None and not isinstance(url, str):
             raise TypeError("url must be a string or None")


        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """
        Compares two TextNode objects for equality.

        Returns:
            bool: True if all properties (text, text_type, url) are equal, False otherwise.
        """
        if not isinstance(other, TextNode):
            return NotImplemented

        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        """
        Provides a string representation of the TextNode object.
        """
        return f"TextNode({repr(self.text)}, {self.text_type.value}, {repr(self.url)})"


# --- LeafNode class (moved to htmlnode.py in best practice, but keeping here for now based on error location) ---
# NOTE: It's generally better practice to have each major class in its own file.
# The LeafNode definition should probably be in htmlnode.py with HTMLNode,
# but the error message indicates it was found in textnode.py line 66.
# So, for now, we fix the import assuming LeafNode is *in* textnode.py as per the traceback.
class LeafNode(HTMLNode): # This line needs HTMLNode to be defined
    """
    Represents a leaf node in an HTML tree structure (cannot have children).
    ... (rest of LeafNode definition) ...
    """
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("Leaf nodes must have a value")

        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={repr(self.tag)}, value={repr(self.value)}, props={repr(self.props)})"


# Example usage (can be removed or commented out if not needed directly in textnode.py)
# if __name__ == "__main__":
#     node1 = TextNode("This is some text", TextType.TEXT)
#     print(node1)
#
#     leaf1 = LeafNode("p", "A paragraph")
#     print(leaf1) # Will now work after importing HTMLNode