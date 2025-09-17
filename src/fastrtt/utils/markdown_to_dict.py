#!/usr/bin/env python3
"""
Markdown to Dictionary Converter

This script converts a markdown document into a dictionary where each section heading
becomes a key with a value containing:
- title: the section heading text
- content: the text content under that heading
- parent: the immediate parent section heading (based on heading level hierarchy)
"""

import json
import re
from typing import Dict, Optional


class MarkdownParser:
    def __init__(self):
        self.sections = {}
        self.heading_stack = []  # Stack to track parent headings at each level

    def parse_file(self, file_path: str) -> Dict:
        """Parse a markdown file and return the dictionary structure."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return self.parse_content(content)

    def parse_content(self, content: str) -> Dict:
        """Parse markdown content and return the dictionary structure."""
        lines = content.split("\n")

        current_section = None
        current_content = []

        for line in lines:
            heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)

            if heading_match:
                # Save previous section content if exists
                if current_section:
                    self.sections[current_section]["content"] = "\n".join(
                        current_content
                    ).strip()

                # Process new heading
                heading_level = len(heading_match.group(1))
                heading_text = heading_match.group(2).strip()

                # Update heading stack for parent tracking
                self._update_heading_stack(heading_level, heading_text)

                # Find parent heading
                parent = self._find_parent(heading_level)

                # Create section entry
                current_section = heading_text
                self.sections[current_section] = {
                    "title": heading_text,
                    "content": "",
                    "parent": parent,
                }

                # Reset content for new section
                current_content = []
            else:
                # Accumulate content for current section
                if current_section is not None:
                    current_content.append(line)

        # Save the last section's content
        if current_section:
            self.sections[current_section]["content"] = "\n".join(
                current_content
            ).strip()

        return self.sections

    def _update_heading_stack(self, level: int, heading_text: str):
        """Update the heading stack to track hierarchy."""
        # Ensure stack has enough levels
        while len(self.heading_stack) < level:
            self.heading_stack.append(None)

        # Set current level and clear deeper levels
        self.heading_stack[level - 1] = heading_text
        self.heading_stack = self.heading_stack[:level]

    def _find_parent(self, current_level: int) -> Optional[str]:
        """Find the parent heading for the current heading level."""
        if current_level <= 1:
            return None

        # Look for parent at level - 1
        parent_level = current_level - 1
        if parent_level <= len(self.heading_stack):
            return self.heading_stack[parent_level - 1]

        return None

    def to_json(self, indent: int = 2) -> str:
        """Convert the sections dictionary to JSON format."""
        return json.dumps(self.sections, indent=indent, ensure_ascii=False)

    def print_structure(self):
        """Print a summary of the document structure."""
        print("Document Structure:")
        print("=" * 50)

        for title, data in self.sections.items():
            parent_text = f" (parent: {data['parent']})" if data["parent"] else ""
            content_preview = (
                data["content"][:100].replace("\n", " ") + "..."
                if len(data["content"]) > 100
                else data["content"].replace("\n", " ")
            )

            print(f"Title: {title}{parent_text}")
            print(f"Content: {content_preview}")
            print("-" * 30)


def main():
    """Main function to demonstrate usage."""
    import os
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        raise ValueError("Please provide a markdown file path as an argument.")

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        print(f"Usage: {sys.argv[0]} [markdown_file]")
        return

    # Parse the document
    parser = MarkdownParser()
    sections_dict = parser.parse_file(file_path)

    # Print structure summary
    parser.print_structure()

    # Optionally save to JSON file
    output_file = file_path.replace(".md", "_sections.json")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(parser.to_json())

    print(f"\nSections dictionary saved to: {output_file}")
    print(f"Total sections parsed: {len(sections_dict)}")


if __name__ == "__main__":
    main()
