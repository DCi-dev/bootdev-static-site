def markdown_to_blocks(markdown):
    # Split the markdown into blocks
    blocks = markdown.split('\n\n')
    
    # Process blocks
    cleaned_blocks = []
    in_code_block = False
    current_block = []

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block.startswith("```") and stripped_block.endswith("```"):
            # Single block code
            cleaned_blocks.append(stripped_block)
        elif stripped_block.startswith("```") or stripped_block.endswith("```"):
            # Start or end of a multi-block code
            in_code_block = not in_code_block
            current_block.append(stripped_block)
            if not in_code_block:
                cleaned_blocks.append("\n".join(current_block))
                current_block = []
        elif in_code_block:
            # Inside a code block
            current_block.append(stripped_block)
        elif stripped_block:
            # Regular block
            cleaned_blocks.append(stripped_block)

    # Add any remaining code block
    if current_block:
        cleaned_blocks.append("\n".join(current_block))

    return cleaned_blocks