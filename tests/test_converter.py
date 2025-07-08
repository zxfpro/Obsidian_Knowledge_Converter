import pytest
import json
from pathlib import Path
import shutil

from Obsidian_Knowledge_Converter.converter import ObsidianConverter
from Obsidian_Knowledge_Converter.models import GLOBAL_LINK_MAP

@pytest.fixture
def temp_output_vault(tmp_path):
    """
    为测试提供一个临时输出目录，并在测试结束后清理。
    """
    output_dir = tmp_path / "output_vault"
    output_dir.mkdir()
    yield output_dir
    shutil.rmtree(output_dir)

@pytest.fixture(autouse=True)
def clear_global_link_map_for_converter_tests():
    """
    在每个测试运行前清空 GLOBAL_LINK_MAP。
    """
    GLOBAL_LINK_MAP.clear()
    yield

def test_converter_unique_filenames(temp_output_vault):
    input_json = {
        "name": "root",
        "type": "folder",
        "children": [
            {
                "name": "file1.md",
                "type": "file",
                "content": {
                    "title": "Duplicate Name",
                    "level": 1,
                    "content": "Content 1",
                    "children": []
                }
            },
            {
                "name": "file2.md",
                "type": "file",
                "content": {
                    "title": "Duplicate Name",
                    "level": 1,
                    "content": "Content 2",
                    "children": []
                }
            }
        ]
    }

    converter = ObsidianConverter(str(temp_output_vault))
    converter.convert(input_json)

    assert (temp_output_vault / "root" / "duplicate-name.md").exists()
    assert (temp_output_vault / "root" / "duplicate-name-1.md").exists()
