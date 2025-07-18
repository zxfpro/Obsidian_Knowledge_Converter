from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml

class MarkdownGenerator:
    """
    负责将处理好的内容写入磁盘。
    """
    def generate_file(
        self,
        filepath: Path,
        main_title: str,
        content_body: str,
        raw_content_for_describe: str = "",
        aliases: Optional[List[str]] = None,
        frontmatter_fields: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        根据提供的路径、标题、内容和 Frontmatter 参数，生成 .md 文件。
        文件内容应包含 YAML Frontmatter 和正文内容。
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)

        fm_data = {
            "title": main_title,
            "aliases": aliases if aliases else [],
            "describe": raw_content_for_describe[:100].strip()
        }
        if frontmatter_fields:
            fm_data.update(frontmatter_fields)
        
        fm_data.setdefault("type", "")
        fm_data.setdefault("ends", "")
        fm_data.setdefault("version", "")
        fm_data.setdefault("over", "")
        fm_data.setdefault("tags", [])

        # 使用 safe_dump 来处理 YAML 序列化，并确保 describe 字段的正确格式
        # default_flow_style=False 确保多行字符串以块状样式输出
        frontmatter_block = f"---\n{yaml.safe_dump(fm_data, allow_unicode=True, sort_keys=False).strip()}\n---\n"
        
        final_content = f"{frontmatter_block}\n{content_body}"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)