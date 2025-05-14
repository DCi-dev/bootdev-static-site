from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

def markdown_to_blocks(markdown):
    blocks = []
    current_block = []
    in_code_block = False

    for line in markdown.split('\n'):
        if line.strip() == '```':
            if in_code_block:
                current_block.append(line)
                blocks.append('\n'.join(current_block))
                current_block = []
                in_code_block = False
            else:
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
                current_block.append(line)
                in_code_block = True
        elif in_code_block:
            current_block.append(line)
        elif line.strip() == '' and not in_code_block:
            if current_block:
                blocks.append('\n'.join(current_block))
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append('\n'.join(current_block))

    return [block.strip() for block in blocks if block.strip()]


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif re.match(r'^#{1,6}\s', block):
        return BlockType.HEADING
    elif all(line.strip().startswith('>') for line in block.split('\n')):
        return BlockType.QUOTE
    elif all(line.strip().startswith('- ') for line in block.split('\n')):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r'^\d+\.\s', line.strip()) for line in block.split('\n')):
        # Check if the numbers are in ascending order
        numbers = [int(line.split('.')[0]) for line in block.split('\n')]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child = block_to_html_node(block, block_type)
        children.append(child)
    return ParentNode("div", children)

def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", text_to_children(block.replace('\n', ' ')))
    elif block_type == BlockType.HEADING:
        level = len(block.split()[0])  # Count the number of '#' symbols
        return ParentNode(f"h{level}", text_to_children(block.lstrip("#").strip()))
    elif block_type == BlockType.CODE:
        # Remove the first and last line (which contain ```)
        code_content = '\n'.join(block.split('\n')[1:-1])
        return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])])
    elif block_type == BlockType.QUOTE:
        return ParentNode("blockquote", text_to_children(block.replace('> ', '').replace('\n', ' ').strip()))
    elif block_type == BlockType.UNORDERED_LIST:
        items = [ParentNode("li", text_to_children(item.lstrip("- ").strip())) for item in block.split("\n")]
        return ParentNode("ul", items)
    elif block_type == BlockType.ORDERED_LIST:
        items = [ParentNode("li", text_to_children(item.split(". ", 1)[1].strip())) for item in block.split("\n")]
        return ParentNode("ol", items)
    else:
        raise ValueError(f"Invalid block type: {block_type}")

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return ParentNode("b", [LeafNode(None, text_node.text)])
    elif text_node.text_type == TextType.ITALIC:
        return ParentNode("i", [LeafNode(None, text_node.text)])
    elif text_node.text_type == TextType.CODE:
        return ParentNode("code", [LeafNode(None, text_node.text)])
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text node type: {text_node.text_type}")

def text_to_children(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return [text_node_to_html_node(node) for node in nodes]


def split_nodes_image(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        current_text = node.text
        for alt_text, url in images:
            parts = current_text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            current_text = parts[1] if len(parts) > 1 else ""
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(nodes):
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        current_text = node.text
        for text, url in links:
            parts = current_text.split(f"[{text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            current_text = parts[1] if len(parts) > 1 else ""
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes