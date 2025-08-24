import asyncio
import os
import tempfile

from nodes.contextual_system_prompt import ContextualSystemPrompt
from nodes.table_extractor import MarkdownTableExtractor


def test_contextual_system_prompt_disabled():
    """Test ContextualSystemPrompt when disabled."""

    async def run_test():
        node = ContextualSystemPrompt(
            enable_contextual_system_prompt=False,
            genai_chat_system_prompt="base prompt",
            history_limit=10,
        )
        shared = {"unique_users": {"UserA"}, "author_name": "UserB"}
        prep_res = await node.prep_async(shared)
        exec_res = await node.exec_async(prep_res)
        assert exec_res == "base prompt"

    asyncio.run(run_test())


def test_contextual_system_prompt_enabled():
    """Test ContextualSystemPrompt when enabled."""

    async def run_test():
        node = ContextualSystemPrompt(
            enable_contextual_system_prompt=True,
            genai_chat_system_prompt="base prompt",
            history_limit=10,
        )
        shared = {"unique_users": {"UserA"}, "author_name": "UserB"}
        prep_res = await node.prep_async(shared)
        exec_res = await node.exec_async(prep_res)
        assert "You are talking to a human named UserB" in exec_res
        assert "Current participants:" in exec_res
        assert "UserA" in exec_res and "UserB" in exec_res
        assert "base prompt" in exec_res

    asyncio.run(run_test())


def test_markdown_table_extractor_no_table():
    """Test MarkdownTableExtractor when no table is present."""

    async def run_test():
        node = MarkdownTableExtractor()
        shared = {"llm_response": "This is a test without a table."}
        prep_res = await node.prep_async(shared)
        exec_res = await node.exec_async(prep_res)
        assert exec_res["has_table"] is False
        assert exec_res["table_count"] == 0
        assert len(exec_res["tables"]) == 0

    asyncio.run(run_test())


def test_markdown_table_extractor_with_table():
    """Test MarkdownTableExtractor when a table is present."""

    async def run_test():
        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory to avoid creating files in project root
            original_cwd = os.getcwd()
            os.chdir(temp_dir)

            try:
                node = MarkdownTableExtractor()
                table_text = "| Header 1 | Header 2 |\n|---|---|\n| Cell 1 | Cell 2 |"
                shared = {
                    "llm_response": f"Here is a table:\n{table_text}",
                    "message_id": "test123",
                }
                prep_res = await node.prep_async(shared)
                exec_res = await node.exec_async(prep_res)

                assert exec_res["has_table"] is True
                assert exec_res["table_count"] == 1
                assert len(exec_res["tables"]) == 1
                assert table_text in exec_res["tables"][0]["raw_text"]

                # Check that the parsed table has correct structure
                parsed = exec_res["tables"][0]["parsed"]
                assert parsed["headers"] == ["Header 1", "Header 2"]
                assert parsed["rows"] == [["Cell 1", "Cell 2"]]
                assert parsed["valid"] is True

            finally:
                os.chdir(original_cwd)

    asyncio.run(run_test())
