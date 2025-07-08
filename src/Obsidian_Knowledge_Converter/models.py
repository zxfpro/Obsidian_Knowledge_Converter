from pathlib import Path
from typing import Dict, List, Optional

# 定义全局链接映射，用于存储原始路径到Obsidian链接名的映射
GLOBAL_LINK_MAP: Dict[str, str] = {}

class ContentData:
    """
    用于表示文件或内部标题块的内容。
    """
    def __init__(self,
                 title: str,
                 level: int,
                 content: str,
                 children_raw: List[Dict],
                 original_filename: str,
                 parent_title: Optional[str] = None,
                 obsidian_link_name: Optional[str] = None,
                 output_slug_filename: Optional[str] = None,
                 output_filepath: Optional[Path] = None):
        self.title = title
        self.level = level
        self.content = content
        self.children_raw = children_raw
        self.original_filename = original_filename
        self.parent_title = parent_title
        self.obsidian_link_name = obsidian_link_name
        self.output_slug_filename = output_slug_filename
        self.output_filepath = output_filepath

class ProcessedNode:
    """
    用于表示JSON中的文件或文件夹节点。
    """
    def __init__(self,
                 name: str,
                 node_type: str,
                 relative_path: Path,
                 children: List['ProcessedNode'],
                 content_data: Optional[ContentData] = None):
        self.name = name
        self.type = node_type
        self.relative_path = relative_path
        self.children = children
        self.content_data = content_data