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
    main_title = "Test Title"
    content_body = "This is some test content."
    raw_content_for_describe = "This is a description for the test file."
    aliases = ["test-alias"]

    generator.generate_file(
        filepath,
        main_title=main_title,
        content_body=content_body,
        raw_content_for_describe=raw_content_for_describe,
        aliases=aliases
    )

    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert content.startswith("---")
        assert "title: Test Title" in content
        assert "describe: This is a description for the test file." in content
        assert "aliases:" in content
        assert "- test-alias" in content
        assert "---" in content
        assert content_body in content

def test_generate_file_with_empty_content_body(temp_output_dir):
    generator = MarkdownGenerator()
    filepath = temp_output_dir / "empty-content.md"
    main_title = "Empty Content"
    content_body = ""
    raw_content_for_describe = "This file has no body content."

    generator.generate_file(
        filepath,
        main_title=main_title,
        content_body=content_body,
        raw_content_for_describe=raw_content_for_describe
    )

    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert content.startswith("---")
        assert "title: Empty Content" in content
        assert "describe: This file has no body content." in content
        assert "---" in content
        assert content_body in content # Should still be present, even if empty

def test_generate_file_with_long_describe(temp_output_dir):
    generator = MarkdownGenerator()
    filepath = temp_output_dir / "long-describe.md"
    main_title = "Long Describe"
    content_body = "Some body content."
    long_describe = "a" * 150 # More than 100 characters

    generator.generate_file(
        filepath,
        main_title=main_title,
        content_body=content_body,
        raw_content_for_describe=long_describe
    )

    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert "describe: " + ("a" * 100) in content # Should be truncated to 100 chars
        assert "Some body content." in content

def test_generate_file_with_additional_frontmatter_fields(temp_output_dir):
    generator = MarkdownGenerator()
    filepath = temp_output_dir / "custom-fm.md"
    main_title = "Custom FM"
    content_body = "Body content."
    frontmatter_fields = {
        "type": "note",
        "version": "1.0",
        "tags": ["tag1", "tag2"]
    }

    generator.generate_file(
        filepath,
        main_title=main_title,
        content_body=content_body,
        frontmatter_fields=frontmatter_fields
    )

    assert filepath.exists()
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert "title: Custom FM" in content
        assert "type: note" in content
        assert "version: '1.0'" in content # PyYAML might output '1.0' as a string
        assert "tags:" in content
        assert "- tag1" in content
        assert "- tag2" in content
        assert "Body content." in content

def test_generate_file_creates_directories(tmp_path):
    generator = MarkdownGenerator()
    filepath = tmp_path / "nested" / "sub" / "nested-file.md"
    title = "Nested File"
    content = "Content for nested file."

    generator.generate_file(filepath, title, content)

    assert filepath.exists()
    assert filepath.parent.exists()