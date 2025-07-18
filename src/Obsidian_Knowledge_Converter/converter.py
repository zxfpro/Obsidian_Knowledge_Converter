import json
from pathlib import Path
from typing import Dict, List, Optional

from .models import ContentData, ProcessedNode, GLOBAL_LINK_MAP
from .sanitizers import FilenameSanitizer
from .link_rewriter import LinkRewriter
from .generator import MarkdownGenerator

class ObsidianConverter:
    """
    主协调器，包含核心转换流程。
    """
    def __init__(self, output_root: str):
        self.output_root = Path(output_root)
        self.sanitizer = FilenameSanitizer()
        self.link_rewriter = LinkRewriter(GLOBAL_LINK_MAP)
        self.generator = MarkdownGenerator()
        GLOBAL_LINK_MAP.clear() # 每次初始化时清空，确保新的转换不受旧数据影响

    def convert(self, input_json: Dict):
        """
        开始转换过程。
        """
        self.sanitizer.reset() # 重置文件名生成器
        
        # 第一次遍历：收集所有链接映射
        self._collect_link_mappings(input_json, Path(""), Path(""))

        # 第二次遍历：生成Markdown文件并重写链接
        self._generate_markdown_files(input_json, self.output_root, Path(""))

    def _collect_link_mappings(self, node_data: Dict, current_original_path: Path, current_output_path: Path):
        """
        第一次遍历：递归处理JSON中的节点，收集所有文件和章节的链接映射。
        """
        node_name = node_data.get("name")
        node_type = node_data.get("type")
        children = node_data.get("children", [])

        if node_type == "folder":
            new_original_path = current_original_path / node_name
            new_output_path = current_output_path / node_name # 收集阶段也需要生成output_path来确保sanitizer的唯一性
            for child in children:
                self._collect_link_mappings(child, new_original_path, new_output_path)
        elif node_type == "file":
            file_content = node_data.get("content")
            if file_content:
                original_file_full_path = current_original_path / node_name
                self._collect_file_mapping(file_content, original_file_full_path, current_output_path)

    def _collect_file_mapping(self, file_data: Dict, original_file_full_path: Path, current_output_path: Path):
        """
        收集单个文件节点的链接映射。
        """
        title = file_data.get("title", "Untitled")
        children_raw = file_data.get("children", [])

        main_obsidian_link_name = self.sanitizer.get_unique_filename(title)

        original_path_key = original_file_full_path.as_posix() # 使用完整路径作为key
        GLOBAL_LINK_MAP[original_path_key] = main_obsidian_link_name

        for child_data in children_raw:
            self._collect_section_mapping(child_data, original_file_full_path, main_obsidian_link_name, current_output_path)

    def _collect_section_mapping(self, section_data: Dict, original_file_full_path: Path, parent_obsidian_link_name: str, current_output_path: Path):
        """
        收集单个章节的链接映射。
        """
        title = section_data.get("title", "Untitled Section")
        children_raw = section_data.get("children", [])

        # DCN中建议的命名规则：f"{original_filename_base}-{child_content_data.title}"
        # 这里需要根据实际情况调整，确保唯一性
        # 对于子章节，其原始路径可以表示为 "原始文件路径#章节标题"
        section_original_path_key = f"{original_file_full_path.as_posix()}#{title}"
        
        # 生成子章节的 Obsidian 链接名，确保唯一性
        # 这里使用原始文件名的stem作为前缀，加上章节标题
        original_filename_base = original_file_full_path.stem
        suggested_filename_base = f"{original_filename_base}-{title}"
        section_obsidian_link_name = self.sanitizer.get_unique_filename(suggested_filename_base)

        GLOBAL_LINK_MAP[section_original_path_key] = section_obsidian_link_name

        for child_data in children_raw:
            self._collect_section_mapping(child_data, original_file_full_path, section_obsidian_link_name, current_output_path)

    def _generate_markdown_files(self, node_data: Dict, current_output_path: Path, current_original_path: Path):
        """
        第二次遍历：递归处理JSON中的节点，生成Markdown文件并重写链接。
        """
        node_name = node_data.get("name")
        node_type = node_data.get("type")
        children = node_data.get("children", [])

        if node_type == "folder":
            new_output_path = current_output_path / node_name
            new_original_path = current_original_path / node_name
            for child in children:
                self._generate_markdown_files(child, new_output_path, new_original_path)
        elif node_type == "file":
            file_content = node_data.get("content")
            if file_content:
                original_file_full_path = current_original_path / node_name
                self._generate_file_content(file_content, current_output_path, original_file_full_path)

    def _generate_file_content(self, file_data: Dict, current_output_path: Path, original_file_full_path: Path):
        """
        生成单个文件节点的内容。
        """
        main_title = file_data.get("title", "Untitled")
        raw_content_for_describe = file_data.get("content", "")
        children_raw = file_data.get("children", [])

        original_path_key = original_file_full_path.as_posix()
        main_obsidian_link_name = GLOBAL_LINK_MAP.get(original_path_key, self.sanitizer._slugify(main_title))

        child_links_markdown = []
        for child_data in children_raw:
            child_original_path_key = f"{original_file_full_path.as_posix()}#{child_data.get('title')}"
            child_obsidian_link_name = GLOBAL_LINK_MAP.get(child_original_path_key)
            if child_obsidian_link_name: # 确保链接名存在
                child_links_markdown.append(f"[[{child_obsidian_link_name}]]")
        
        content_body = "\n".join(child_links_markdown)

        output_filepath = current_output_path / f"{main_obsidian_link_name}.md"
        self.generator.generate_file(
            filepath=output_filepath,
            main_title=main_title,
            content_body=content_body,
            raw_content_for_describe=raw_content_for_describe,
            aliases=[main_obsidian_link_name]
        )

        for child_data in children_raw:
            self._generate_section_content(child_data, current_output_path, original_file_full_path, main_obsidian_link_name)

    def _generate_section_content(self, section_data: Dict, current_output_path: Path, original_file_full_path: Path, parent_obsidian_link_name: str):
        """
        生成单个章节的内容。
        """
        section_title = section_data.get("title", "Untitled Section")
        raw_content_for_describe = section_data.get("content", "")
        children_raw = section_data.get("children", [])

        section_original_path_key = f"{original_file_full_path.as_posix()}#{section_title}"
        section_obsidian_link_name = GLOBAL_LINK_MAP.get(section_original_path_key) # 直接从GLOBAL_LINK_MAP获取

        grandchild_links_markdown = []
        for grandchild_data in children_raw:
            grandchild_original_path_key = f"{original_file_full_path.as_posix()}#{grandchild_data.get('title')}"
            grandchild_obsidian_link_name = GLOBAL_LINK_MAP.get(grandchild_original_path_key)
            if grandchild_obsidian_link_name: # 确保链接名存在
                grandchild_links_markdown.append(f"[[{grandchild_obsidian_link_name}]]")
        
        content_body = "\n".join(grandchild_links_markdown)

        output_filepath = current_output_path / f"{section_obsidian_link_name}.md"
        self.generator.generate_file(
            filepath=output_filepath,
            main_title=section_title,
            content_body=content_body,
            raw_content_for_describe=raw_content_for_describe,
            aliases=[section_obsidian_link_name]
        )

        for child_data in children_raw:
            self._generate_section_content(child_data, current_output_path, original_file_full_path, section_obsidian_link_name)
