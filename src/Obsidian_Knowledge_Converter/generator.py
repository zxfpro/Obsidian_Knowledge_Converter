from pathlib import Path
from typing import List, Optional

class MarkdownGenerator:
    """
    负责将处理好的内容写入磁盘。
    """
    def generate_file(self, filepath: Path, title: str, content: str, parent_links: Optional[List[str]] = None):
        """
        根据提供的路径、标题、内容和父级链接列表，生成 .md 文件。
        文件内容应包含 H1 标题、主要内容，以及可选的、位于 --- 分隔符下方的父级链接。
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(content)

            if parent_links:
                f.write("\n\n---\n")
                for link in parent_links:
                    f.write(f"* {link}\n")