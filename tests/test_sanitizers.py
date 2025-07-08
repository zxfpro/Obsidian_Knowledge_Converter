import pytest
from Obsidian_Knowledge_Converter.sanitizers import FilenameSanitizer

def test_slugify_basic():
    sanitizer = FilenameSanitizer()
    assert sanitizer._slugify("Hello World") == "hello-world"
    assert sanitizer._slugify("Another-Test_Case") == "another-test-case"
    assert sanitizer._slugify("  Leading and Trailing Spaces  ") == "leading-and-trailing-spaces"
    assert sanitizer._slugify("Multiple---Dashes") == "multiple-dashes"
    assert sanitizer._slugify("Special!@#$%^&*()Characters") == "special-characters"

def test_slugify_unicode():
    sanitizer = FilenameSanitizer()
    assert sanitizer._slugify("我的新知识！") == "我的新知识"
    assert sanitizer._slugify("你好世界") == "你好世界"

def test_get_unique_filename_no_conflict():
    sanitizer = FilenameSanitizer()
    sanitizer.reset()
    assert sanitizer.get_unique_filename("My Document") == "my-document"
    assert sanitizer.get_unique_filename("Another Doc") == "another-doc"

def test_get_unique_filename_with_conflict():
    sanitizer = FilenameSanitizer()
    sanitizer.reset()
    assert sanitizer.get_unique_filename("Duplicate Name") == "duplicate-name"
    assert sanitizer.get_unique_filename("Duplicate Name") == "duplicate-name-1"
    assert sanitizer.get_unique_filename("Duplicate Name") == "duplicate-name-2"
    assert sanitizer.get_unique_filename("duplicate-name") == "duplicate-name-3" # Test with already slugified name

def test_get_unique_filename_reset():
    sanitizer = FilenameSanitizer()
    sanitizer.reset()
    sanitizer.get_unique_filename("Test")
    sanitizer.get_unique_filename("Test")
    assert sanitizer.get_unique_filename("Test") == "test-2"
    sanitizer.reset()
    assert sanitizer.get_unique_filename("Test") == "test"