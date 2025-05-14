from enum import Enum
import re

def markdown_to_blocks(markdown):
    # Split the markdown into blocks
    blocks = markdown.strip().split('\n\n')
    
    # Process blocks
    cleaned_blocks = []
    for block in blocks:
        # Remove leading/trailing whitespace from the entire block
        cleaned_block = block.strip()
        if cleaned_block:
            # Preserve internal newlines and spaces
            cleaned_blocks.append(cleaned_block)

    return cleaned_blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    # Check for heading
    if re.match(r'^#{1,6}\s', block):
        return BlockType.HEADING
    
    # Check for code block
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    # Check for quote
    if all(line.strip().startswith('>') for line in block.split('\n')):
        return BlockType.QUOTE
    
    # Check for unordered list
    if all(line.strip().startswith('- ') for line in block.split('\n')):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    lines = block.split('\n')
    if all(re.match(r'^\d+\.\s', line.strip()) for line in lines):
        numbers = [int(line.split('.')[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    
    # If none of the above, it's a paragraph
    return BlockType.PARAGRAPH