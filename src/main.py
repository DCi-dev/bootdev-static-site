import sys
from textnode import TextNode, TextType

def main():
  """
  Creates and prints a TextNode object for demonstration.
  """
  # Create a TextNode object with dummy values
  dummy_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

  # Print the object (which will use the __repr__ method)
  print(dummy_node)

  # Example of another node type
  another_node = TextNode("This is just plain text", TextType.TEXT)
  print(another_node)

  # Example with no URL
  bold_node = TextNode("This is bold text", TextType.BOLD)
  print(bold_node)

if __name__ == "__main__":
  # For this assignment, we just want to run the new main()
  main()