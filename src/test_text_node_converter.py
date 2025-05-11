# src/test_text_node_converter.py

import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from text_node_converter import text_node_to_html_node # Import the function

class TestTextNodeToHTMLNode(unittest.TestCase):
    """
    Test suite for the text_node_to_html_node conversion function.
    """

    # Test case 1: TextType.TEXT
    def test_text_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode) # Check it returns a LeafNode
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    # Test case 2: TextType.BOLD
    def test_text_node_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, None)

    # Test case 3: TextType.ITALIC
    def test_text_node_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, None)

    # Test case 4: TextType.CODE
    def test_text_node_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")
        self.assertEqual(html_node.props, None)

    # Test case 5: TextType.LINK
    def test_text_node_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        # Adjust expected props based on your props_to_html test experience (single/double quotes)
        # Using double quotes as in the htmlnode.py code provided earlier
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})


    # Test case 6: TextType.IMAGE
    def test_text_node_image(self):
        node = TextNode("An image", TextType.IMAGE, "https://www.boot.dev/image.png")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "") # img tag has empty value
        # Adjust expected props based on your props_to_html test experience (single/double quotes)
        # Using double quotes as in the htmlnode.py code provided earlier
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/image.png", "alt": "An image"})


    # Test case 7: Link with no URL (should raise ValueError)
    def test_text_node_link_no_url(self):
        node = TextNode("Click here", TextType.LINK, None) # URL is None
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Link text node missing URL")

     # Test case 8: Image with no URL (should raise ValueError)
    def test_text_node_image_no_url(self):
        node = TextNode("An image", TextType.IMAGE, None) # URL is None
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual(str(cm.exception), "Image text node missing URL")

    # REMOVE OR COMMENT OUT THIS TEST CASE:
    # def test_text_node_invalid_type(self):
    #     class UnknownType: pass
    #     node = TextNode("Should fail", UnknownType()) # This line causes TypeError in TextNode.__init__
    #     with self.assertRaises(Exception) as cm:
    #         text_node_to_html_node(node)
    #     self.assertIn("Invalid text node type:", str(cm.exception))


# This allows running the tests directly from this file if needed,
# but the test.sh script is the preferred way for the assignment.
if __name__ == "__main__":
    unittest.main()