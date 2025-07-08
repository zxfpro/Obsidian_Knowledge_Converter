import re
from pathlib import Path
from typing import Dict
from urllib.parse import urlparse, unquote

class LinkRewriter:
    """
    负责解析和转换 Markdown 内部链接为 Obsidian 双链。
    """
    def __init__(self, global_link_map: Dict[str, str]):
        self.global_link_map = global_link_map

    def rewrite_links(self, markdown_content: str, current_file_original_path: Path) -> str:
        """
        将原始 Markdown 内容中的相对路径链接转换为 Obsidian 双链。
        """
        # 正则表达式匹配 Markdown 链接：[text](url)
        # 确保不匹配代码块中的链接
        # 匹配非代码块中的链接
        # 匹配非代码块中的链接
        def replace_link(match):
            full_match = match.group(0)
            link_text = match.group(1)
            link_url = match.group(2)
            print(f"LinkRewriter: Matched link: text='{link_text}', url='{link_url}'") # Debug print

            # 检查是否是外部链接
            if link_url.startswith(('http://', 'https://', 'mailto:', 'ftp://')):
                return full_match

            print(f"LinkRewriter Debug: current_file_original_path={current_file_original_path}")
            print(f"LinkRewriter Debug: link_url={link_url}")

            try:
                parsed_url = urlparse(link_url)
                path_part = Path(unquote(parsed_url.path))
                fragment_part = unquote(parsed_url.fragment)

                # 计算链接的原始相对路径
                if current_file_original_path.is_file():
                    resolved_original_path = (current_file_original_path.parent / path_part).resolve()
                else:
                    resolved_original_path = (current_file_original_path / path_part).resolve()
                
                # 移除文件扩展名
                key_path_base = resolved_original_path.with_suffix('').as_posix()

                if fragment_part:
                    key_path = f"{key_path_base}-{link_text}"
                else:
                    key_path = key_path_base

                print(f"LinkRewriter Debug: resolved_original_path={resolved_original_path}")
                print(f"LinkRewriter Debug: key_path generated: {key_path}") # Debug print
                print(f"LinkRewriter Debug: global_link_map keys: {self.global_link_map.keys()}") # Debug print

                obsidian_link_name = self.global_link_map.get(key_path)

                if obsidian_link_name:
                    # 如果找到，转换为 Obsidian 双链
                    rewritten_link = f"[[{obsidian_link_name}|{link_text}]]"
                    print(f"LinkRewriter Debug: Rewritten link: {rewritten_link}") # Debug print
                    return rewritten_link
                else:
                    # 如果未找到映射，保留原始链接
                    print(f"LinkRewriter Debug: No obsidian_link_name found for key_path: {key_path}. Retaining original link.") # Debug print
                    return full_match
            except Exception as e:
                print(f"LinkRewriter Error: Exception during link rewriting: {e}") # Debug print
                # 解析失败，保留原始链接
                return full_match

        # 使用 re.sub 和一个函数来处理匹配到的链接
        # 这个正则表达式会跳过被 ``` 包裹的代码块
        # 它首先尝试匹配代码块，如果匹配到，则不进行替换；否则，匹配普通链接
        # re.DOTALL 使得 . 匹配包括换行符在内的所有字符
        # re.M 使得 ^ 和 $ 匹配每一行的开始和结束
        
        # 这是一个简化的方法，更健壮的Markdown解析器会使用AST
        # 这里我们尝试避免在代码块中替换链接
        # 匹配代码块
        code_block_pattern = r"(```.*?```)"
        # 匹配非代码块中的链接
        # 匹配 [text](url) 形式的链接
        link_pattern = r"\[([^\]]+?)\]\((.+?)\)"

        # 分割文本为代码块和非代码块部分
        parts = re.split(code_block_pattern, markdown_content, flags=re.DOTALL)
        
        rewritten_parts = []
        for i, part in enumerate(parts):
            if i % 2 == 0:  # 非代码块部分
                rewritten_parts.append(re.sub(link_pattern, replace_link, part))
            else:  # 代码块部分
                rewritten_parts.append(part)
        
        return "".join(rewritten_parts)