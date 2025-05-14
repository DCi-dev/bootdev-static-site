import unittest
from markdown_parser import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_heading(self):
        md = """
# Heading

This is a paragraph.

## Subheading

Another paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph.",
                "## Subheading",
                "Another paragraph.",
            ],
        )
def test_markdown_to_blocks_with_mixed_content(self):
        md = """
# Welcome

This is an introduction.

- List item 1
- List item 2

## Section 1

Some text here.

1. Numbered item
2. Another numbered item

> This is a blockquote.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Welcome",
                "This is an introduction.",
                "- List item 1\n- List item 2",
                "## Section 1",
                "Some text here.",
                "1. Numbered item\n2. Another numbered item",
                "> This is a blockquote.",
            ],
        )


if __name__ == "__main__":
    unittest.main()