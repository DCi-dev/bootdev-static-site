import unittest
from markdown_parser import markdown_to_blocks, BlockType, block_to_block_type

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
        md = """# Welcome

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
            ],)


    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "### This is a level 3 heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\ndef hello_world():\n    print('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> It spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list(self):
        block = "1. First item\n3. Third item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_content(self):
        block = "This is a paragraph with a - dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()