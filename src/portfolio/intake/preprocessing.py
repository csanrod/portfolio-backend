"""Data preprocessing module for markdown documents.

This module provides utilities to read and parse markdown files,
extracting structured sections and their contents for RAG processing.
"""
import re

from ..utils import setup_logger

logger = setup_logger(__name__)

def read_markdown_file(doc_path: str) -> str | None:
    """Read markdown file from disk with error handling.

    Args:
        doc_path: Absolute or relative path to the markdown file.

    Returns:
        File contents as a string, or None if reading fails.
    """
    try:
        with open(doc_path, "r", encoding="utf-8") as f:
            md = f.read()
        logger.info("✅\tMarkdown read successfully.")
        return md
    except Exception as e:
        logger.error("❌\tMarkdown error.")
        logger.exception(e)
        return None

def parse_sections_and_contents(text: str) -> tuple[list[str], list[str]] | tuple[None, None]:
    """Parse markdown text in O(n) time to extract sections and their contents.

    This function processes markdown headings (H2 and H3) and their associated
    content with the following logic:
    - If H2 has H3 subsections: returns "H2 > H3" paths with H3 contents only
    - If H2 has no H3: returns H2 path with H2 content

    Algorithm:
        1. Single pass to classify all lines: O(n)
        2. Single pass to build structure: O(n)
        Total: O(n)

    Args:
        text: Markdown text to parse.

    Returns:
        tuple[list[str], list[str]] | tuple[None, None]:
            A tuple of (sections, contents) where:
            - sections: List of section paths (e.g., "H2" or "H2 > H3")
            - contents: List of content strings aligned with sections
            Returns (None, None) if sections and contents don't match.

    Example:
        >>> text = "## Section\\nContent here\\n### Subsection\\nMore content"
        >>> sections, contents = parse_sections_and_contents(text)
        >>> sections
        ['Section > Subsection']
    """
    sections = []
    contents = []
    lines = text.split('\n')
    
    # Pre-compile regex patterns for performance (avoid recompilation in loops)
    h2_pattern = re.compile(r'^#{2}\s+(.+)$')
    h3_pattern = re.compile(r'^#{3}\s+(.+)$')
    
    # Pass 1: Classify each line exactly once - O(n)
    line_info = []  # List of (original_line_index, type, title)
    for i, line in enumerate(lines):
        # Skip YAML frontmatter
        if i <= 2 and line.strip() == '---':
            continue
            
        h2_match = h2_pattern.match(line)
        if h2_match:
            line_info.append((i, 'h2', h2_match.group(1).strip()))
            continue
        
        h3_match = h3_pattern.match(line)
        if h3_match:
            line_info.append((i, 'h3', h3_match.group(1).strip()))
            continue
        
        line_info.append((i, 'content', None))
    
    # Pass 2: Build sections and contents - O(n)
    # Key insight: each element is visited exactly once
    i = 0
    m = len(line_info)
    
    while i < m:
        _, line_type, title = line_info[i]
        
        if line_type != 'h2':
            i += 1
            continue
        
        h2_title = title
        i += 1
        
        # Collect all content/H3s until next H2 or end
        h2_children = []  # List of (type, title_or_none, start_idx, end_idx)
        current_start = i
        
        while i < m and line_info[i][1] != 'h2':
            if line_info[i][1] == 'h3':
                # Save any preceding content as part of H2 (will be ignored if H3s exist)
                if i > current_start:
                    h2_children.append(('h2_content', None, current_start, i))
                
                # Track H3 and its content
                h3_title = line_info[i][2]
                i += 1
                h3_start = i
                
                # Find end of H3 content
                while i < m and line_info[i][1] == 'content':
                    i += 1
                
                h2_children.append(('h3', h3_title, h3_start, i))
                current_start = i
            else:
                i += 1
        
        # Capture any remaining content after last H3 or if no H3s
        if i > current_start:
            h2_children.append(('h2_content', None, current_start, i))
        
        # Decide: does H2 have H3 subsections?
        has_h3 = any(child[0] == 'h3' for child in h2_children)
        
        if has_h3:
            # Only emit H3 sections and their contents
            for child_type, child_title, start, end in h2_children:
                if child_type == 'h3':
                    sections.append(f"{h2_title} > {child_title}")
                    
                    # Extract content lines
                    content_lines = [
                        lines[line_info[j][0]] 
                        for j in range(start, end) 
                        if line_info[j][1] == 'content'
                    ]
                    contents.append('\n'.join(content_lines).strip())
        else:
            # No H3s: emit H2 section with all its content
            sections.append(h2_title)
            
            # Extract all content lines
            content_lines = []
            for child_type, _, start, end in h2_children:
                for j in range(start, end):
                    if line_info[j][1] == 'content':
                        content_lines.append(lines[line_info[j][0]])
            
            contents.append('\n'.join(content_lines).strip())
    
    logger.info("✅\tSections and contents parsed.")
    if len(sections) != len(contents):
        logger.error("⛔\tSections and contents do not match.")
        return None, None
    else:
        logger.info("🟢\tSections and contents match.")
    return sections, contents

def get_chunks(sections: list[str], contents: list[str]) -> list[str] | None:
    """Build formatted text chunks for RAG vectorization.

    Combines section paths with their contents in the format "section - content".
    These chunks are ready for embedding generation and vector storage.

    Args:
        sections: List of section paths (e.g., "H2" or "H2 > H3").
        contents: List of content strings, aligned 1:1 with sections.

    Returns:
        List of formatted strings in "section - content" format, or None on error.

    Example:
        >>> sections = ["Experience", "Education"]
        >>> contents = ["5 years in AI", "PhD in CS"]
        >>> get_chunks(sections, contents)
        ['Experience - 5 years in AI', 'Education - PhD in CS']
    """
    chunks = []
    try:
        for section, content in zip(sections, contents):
            chunks.append(f"{section} - {content}")
    except Exception as e:
        logger.error("❌\tChunks error.")
        logger.exception(e)
        return None

    logger.info("✅\tChunks built.")
    return chunks