"""
Discord-specific utility functions for message processing.
"""

import re
from typing import List, Optional, Tuple, NamedTuple


class SyntaxBoundary(NamedTuple):
    """Represents a paired syntax boundary in the text."""

    start: int
    end: int
    name: str
    opening: str
    closing: str


class DiscordTextSplitter:
    """
    A utility class for splitting Discord text while preserving formatting.

    Args:
        max_chars (int): Maximum characters per chunk (default: 2000)
        preserve_formatting (bool): Whether to preserve Discord formatting (default: True)
        verbose (bool): Whether to print warnings for forced splits (default: False)
    """

    # Discord paired syntaxes (opening, closing, name) - order matters for precedence
    PAIRED_SYNTAXES = [
        ("```", "```", "code_block"),
        ("||", "||", "spoiler"),
        ("~~", "~~", "strikethrough"),
        ("__", "__", "underline"),
        ("**", "**", "bold"),
        ("`", "`", "inline_code"),
        ("*", "*", "italic_asterisk"),
        ("_", "_", "italic_underscore"),
    ]

    # Line-start formats (regex pattern, name)
    LINE_START_FORMATS = [
        (r"^#{1,6}\s", "heading"),
        (r"^>\s", "blockquote"),
        (r"^[-*+]\s", "unordered_list"),
        (r"^\d+\.\s", "ordered_list"),
    ]

    def __init__(
        self,
        max_chars: int = 2000,
        preserve_formatting: bool = True,
        verbose: bool = False,
    ):
        self.max_chars = max_chars
        self.preserve_formatting = preserve_formatting
        self.verbose = verbose

        if max_chars <= 0:
            raise ValueError("max_chars must be positive")

    def split(self, text: str) -> List[str]:
        """
        Split text into chunks while preserving Discord formatting.

        Args:
            text (str): The text to split

        Returns:
            List[str]: List of text chunks
        """
        if not text or not text.strip():
            return []

        if len(text) <= self.max_chars:
            return [text]

        if not self.preserve_formatting:
            return self._simple_split(text)

        return self._smart_split(text)

    def _simple_split(self, text: str) -> List[str]:
        """Simple splitting without format preservation."""
        chunks = []
        for i in range(0, len(text), self.max_chars):
            chunk = text[i : i + self.max_chars]
            if chunk.strip():
                chunks.append(chunk.strip())
        return chunks

    def _smart_split(self, text: str) -> List[str]:
        """Smart splitting with Discord format preservation."""
        chunks = []
        remaining = text

        while len(remaining) > self.max_chars:
            split_point = self._find_safe_split_point(remaining, self.max_chars)

            if split_point is None or split_point <= 0:
                split_point = self.max_chars
                if self.verbose:
                    print(f"Warning: Forced split at position {split_point}")

            chunk = remaining[:split_point].rstrip()
            if chunk:
                chunks.append(chunk)

            remaining = remaining[split_point:].lstrip()

        if remaining.strip():
            chunks.append(remaining.strip())

        return chunks

    def _find_safe_split_point(self, text: str, target_pos: int) -> Optional[int]:
        """Find a safe split point considering paired syntaxes and line-start formats."""
        if target_pos >= len(text):
            return len(text)

        paired_boundaries = self._find_all_paired_syntaxes(text)
        line_start_formats = self._find_line_start_formats(text)

        # Check for crossing syntax
        crossing_syntax = None
        for boundary in paired_boundaries:
            if boundary.start < target_pos < boundary.end:
                crossing_syntax = boundary
                break

        if crossing_syntax:
            syntax_length = crossing_syntax.end - crossing_syntax.start
            if syntax_length > self.max_chars:
                if self.verbose:
                    print(
                        f"Warning: {crossing_syntax.name} syntax is {syntax_length} characters, "
                        f"exceeding limit of {self.max_chars}. Forcing split."
                    )
                return target_pos

            if crossing_syntax.end <= self.max_chars:
                return self._find_best_split_before_position(
                    text, crossing_syntax.end, paired_boundaries, line_start_formats
                )
            else:
                return self._find_best_split_before_position(
                    text, crossing_syntax.start, paired_boundaries, line_start_formats
                )

        return self._find_best_split_before_position(
            text, target_pos, paired_boundaries, line_start_formats
        )

    def _find_all_paired_syntaxes(self, text: str) -> List[SyntaxBoundary]:
        """Find all paired syntax boundaries, handling nested cases."""
        all_boundaries = []

        for opening, closing, name in self.PAIRED_SYNTAXES:
            boundaries = self._find_paired_syntax(text, opening, closing, name)
            all_boundaries.extend(boundaries)

        all_boundaries.sort(key=lambda x: (x.start, -x.end))

        # Remove overlapping boundaries
        filtered_boundaries = []
        for boundary in all_boundaries:
            is_overlapped = any(
                (
                    existing.start <= boundary.start < existing.end
                    or existing.start < boundary.end <= existing.end
                    or (
                        boundary.start <= existing.start
                        and boundary.end >= existing.end
                    )
                )
                for existing in filtered_boundaries
            )

            if not is_overlapped:
                filtered_boundaries.append(boundary)

        return sorted(filtered_boundaries, key=lambda x: x.start)

    def _find_paired_syntax(
        self, text: str, opening: str, closing: str, name: str
    ) -> List[SyntaxBoundary]:
        """Find all instances of a specific paired syntax."""
        boundaries = []
        pos = 0

        while pos < len(text):
            open_pos = text.find(opening, pos)
            if open_pos == -1:
                break

            close_start = open_pos + len(opening)
            close_pos = text.find(closing, close_start)
            if close_pos == -1:
                pos = open_pos + 1
                continue

            close_end = close_pos + len(closing)
            boundaries.append(
                SyntaxBoundary(open_pos, close_end, name, opening, closing)
            )
            pos = close_end

        return boundaries

    def _find_line_start_formats(self, text: str) -> List[Tuple[int, str]]:
        """Find all line-start format positions."""
        line_formats = []
        lines = text.split("\n")
        pos = 0

        for line in lines:
            for pattern, name in self.LINE_START_FORMATS:
                if re.match(pattern, line):
                    line_formats.append((pos, name))
                    break
            pos += len(line) + 1

        return line_formats

    def _find_best_split_before_position(
        self,
        text: str,
        max_pos: int,
        paired_boundaries: List[SyntaxBoundary],
        line_start_formats: List[Tuple[int, str]],
    ) -> int:
        """Find the best split point before max_pos."""
        if max_pos <= 0:
            return 0

        # Try sentence boundaries
        for i in range(max_pos - 1, -1, -1):
            if text[i] in ".!?":
                split_pos = i + 1
                if self._is_position_safe(
                    split_pos, paired_boundaries, line_start_formats, text
                ):
                    return split_pos

        # Try line boundaries
        current_pos = 0
        for line_start, line_end in self._find_line_boundaries(text):
            if line_end <= max_pos:
                if self._is_position_safe(
                    line_end, paired_boundaries, line_start_formats, text
                ):
                    current_pos = line_end
            else:
                break

        if current_pos > 0:
            return current_pos

        # Try word boundaries
        for i in range(max_pos - 1, -1, -1):
            if text[i].isspace():
                split_pos = i + 1
                if self._is_position_safe(
                    split_pos, paired_boundaries, line_start_formats, text
                ):
                    return split_pos

        return max_pos

    def _find_line_boundaries(self, text: str) -> List[Tuple[int, int]]:
        """Find line boundaries in the text."""
        lines = []
        start = 0

        while start < len(text):
            end = text.find("\n", start)
            if end == -1:
                end = len(text)
            else:
                end += 1

            lines.append((start, end))
            start = end

        return lines

    def _is_position_safe(
        self,
        pos: int,
        paired_boundaries: List[SyntaxBoundary],
        line_start_formats: List[Tuple[int, str]],
        text: str,
    ) -> bool:
        """Check if a position is safe to split at."""
        # Check if position is inside any paired syntax
        for boundary in paired_boundaries:
            if boundary.start < pos < boundary.end:
                return False

        # Check line-start formats
        if pos < len(text):
            next_line_start = pos
            while next_line_start < len(text) and text[next_line_start] in " \t":
                next_line_start += 1

            for format_pos, format_name in line_start_formats:
                if format_pos >= pos and format_pos <= next_line_start + 10:
                    if pos > format_pos:
                        return False

        return True


def split_discord_text(
    text: str,
    max_chars: int = 2000,
    preserve_formatting: bool = True,
    verbose: bool = False,
) -> List[str]:
    """
    Split Discord text into chunks while preserving formatting.

    Args:
        text (str): The text to split
        max_chars (int): Maximum characters per chunk (default: 2000)
        preserve_formatting (bool): Whether to preserve Discord formatting (default: True)
        verbose (bool): Whether to print warnings (default: False)

    Returns:
        List[str]: List of text chunks

    Example:
        >>> chunks = split_discord_text("Your very long text here...", max_chars=2000)
        >>> for i, chunk in enumerate(chunks, 1):
        ...     print(f"Chunk {i}: {len(chunk)} characters")
    """
    splitter = DiscordTextSplitter(
        max_chars=max_chars, preserve_formatting=preserve_formatting, verbose=verbose
    )
    return splitter.split(text)


def split_message(
    text: str, max_length: int = 2000, preserve_syntax: bool = True
) -> List[str]:
    """
    Split a message into chunks that fit Discord's character limit.

    This function uses the discord_text_splitter module to maintain Discord formatting
    elements like **bold**, `code`, ``` code blocks, # headings, > quotes, etc.

    Args:
        text: The text to split
        max_length: Maximum characters per message (default 2000 for Discord)
        preserve_syntax: Whether to use syntax-aware chunking (default True)

    Returns:
        List of message chunks with preserved formatting (if preserve_syntax=True)
    """
    # Use the discord_text_splitter for syntax-aware chunking
    if preserve_syntax:
        return split_discord_text(text, max_chars=max_length, preserve_formatting=True)

    # Fallback to legacy implementation when syntax preservation is disabled
    return _split_message_legacy(text, max_length)


def _split_message_legacy(text: str, max_length: int = 2000) -> List[str]:
    """
    Legacy message splitting implementation without syntax awareness.

    This is the original implementation kept for fallback purposes and when
    syntax preservation is explicitly disabled.

    Args:
        text: The text to split
        max_length: Maximum characters per message (default 2000 for Discord)

    Returns:
        List of message chunks
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    # Split by lines first to preserve formatting
    lines = text.split("\n")

    for line in lines:
        # If a single line is too long, split it by words
        if len(line) > max_length:
            words = line.split(" ")
            current_line = ""

            for word in words:
                # If a single word is too long, split it by characters
                if len(word) > max_length:
                    if current_line:
                        if len(current_chunk + current_line) <= max_length:
                            current_chunk += current_line + "\n"
                        else:
                            chunks.append(current_chunk.rstrip())
                            current_chunk = current_line + "\n"
                        current_line = ""

                    # Split the long word
                    for i in range(0, len(word), max_length - 10):  # Leave some buffer
                        word_chunk = word[i : i + max_length - 10]
                        if len(current_chunk + word_chunk) <= max_length:
                            current_chunk += word_chunk
                        else:
                            chunks.append(current_chunk.rstrip())
                            current_chunk = word_chunk
                else:
                    # Check if adding this word would exceed the limit
                    test_line = current_line + (" " if current_line else "") + word
                    if len(test_line) <= max_length:
                        current_line = test_line
                    else:
                        # Add current line to chunk and start new line
                        if current_line:
                            if len(current_chunk + current_line + "\n") <= max_length:
                                current_chunk += current_line + "\n"
                            else:
                                chunks.append(current_chunk.rstrip())
                                current_chunk = current_line + "\n"
                        current_line = word

            # Add remaining line
            if current_line:
                if len(current_chunk + current_line + "\n") <= max_length:
                    current_chunk += current_line + "\n"
                else:
                    chunks.append(current_chunk.rstrip())
                    current_chunk = current_line + "\n"
        else:
            # Check if adding this line would exceed the limit
            test_chunk = current_chunk + line + "\n"
            if len(test_chunk) <= max_length:
                current_chunk = test_chunk
            else:
                # Start new chunk
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                current_chunk = line + "\n"

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.rstrip())

    return chunks if chunks else [text[:max_length]]
