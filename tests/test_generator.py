import pytest
from pathlib import Path
from Obsidian_Knowledge_Converter.generator import MarkdownGenerator

@pytest.fixture
def temp_output_dir(tmp_path):
    """
    为测试提供一个临时输出目录。
    """
    return tmp_path / "output"

def test_generate_file_basic(temp_output_dir):
    generator = MarkdownGenerator()
    filepath = temp_output_dir / "test-file.md"
    title = "Test Title"
    content = "This is some test content."

    generator.generate_file(filepath, title, content)

    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert lines[0].strip() == "# Test Title"
        assert lines[2].strip() == "This is some test content."

def test_generate_file_with_parent_links(temp_output_dir):
    generator = MarkdownGenerator()
    filepath = temp_output_dir / "linked-file.md"
    title = "Linked Title"
    content = "Content with links."
    parent_links = ["Parent File: [[ParentDoc]]", "Parent Section: [[Section1]]"]

    generator.generate_file(filepath, title, content, parent_links)

    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert lines[0].strip() == "# Linked Title"
        assert lines[2].strip() == "Content with links."
        assert lines[4].strip() == "---"
        assert lines[5].strip() == "* Parent File: [[ParentDoc]]"
        assert lines[6].strip() == "* Parent Section: [[Section1]]"

def test_generate_file_creates_directories(tmp_path):
    generator = MarkdownGenerator()
    filepath = tmp_path / "nested" / "sub" / "nested-file.md"
    title = "Nested File"
    content = "Content for nested file."

    generator.generate_file(filepath, title, content)

    assert filepath.exists()
    assert filepath.parent.exists()