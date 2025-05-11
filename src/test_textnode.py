import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    """
    Test suite for the TextNode class.
    """

    # Test case 1: Equality with same values (basic)
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # Test case 2: Equality with different text
    def test_eq_different_text(self):
        node = TextNode("This is node 1", TextType.TEXT)
        node2 = TextNode("This is node 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    # Test case 3: Equality with different text_type
    def test_eq_different_type(self):
        node = TextNode("Same text here", TextType.TEXT)
        node2 = TextNode("Same text here", TextType.BOLD)
        self.assertNotEqual(node, node2)

    # Test case 4: Equality with different url
    def test_eq_different_url(self):
        node = TextNode("Link Node", TextType.LINK, "https://example.com/1")
        node2 = TextNode("Link Node", TextType.LINK, "https://example.com/2")
        self.assertNotEqual(node, node2)

    # Test case 5: Equality when one has URL, other is None
    def test_eq_url_none_vs_value(self):
        node = TextNode("Text Node", TextType.TEXT, None)
        node2 = TextNode("Text Node", TextType.TEXT, "https://example.com")
        self.assertNotEqual(node, node2)

    # Test case 6: Equality when both have None URL
    def test_eq_url_both_none(self):
        node = TextNode("Plain text", TextType.TEXT, None)
        node2 = TextNode("Plain text", TextType.TEXT, None)
        self.assertEqual(node, node2)

    # Test case 7: Equality with different types but url is None for both
    def test_eq_different_type_url_none(self):
        node = TextNode("Text content", TextType.TEXT, None)
        node2 = TextNode("Text content", TextType.ITALIC, None)
        self.assertNotEqual(node, node2)


# This allows running the tests directly from this file if needed,
# but the test.sh script is the preferred way for the assignment.
if __name__ == "__main__":
    unittest.main()