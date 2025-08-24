from utils.discord_helpers import split_message

def test_split_message_simple():
    long_text = "a" * 2500
    chunks = split_message(long_text)
    assert len(chunks) == 2
    assert len(chunks[0]) <= 2000
    assert len(chunks[1]) <= 2000

def test_split_message_no_split():
    short_text = "hello"
    chunks = split_message(short_text)
    assert len(chunks) == 1
    assert chunks[0] == short_text

def test_split_message_on_boundary():
    text = "a" * 2000
    chunks = split_message(text)
    assert len(chunks) == 1
    assert chunks[0] == text
