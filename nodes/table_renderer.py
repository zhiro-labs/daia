"""
Table image rendering node for the async flow pipeline.
"""

import re
import io
from typing import Dict, Any, List
from pocketflow import AsyncNode
from PIL import Image, ImageDraw, ImageFont


class TableImageRenderer(AsyncNode):
    """Node to render markdown tables as images"""

    async def prep_async(self, shared):
        extracted_tables = shared.get("extracted_tables", [])
        llm_response = shared.get("llm_response", "")
        message_id = shared.get("message_id", "")

        print("🖼️ [TableImageRenderer] Preparing to render tables as images")
        print(f"🔍 [TableImageRenderer] Found {len(extracted_tables)} extracted tables")
        print(
            f"📝 [TableImageRenderer] Response length: {len(llm_response)} characters"
        )

        for i, table in enumerate(extracted_tables):
            print(
                f"📊 [TableImageRenderer] Table {i + 1}: valid={table.get('parsed', {}).get('valid', False)}"
            )

        return {
            "extracted_tables": extracted_tables,
            "llm_response": llm_response,
            "message_id": message_id,
        }

    async def exec_async(self, prep_res):
        print(
            f"🎨 [TableImageRenderer] Rendering {len(prep_res['extracted_tables'])} table(s)"
        )

        if not prep_res["extracted_tables"]:
            print("⚠️ [TableImageRenderer] No tables to render")
            return {"images": [], "response_without_tables": prep_res["llm_response"]}

        rendered_images = []
        response_text = prep_res["llm_response"]

        # Replace tables with placeholders in response text
        for table in prep_res["extracted_tables"]:
            table_index = table.get("index", "unknown")
            table_count = (
                table_index + 1 if isinstance(table_index, int) else table_index
            )

            print(f"🔄 [TableImageRenderer] Processing table {table_count}")

            if table["parsed"]["valid"]:
                try:
                    parsed_data = table["parsed"]
                    headers = parsed_data.get("headers", [])
                    rows = parsed_data.get("rows", [])

                    print(
                        f"📋 [TableImageRenderer] Table {table_count}: {len(headers)} headers, {len(rows)} rows"
                    )
                    print(f"📋 [TableImageRenderer] Headers: {headers}")

                    # Render table as image
                    print(
                        f"🎨 [TableImageRenderer] Starting image rendering for table {table_count}"
                    )
                    image_buffer = self._render_table_image(table["parsed"])

                    rendered_images.append(
                        {
                            "index": table["index"],
                            "buffer": image_buffer,
                            "filename": f"table_{table['index'] + 1}.png",
                        }
                    )

                    # Replace table in response text with placeholder
                    table_raw_text = table.get("raw_text", "")
                    if table_raw_text and table_raw_text in response_text:
                        placeholder = f"> `[daia_replaced_table_{prep_res['message_id']}_{table_count}_as_image]`"
                        response_text = response_text.replace(
                            table_raw_text, placeholder
                        )
                        print(
                            f"🔄 [TableImageRenderer] Replaced table {table_count} with placeholder"
                        )

                    print(
                        f"✅ [TableImageRenderer] Successfully rendered table {table_count}"
                    )

                except Exception as e:
                    print(
                        f"❌ [TableImageRenderer] Failed to render table {table_count}: {e}"
                    )
                    print(
                        f"🔍 [TableImageRenderer] Table data: {table.get('parsed', {})}"
                    )
            else:
                print(f"⚠️ [TableImageRenderer] Skipping invalid table {table_count}")

        # Clean up response text (remove extra newlines)
        response_text = re.sub(r"\n\s*\n\s*\n", "\n\n", response_text).strip()

        return {
            "images": rendered_images,
            "response_without_tables": response_text,
            "rendered_count": len(rendered_images),
        }

    def _get_font(self, size: int, bold: bool = False):
        """Load Noto Sans font (regular or bold)."""
        try:
            # Choose the appropriate font file based on bold parameter
            if bold:
                font_path = "assets/fonts/03_NotoSansCJK-OTC/NotoSansCJK-Bold.ttc"
            else:
                font_path = "assets/fonts/03_NotoSansCJK-OTC/NotoSansCJK-Regular.ttc"

            return ImageFont.truetype(font_path, size)
        except Exception as e:
            # Fallback to old path for backward compatibility
            try:
                font_path = "assets/fonts/NotoSansCJK.ttc"
                return ImageFont.truetype(font_path, size)
            except Exception as e2:
                print(
                    f"⚠️ [TableImageRenderer] Could not load font from either path: {e}, {e2}, using default"
                )
                return ImageFont.load_default()

    def _parse_text_formatting(self, text: str):
        """Parse text with **bold** formatting into segments, handling various patterns."""
        import re

        segments = []

        # More flexible pattern that handles:
        # - **text** (standard bold)
        # - **text at start
        # - text** at end
        # - **text in middle**
        parts = re.split(r"(\*\*[^*]*?\*\*|\*\*[^*]*$|^[^*]*\*\*|\*\*[^*]*)", text)

        for part in parts:
            if not part:
                continue

            # Handle different bold patterns
            if part.startswith("**") and part.endswith("**") and len(part) > 4:
                # Standard **bold** text
                segments.append(("bold", part[2:-2]))
            elif part.startswith("**") and len(part) > 2:
                # **text at start (treat as bold)
                segments.append(("bold", part[2:]))
            elif part.endswith("**") and len(part) > 2:
                # text** at end (treat as bold)
                segments.append(("bold", part[:-2]))
            elif "**" in part:
                # Handle mixed cases - split on ** and alternate between regular and bold
                subparts = part.split("**")
                for i, subpart in enumerate(subparts):
                    if subpart:
                        # Odd indices are bold (after **), even indices are regular
                        segment_type = "bold" if i % 2 == 1 else "regular"
                        segments.append((segment_type, subpart))
            else:
                # Regular text
                segments.append(("regular", part))

        return segments

    def _wrap_text_with_formatting(
        self, text: str, max_width: int, fonts
    ) -> List[List[tuple]]:
        """Wrap text with formatting based on pixel width."""
        if not text:
            return [[("regular", "")]]

        draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        segments = self._parse_text_formatting(text)

        lines = []
        current_line = []
        current_width = 0

        for segment_type, segment_text in segments:
            font = fonts["cell_bold"] if segment_type == "bold" else fonts["cell"]
            words = segment_text.split()

            for word in words:
                # Calculate word width without trailing space first
                word_width = draw.textlength(word, font=font)
                space_width = draw.textlength(" ", font=font)

                # Check if we need space before this word (not first word in line)
                space_needed = space_width if current_line else 0
                total_width_needed = word_width + space_needed

                # If word fits on current line
                if current_width + total_width_needed <= max_width:
                    current_line.append((segment_type, word))
                    current_width += word_width + space_width  # Add space for next word
                else:
                    # Start new line
                    if current_line:
                        lines.append(current_line)

                    # Handle very long words that don't fit in max_width
                    if word_width > max_width:
                        # Break long word into chunks
                        chars = list(word)
                        chunk = ""
                        for char in chars:
                            test_chunk = chunk + char
                            if draw.textlength(test_chunk, font=font) <= max_width:
                                chunk = test_chunk
                            else:
                                if chunk:
                                    lines.append([(segment_type, chunk)])
                                chunk = char
                        if chunk:
                            current_line = [(segment_type, chunk)]
                            current_width = (
                                draw.textlength(chunk, font=font) + space_width
                            )
                    else:
                        current_line = [(segment_type, word)]
                        current_width = word_width + space_width

        if current_line:
            lines.append(current_line)

        return lines or [[("regular", "")]]

    def _wrap_text(self, text: str, max_width: int, font) -> List[str]:
        """Wrap text based on pixel width instead of char count (legacy method)."""
        if not text:
            return [""]

        draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        words, lines, current = text.split(), [], ""
        for word in words:
            test = (current + " " + word).strip()
            if draw.textlength(test, font=font) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]

    def _calc_col_widths(self, headers, rows, font, padding: int = 36):
        """Calculate optimal column widths with limits (high resolution)."""
        print(
            f"📏 [TableImageRenderer] Calculating high-resolution column widths for {len(headers)} columns"
        )

        draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        col_widths = []
        for i, header in enumerate(headers):
            max_width = max(
                360, int(draw.textlength(header, font=font)) + padding * 2
            )  # 3x larger min width
            for row in rows:
                if i < len(row):
                    text = str(row[i]).strip()
                    text_width = int(draw.textlength(text, font=font)) + padding * 2
                    max_width = max(
                        max_width, min(text_width, 1200)
                    )  # 3x larger max width
            col_widths.append(max_width)
            print(
                f"📏 [TableImageRenderer] Column {i + 1} ({header}): width={max_width}px"
            )

        print(
            f"📏 [TableImageRenderer] Total table width: {sum(col_widths) + len(col_widths) + 1}px"
        )
        return col_widths

    def _draw_header(
        self, draw, headers, col_widths, header_height, fonts, colors, padding
    ):
        """Draw the table header row with bold formatting support."""
        x = 0
        for i, (header, width) in enumerate(zip(headers, col_widths)):
            draw.rectangle(
                [x, 0, x + width, header_height],
                fill=colors["header_bg"],
                outline=colors["border"],
            )

            # Use formatting-aware text wrapping for headers
            header_lines = self._wrap_text_with_formatting(
                header, width - padding * 2, fonts
            )
            total_text_height = len(header_lines) * fonts["line_height"]
            text_y = (header_height - total_text_height) // 2

            for line_segments in header_lines:
                # Calculate total line width for centering
                line_width = 0
                for segment_type, word in line_segments:
                    font = (
                        fonts["header_bold"]
                        if segment_type == "bold"
                        else fonts["header"]
                    )
                    line_width += draw.textlength(word, font=font)
                    # Add space width except for last segment
                    if (segment_type, word) != line_segments[-1]:
                        line_width += draw.textlength(" ", font=font)

                # Center the line
                text_x = x + (width - line_width) // 2

                # Draw each segment
                current_x = text_x
                for idx, (segment_type, word) in enumerate(line_segments):
                    font = (
                        fonts["header_bold"]
                        if segment_type == "bold"
                        else fonts["header"]
                    )
                    # Add space before word (except for first word)
                    if idx > 0:
                        draw.text(
                            (current_x, text_y),
                            " ",
                            fill=colors["header_text"],
                            font=font,
                        )
                        current_x += draw.textlength(" ", font=font)
                    # Draw the word
                    draw.text(
                        (current_x, text_y), word, fill=colors["header_text"], font=font
                    )
                    current_x += draw.textlength(word, font=font)

                text_y += fonts["line_height"]
            x += width + 1

    def _draw_rows(
        self, draw, rows, processed_data, col_widths, start_y, fonts, colors, padding
    ):
        """Draw table rows with zebra striping and formatted text."""
        y = start_y
        for row_idx, (processed_row, row_height) in enumerate(processed_data):
            x = 0
            row_bg = colors["row_bg_alt"] if row_idx % 2 else colors["row_bg"]
            for i, (wrapped_lines, width) in enumerate(zip(processed_row, col_widths)):
                draw.rectangle(
                    [x, y, x + width, y + row_height],
                    fill=row_bg,
                    outline=colors["border"],
                )
                text_x, text_y = x + padding, y + padding // 2

                for line_segments in wrapped_lines:
                    if text_y + fonts["line_height"] <= y + row_height - padding // 2:
                        current_x = text_x
                        for idx, (segment_type, word) in enumerate(line_segments):
                            font = (
                                fonts["cell_bold"]
                                if segment_type == "bold"
                                else fonts["cell"]
                            )
                            # Add space before word (except for first word)
                            if idx > 0:
                                draw.text(
                                    (current_x, text_y),
                                    " ",
                                    fill=colors["text"],
                                    font=font,
                                )
                                current_x += draw.textlength(" ", font=font)
                            # Draw the word
                            draw.text(
                                (current_x, text_y),
                                word,
                                fill=colors["text"],
                                font=font,
                            )
                            current_x += draw.textlength(word, font=font)
                        text_y += fonts["line_height"]
                x += width + 1
            y += row_height + 1
        return y

    def _render_table_image(self, table_data: Dict[str, Any]) -> io.BytesIO:
        headers, rows = table_data["headers"], table_data["rows"]

        print("🎨 [TableImageRenderer] Starting table image rendering")
        print(
            f"📊 [TableImageRenderer] Table dimensions: {len(headers)} columns × {len(rows)} rows"
        )

        # Safety check
        if not headers:
            print("❌ [TableImageRenderer] No headers found in table data")
            raise ValueError("Table must have at least one header")

        # High resolution fonts (3x scale)
        font_size = 42  # 3x larger for high resolution
        print(
            f"🔤 [TableImageRenderer] Loading high-resolution fonts with size {font_size}"
        )
        fonts = {
            "header": self._get_font(font_size + 6, bold=False),  # 48px
            "header_bold": self._get_font(font_size + 6, bold=True),  # 48px bold
            "cell": self._get_font(font_size, bold=False),  # 42px
            "cell_bold": self._get_font(font_size, bold=True),  # 42px bold
            "line_height": font_size + 12,  # 54px line height
        }

        # Colors
        colors = {
            "bg": (255, 255, 255),
            "header_bg": (230, 230, 230),
            "row_bg": (255, 255, 255),
            "row_bg_alt": (248, 248, 248),
            "border": (200, 200, 200),
            "text": (0, 0, 0),
            "header_text": (20, 20, 20),
        }

        # High resolution layout (3x scale)
        padding, header_height, min_cell_height = 36, 120, 84  # 3x larger
        print(
            f"📐 [TableImageRenderer] High-resolution layout settings: padding={padding}, header_height={header_height}"
        )

        col_widths = self._calc_col_widths(headers, rows, fonts["cell"], padding)

        # Process rows
        print("📝 [TableImageRenderer] Processing row text wrapping")
        processed_data = []
        for row_idx, row in enumerate(rows):
            processed_row, row_height = [], min_cell_height
            for i, cell in enumerate(row):
                wrapped = self._wrap_text_with_formatting(
                    str(cell).strip(), col_widths[i] - padding * 2, fonts
                )
                processed_row.append(wrapped)
                row_height = max(
                    row_height, len(wrapped) * fonts["line_height"] + padding
                )
            processed_data.append((processed_row, row_height))
            print(f"📝 [TableImageRenderer] Row {row_idx + 1}: height={row_height}px")

        # Canvas
        total_width = sum(col_widths) + len(col_widths) + 1
        total_height = (
            header_height + sum(h for _, h in processed_data) + len(processed_data) + 1
        )
        print(f"🖼️ [TableImageRenderer] Creating canvas: {total_width}×{total_height}px")

        img = Image.new("RGB", (total_width, total_height), colors["bg"])
        draw = ImageDraw.Draw(img)

        # Draw table
        print("🎨 [TableImageRenderer] Drawing header row")
        self._draw_header(
            draw, headers, col_widths, header_height, fonts, colors, padding
        )

        print(f"🎨 [TableImageRenderer] Drawing {len(rows)} data rows")
        self._draw_rows(
            draw,
            rows,
            processed_data,
            col_widths,
            header_height + 1,
            fonts,
            colors,
            padding,
        )

        # Save high resolution image
        print("💾 [TableImageRenderer] Saving high-resolution image to buffer")
        buffer = io.BytesIO()
        img.save(
            buffer, format="PNG", quality=100, optimize=False, dpi=(300, 300)
        )  # High DPI for crisp output
        buffer.seek(0)

        print(
            f"✅ [TableImageRenderer] High-resolution image rendering complete, buffer size: {len(buffer.getvalue())} bytes"
        )
        return buffer

    async def post_async(self, shared, prep_res, exec_res):
        images = exec_res["images"]
        response_text = exec_res["response_without_tables"]
        rendered_count = exec_res["rendered_count"]

        print("🔄 [TableImageRenderer] Post-processing results")
        print(f"🖼️ [TableImageRenderer] Images generated: {len(images)}")
        print(
            f"📝 [TableImageRenderer] Response text length: {len(response_text)} characters"
        )

        shared["table_images"] = images
        shared["response_without_tables"] = response_text

        for img in images:
            print(
                f"🖼️ [TableImageRenderer] Image {img['index'] + 1}: {img['filename']}, size: {len(img['buffer'].getvalue())} bytes"
            )

        if rendered_count > 0:
            print(
                f"✅ [TableImageRenderer] Successfully rendered {rendered_count} table image(s)"
            )
            return "images_rendered"
        else:
            print("⚠️ [TableImageRenderer] No images rendered")
            return "no_images"
