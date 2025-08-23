"""
Markdown table extraction node for the async flow pipeline.
"""

import re
import os
from typing import Dict, Any
from pocketflow import AsyncNode


class MarkdownTableExtractor(AsyncNode):
    """Node to identify and extract markdown tables from messages"""

    async def prep_async(self, shared):
        print("📊 [MarkdownTableExtractor] Preparing to extract tables from message")
        return {
            "llm_response": shared.get("llm_response", ""),
            "content": shared.get("content", ""),
            "message_id": shared.get("message_id", "unknown"),
        }

    async def exec_async(self, prep_res):
        print("🔍 [MarkdownTableExtractor] Analyzing text for markdown tables...")

        # Check both LLM response and original content
        text_to_analyze = prep_res["llm_response"] or prep_res["content"]

        if not text_to_analyze:
            print("⚠️ [MarkdownTableExtractor] No text to analyze")
            return {"has_table": False, "tables": [], "processed_text": text_to_analyze}

        # Regex pattern to match markdown tables
        # Matches: | header | header |
        #          |--------|--------|
        #          | cell   | cell   |
        table_pattern = r"(\|[^\n]*\|\s*\n\|[-\s|:]*\|\s*\n(?:\|[^\n]*\|\s*\n?)*)"

        tables = re.findall(table_pattern, text_to_analyze, re.MULTILINE)

        if tables:
            print(f"✅ [MarkdownTableExtractor] Found {len(tables)} markdown table(s)")

            # Parse each table into structured data and create files
            parsed_tables = []
            table_files = []
            message_id = prep_res["message_id"]

            # Ensure temp directory exists
            os.makedirs("temp", exist_ok=True)

            for i, table_text in enumerate(tables):
                parsed_table = self._parse_table(table_text.strip())

                # Create filename for this table in temp folder
                filename = f"temp/daia_replaced_table_{message_id}_{i + 1}.md"

                # Write table to file
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(table_text.strip())

                parsed_tables.append(
                    {
                        "index": i,
                        "raw_text": table_text.strip(),
                        "parsed": parsed_table,
                        "filename": filename,
                    }
                )
                table_files.append(filename)

                print(
                    f"📋 [MarkdownTableExtractor] Table {i + 1}: {len(parsed_table['headers'])} columns, {len(parsed_table['rows'])} rows -> {filename}"
                )

            return {
                "has_table": True,
                "tables": parsed_tables,
                "processed_text": text_to_analyze,
                "table_count": len(tables),
                "table_files": table_files,
            }
        else:
            print("❌ [MarkdownTableExtractor] No markdown tables found")
            return {
                "has_table": False,
                "tables": [],
                "processed_text": text_to_analyze,
                "table_count": 0,
            }

    def _parse_table(self, table_text: str) -> Dict[str, Any]:
        """Parse a markdown table into structured data"""
        lines = [line.strip() for line in table_text.split("\n") if line.strip()]

        if len(lines) < 3:  # Need at least header, separator, and one data row
            return {"headers": [], "rows": [], "valid": False}

        # Extract headers (first line)
        header_line = lines[0]
        headers = [
            cell.strip() for cell in header_line.split("|")[1:-1]
        ]  # Remove empty first/last elements

        # Skip separator line (second line)
        # Extract data rows (remaining lines)
        rows = []
        for line in lines[2:]:
            if line.startswith("|") and line.endswith("|"):
                cells = [cell.strip() for cell in line.split("|")[1:-1]]
                # Pad or truncate to match header count
                while len(cells) < len(headers):
                    cells.append("")
                cells = cells[: len(headers)]
                rows.append(cells)

        return {
            "headers": headers,
            "rows": rows,
            "valid": len(headers) > 0 and len(rows) > 0,
        }

    async def post_async(self, shared, prep_res, exec_res):
        shared["table_extraction"] = exec_res

        if exec_res["has_table"]:
            print(
                f"📊 [MarkdownTableExtractor] Extracted {exec_res['table_count']} table(s)"
            )
            # Store individual tables for easy access
            shared["extracted_tables"] = exec_res["tables"]
            # Store table filenames
            shared["extracted_tables_files"] = exec_res["table_files"]
            return "tables_found"
        else:
            print("📊 [MarkdownTableExtractor] No tables found")
            return "no_tables"
