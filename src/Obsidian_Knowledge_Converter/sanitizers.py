import re
from typing import Set

class FilenameSanitizer:
    """
    负责文件名合法化（slugify）和去重。
    """
    def __init__(self):
        self.generated_filenames: Set[str] = set()

    def reset(self):
        """
        重置已生成的文件名集合。
        """
        self.generated_filenames.clear()

    def _slugify(self, text: str) -> str:
        """
        将文本转换为文件系统友好的“slug”形式。
        - 转换为小写。
        - 非字母数字字符替换为连字符。
        - 移除重复连字符。
        - 移除开头和结尾的连字符。
        """
        text = text.lower()
        # 将非字母数字（包括中文）替换为连字符
        text = re.sub(r'[^\w\s-]', '-', text, flags=re.UNICODE) # 将非字母数字、非空白、非连字符的字符替换为连字符
        text = re.sub(r'[\s_-]+', '-', text, flags=re.UNICODE) # 将空白或下划线替换为连字符，并处理重复连字符
        text = text.strip('-')
        return text

    def get_unique_filename(self, desired_name: str) -> str:
        """
        在 _slugify 的基础上，处理命名冲突，通过添加 _1, _2 等后缀确保唯一性。
        """
        slugified_name = self._slugify(desired_name)
        unique_name = slugified_name
        counter = 1
        while unique_name in self.generated_filenames:
            unique_name = f"{slugified_name}-{counter}"
            counter += 1
        self.generated_filenames.add(unique_name)
        return unique_name