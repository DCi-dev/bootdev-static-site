# src/htmlnode.py

class HTMLNode:
    """
    Represents a node in an HTML tree structure.

    Attributes:
        tag (str or None): The HTML tag name (e.g., "p", "a", "h1"). Defaults to None.
        value (str or None): The value of the HTML tag (e.g., text content). Defaults to None.
        children (list or None): A list of HTMLNode objects that are children. Defaults to None.
        props (dict or None): A dictionary of key-value pairs for HTML attributes. Defaults to None.
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Generically initializes an HTMLNode.

        All arguments are optional and default to None.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the node and its children to an HTML string.
        This method should be overridden by subclasses.
        """
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        """
        Converts the props dictionary into an HTML attribute string.

        Returns:
            str: A string like ' key1="value1" key2="value2"' or an empty string if no props.
        """
        if self.props is None:
            return ""

        html_attributes = []
        for key, value in self.props.items():
            # Add a leading space before each attribute
            # Use repr(value) to ensure strings with internal quotes are handled correctly
            html_attributes.append(f' {key}={repr(value)}')

        return "".join(html_attributes)
    
    def children_to_html(self):
        if self.tag is None:
            return self.value if self.value is not None else ""
        
        props = self.props_to_html()
        props = " " + props if props else ""
        
        if self.children is None:
            if self.value is None:
                return f"<{self.tag}{props}>"
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        
        children_html = "".join(
            child.to_html() if isinstance(child, HTMLNode) else str(child)
            for child in self.children
        )
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"

    def __repr__(self):
        """
        Provides a string representation of the HTMLNode object for debugging.
        """
        # Using repr() for tag, value, and props provides clearer output,
        # especially if they are strings or None.
        return f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, children={self.children}, props={repr(self.props)})"


class LeafNode(HTMLNode):
    """
    Represents a leaf node in an HTML tree structure (cannot have children).
    ... (rest of LeafNode code - should be unchanged) ...
    """
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("Leaf nodes must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        # Ensure value is not None before accessing it, although __init__ checks this
        # if self.value is None:
        #      raise ValueError("Leaf node with tag requires a value") # Should not happen
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={repr(self.tag)}, value={repr(self.value)}, props={repr(self.props)})"


# --- New ParentNode class ---
class ParentNode(HTMLNode):
    """
    Represents a parent node in an HTML tree structure (can have children).

    Attributes:
        tag (str): The HTML tag name. Required.
        children (list): A list of HTMLNode objects that are children. Required.
        props (dict or None): Dictionary of key-value pairs for attributes. Defaults to None.
    """
    def __init__(self, tag, children, props=None):
        """
        Initializes a ParentNode.

        Args:
            tag (str): The HTML tag name (e.g., "div", "p"). Must not be None.
            children (list): A list of HTMLNode objects. Must not be None or empty.
            props (dict or None, optional): HTML attributes. Defaults to None.
        """
        # Parent nodes require a tag and children, but no value.
        # props is optional.
        if tag is None:
            raise ValueError("Parent nodes must have a tag")
        if children is None or not isinstance(children, list): # Also check it's a list
             raise ValueError("Parent nodes must have a list of children")
        # Note: An empty list of children is explicitly allowed by the prompt example structure
        # if len(children) == 0:
        #     raise ValueError("Parent nodes must have at least one child") # If empty list not allowed


        # Parent nodes don't have a value, pass None to the parent constructor
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Renders the ParentNode and its children recursively as an HTML string.

        If tag is None or children is None/empty, raises ValueError.
        Otherwise, renders the HTML tag with children's HTML content inside.
        """
        # Re-check essential requirements, although __init__ tries to ensure this state
        if self.tag is None:
            raise ValueError("Parent node must have a tag to render")
        if self.children is None or len(self.children) == 0:
            # Check if children is None OR an empty list
            raise ValueError("Parent node must have children to render")


        # Render children first by calling their to_html methods
        children_html = ""
        for child in self.children:
            if not isinstance(child, HTMLNode): # Optional check for list contents
                 raise TypeError("Parent node children must be HTMLNode objects")
            children_html += child.to_html()

        # Get formatted properties string
        props_html = self.props_to_html()

        # Construct the full HTML string: <tag attributes>children_html</tag>
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

    def __repr__(self):
        """
        Provides a string representation specific to ParentNode.
        """
        # Using repr() for tag and props provides clearer output
        return f"ParentNode(tag={repr(self.tag)}, children={self.children}, props={repr(self.props)})"