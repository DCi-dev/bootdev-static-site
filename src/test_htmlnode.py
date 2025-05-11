# src/test_htmlnode.py

import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode # Import ParentNode

# Keep your existing TestHTMLNode class for testing HTMLNode's methods (like props_to_html)
class TestHTMLNode(unittest.TestCase):
    """
    Test suite for the base HTMLNode class (primarily testing props_to_html).
    """
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.google.com", "target": "_blank"}
        )
        # >>> FIX: Expect single quotes based on error output <<<
        expected_props_html = " href='https://www.google.com' target='_blank'" # Changed " to '
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_props_to_html_single_prop(self):
        node = HTMLNode(
            "img",
            "",
            None,
            {"src": "/images/logo.png"}
        )
        # >>> FIX: Expect single quotes based on error output <<<
        expected_props_html = " src='/images/logo.png'" # Changed " to '
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_props_to_html_no_props(self):
        node = HTMLNode(
            "p",
            "Just a paragraph.",
            None,
            None
        )
        expected_props_html = ""
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_props_to_html_empty_props_dict(self):
         node = HTMLNode(
             "div",
             "Empty props dict",
             None,
             {}
         )
         expected_props_html = ""
         self.assertEqual(node.props_to_html(), expected_props_html)


# Keep existing TestLeafNode class...
class TestLeafNode(unittest.TestCase):
    """
    Test suite for the LeafNode class.
    """

   # Test case 1: Basic paragraph tag
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    # Test case 2: Anchor tag with href property
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href": "https://www.google.com"})
        # This is the line that likely has the typo or copy/paste issue
        # Ensure this string literal is correctly opened and closed
        expected_html = "<a href='https://www.google.com'>Click here</a>" # <--- Verify this line
        self.assertEqual(node.to_html(), expected_html) # <--- Line 69

    # Test case 3: Heading tag without properties
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")