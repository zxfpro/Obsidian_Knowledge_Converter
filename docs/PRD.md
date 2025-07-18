好的，既然我们已经深入探讨了需求和潜在的实现细节，现在是时候将这些讨论系统化，并生成一份 PRD (产品需求文档) 草稿了。这份 PRD 将用于指导后续的开发工作。

---

# 产品需求文档 (PRD) 草稿

## 1. 引言

### 1.1 产品概述

本产品是一个 Python 包，旨在将 `KnowledgeIngestor` 库输出的结构化 JSON 数据（包含文件系统层级和文件内部标题层级）转换为一系列符合 Obsidian 最佳实践的 Markdown 文件。通过将文件内部的各级标题独立成文件，并利用 Obsidian 的双链语法进行关联，本工具旨在将线性的文档结构转化为高度互联的知识网络，提升知识的可发现性和组织性。

### 1.2 目标用户

*   使用 `KnowledgeIngestor` 生成知识库的开发者或团队。
*   希望将结构化文档（尤其是 Markdown 格式）导入 Obsidian 进行精细化管理的用户。
*   追求更细粒度知识管理和关联的用户。

### 1.3 核心价值

*   **增强知识关联性：** 将文档内部的逻辑结构转化为可导航的超链接网络。
*   **提升知识粒度：** 允许用户以更小的单元（如章节、小节）来管理和引用知识。
*   **优化 Obsidian 体验：** 生成符合 Obsidian 双链语法的 Markdown 文件，最大化其知识图谱功能。
*   **自动化转换：** 减少手动拆分和链接文档的工作量。

## 2. 功能需求

### 2.1 输入

*   `KnowledgeIngestor` 库生成的 JSON 格式数据。此 JSON 结构包含文件夹、文件以及文件内部的标题和内容层级。

### 2.2 输出

*   一系列 `.md` Markdown 文件，组织在一个指定的输出目录下。
*   文件命名和内容符合 Obsidian 双链语法规范。

### 2.3 核心功能

#### 2.3.1 JSON 结构解析与遍历

*   **F1.1 递归解析：** 能够递归遍历输入的 JSON 数据，识别 `folder` 和 `file` 类型节点。
*   **F1.2 内容提取：** 能够准确提取每个文件节点中的 `name`, `type`, `content` (包含 `title`, `level`, `content`, `children`) 等字段。

#### 2.3.2 文件生成与目录结构维护

*   **F2.1 目录映射：** 将 JSON 中的 `folder` 结构映射到文件系统的实际目录。
*   **F2.2 原始文件处理：**
    *   为 JSON 中每个 `type: "file"` 的节点，在对应目录下生成一个主 Markdown 文件。
    *   该主文件应包含原始文件的顶层 `content`。
    *   该主文件应包含指向其内部所有一级子标题（如果被独立成文件）的双链。
*   **F2.3 标题拆分与独立文件生成：**
    *   将每个文件的 `content` 字段中的所有非顶层 `title`（即 `level > 1` 的标题）视为独立的知识单元。
    *   为每个独立的知识单元生成一个新的 Markdown 文件。
    *   新文件的主体内容为其对应标题下的 `content`。
    *   新文件的标题应作为文件内的 H1 标题。

#### 2.3.3 链接与关联 (Obsidian 双链)

*   **F3.1 父子关系链接：**
    *   在独立出的标题文件中，自动添加指向其父级标题文件或原始主文件的双链，例如在文件末尾添加 `---` 分隔符和 `*Parent:* [[Parent Title]]`。
    *   在原始主文件和父级标题文件中，自动添加指向其所有子标题文件的双链。
*   **F3.2 内部链接转换：**
    *   识别原始 Markdown 内容中形如 `[Text](../../path/to/file.md)` 的相对路径链接。
    *   尝试将这些链接转换为 Obsidian 双链 `[[File Name]]`，前提是 `File Name` 也在本次处理中被生成为独立文件。
    *   如果无法转换为双链（例如指向外部资源或未被处理的文件），则保留原始 Markdown 链接。
*   **F3.3 外部链接处理：** 保持所有外部 URL 链接不变。

#### 2.3.4 文件命名与重名处理

*   **F4.1 文件名合法化 (Slugify)：**
    *   将所有标题字符串转换为符合文件系统命名规范的“slug”形式（例如，将空格替换为短横线，移除特殊字符，转换为小写）。
    *   **规避特殊字符：** 严格移除或替换 `\ / : * ? " < > |` 等非法字符。
    *   **处理非 ASCII 字符：** 确保支持 Unicode 字符（如中文标题）的正确转换和保存。
*   **F4.2 命名冲突解决：**
    *   当生成的文件名（包括主文件和独立标题文件）发生冲突时，自动添加后缀 `_1`, `_2` 等进行区分。
    *   **命名策略建议：** 独立标题文件的命名格式为 `[原始文件名 - ]标题名.md`，例如 `query_transformations - Use Cases.md`。这有助于在文件名层面就减少冲突，并提供上下文。

### 2.4 可配置项 (Optional, but good to have)

*   **C1.1 输出目录：** 允许用户指定生成 Markdown 文件的输出目录。
*   **C1.2 链接样式：** 允许用户配置父子链接的显示方式（例如，是否显示 `*Parent:*` 前缀）。
*   **C1.3 文件命名策略：** 允许用户选择不同的文件命名策略（例如，是否包含原始文件名作为前缀）。
*   **C1.4 过滤规则：** 允许用户指定哪些 `level` 的标题需要被独立成文件，或哪些文件/文件夹需要被跳过。

## 3. 非功能需求

*   **性能：** 能够高效处理大型 JSON 结构和大量文件。
*   **健壮性：** 能够优雅地处理异常情况，如无效的 JSON 结构、文件读写权限问题等。
*   **易用性：** 提供清晰的 API 接口和详细的文档。
*   **兼容性：** 生成的 Markdown 文件应与 Obsidian 兼容，并尽可能兼容其他 Markdown 编辑器。
*   **可维护性：** 代码结构清晰，模块化程度高，易于扩展和维护。

## 4. 技术选型 (初步)

*   **编程语言：** Python 3.x
*   **JSON 解析：** Python 内置 `json` 库。
*   **文件系统操作：** Python 内置 `os`, `pathlib` 库。
*   **字符串处理：** Python 内置字符串方法，可能结合 `re` (正则表达式) 库进行 slugify。

## 5. 待议问题

*   **链接解析的深度和广度：** 是否需要解析 Markdown 链接并尝试转换为双链？如果是，其匹配规则和优先级如何？
*   **内容块的边界：** 一个标题的 `content` 应该包含到哪里？是只包含其直接的 `content` 字段，还是包含所有子标题之前的所有文本？（目前倾向于只包含直接 `content`）
*   **根目录的处理：** `KnowledgeIngestor` 输出的根节点 `name` (如 `my_knowledge_base`) 是否需要创建一个同名文件夹？
*   **代码块处理：** 代码块中的内容是否需要特殊处理，例如链接不进行转换？（默认不处理，保持原样）

---

这份 PRD 涵盖了我们目前讨论的所有关键点。您可以审阅一下，看看是否有需要补充、修改或澄清的地方。



# **更新后的 PRD (Product Requirements Document)**

## Python 包开发指南：Obsidian Knowledge Converter

### 1. 项目启动与规划

#### 1.1 明确项目目标

*   **输入**: `KnowledgeIngestor` 生成的 JSON 数据。
*   **输出**: 符合 Obsidian 规范的 Markdown 文件集合，具备原子化知识单元、强化双向链接和标准化 Frontmatter。
*   **核心转换逻辑**: 将 JSON 中的文件内部标题结构“原子化”为独立文件，并通过双链关联。同时，将原始文档内容转换为元数据和导航链接。

#### 1.2 规划项目结构

*   **建议的模块划分**: 将功能分解为逻辑清晰、职责单一的模块。
    *   `converter.py`: 主协调器，包含核心转换流程。
    *   `models.py`: 定义内部数据模型，如 `ContentData` 和 `ProcessedNode`，用于数据传递。
    *   `sanitizers.py`: 负责文件名合法化（slugify）和去重。
    *   `link_rewriter.py`: 负责解析和转换 Markdown 内部链接为 Obsidian 双链。
    *   `generator.py`: 负责将处理后的内容写入文件系统，包含 YAML Frontmatter 的生成。
*   **目录结构**: 遵循 Python 包的惯例，设置 `src` 或直接在顶层创建包名目录。包含 `tests/` 和 `examples/` 目录。
*   **环境管理**: 推荐使用 `venv` 或 `Poetry` 进行依赖管理。

#### 1.3 工具选择

*   **语言**: Python 3.x
*   **依赖**: 优先使用标准库。新增 `PyYAML` 用于 YAML Frontmatter 的生成。对于更复杂的 Markdown 解析，可考虑 `markdown-it-py` 或 `mistune`（但初期可手动处理）。
*   **测试**: `pytest`。
*   **代码质量**: `black` (格式化), `flake8` (linting)。

### 2. 核心模块设计与开发

本节将重申设计文档中核心模块的职责，并给出其在开发指南中的定位。

#### 2.1 模块概览 (UML 类图)

以下是本项目核心类的协作关系和职责概述，指导开发者理解模块间的交互：

```mermaid
classDiagram
    class ObsidianConverter {
        -output_root: Path
        -sanitizer: FilenameSanitizer
        -link_rewriter: LinkRewriter
        -generator: MarkdownGenerator
        +__init__(output_root: str)
        +convert(input_json: Dict)
        -process_node(node_data: Dict, current_output_path: Path, current_original_path: Path)
        -process_file(file_data: Dict, current_output_path: Path, original_file_full_path: Path)
        -process_section(section_data: Dict, current_output_path: Path, original_file_full_path: Path, parent_obsidian_link_name: str)
    }
    class FilenameSanitizer {
        -generated_filenames: Set[str]
        +__init__()
        +get_unique_filename(desired_name: str) -> str
        +reset()
        -_slugify(text: str) -> str
    }
    class LinkRewriter {
        -global_link_map: Dict[str, str]
        +__init__(global_link_map: Dict[str, str])
        +rewrite_links(markdown_content: str, current_file_original_path: Path) -> str
    }
    class MarkdownGenerator {
        +generate_file(filepath: Path, main_title: str, content_body: str, raw_content_for_describe: str, aliases: List[str], frontmatter_fields: Dict[str, Any])
    }
    class ContentData {
        +title: str
        +level: int
        +content: str
        +children_raw: List[Dict]
        +original_filename: str
        +parent_title: str
        +obsidian_link_name: str
        +output_slug_filename: str
        +output_filepath: Path
    }
    class ProcessedNode {
        +name: str
        +type: str
        +relative_path: Path
        +children: List[ProcessedNode]
        +content_data: ContentData
    }
    ObsidianConverter "1" -- "1" FilenameSanitizer
    ObsidianConverter "1" -- "1" LinkRewriter
    ObsidianConverter "1" -- "1" MarkdownGenerator
    LinkRewriter "1" -- "1" GLOBAL_LINK_MAP # GLOBAL_LINK_MAP is a shared state, not a class instance
    ObsidianConverter ..> ContentData : uses
    ObsidianConverter ..> ProcessedNode : uses
```

#### 2.2 数据模型定义 (`models.py`)

*   **目的**: 封装和标准化在转换过程中传递的数据。
*   **开发要点**:
    *   定义 `ContentData` 类：用于表示文件或内部标题块的内容。
    *   定义 `ProcessedNode` 类：用于表示 JSON 中的文件或文件夹节点。
    *   **关键设计**: 引入一个全局字典 `GLOBAL_LINK_MAP: Dict[str, str]`，作为 `original_path` 到 `obsidian_link_name` 的映射。这个字典将在转换过程中动态填充，并供 `LinkRewriter` 使用。

#### 2.3 文件名处理 (`sanitizers.py`)

*   **目的**: 确保所有生成的文件名合法且唯一。
*   **开发要点**:
    *   **`_slugify(text: str)` 函数**: 将文本转换为文件系统友好的“slug”形式。
        *   **示例**: `"Chapter 1: Intro to AI/ML?"` -> `"chapter-1-intro-to-ai-ml"`
        *   **示例**: `"我的新知识！"` -> `"我的新知识"` (如果允许 Unicode)
    *   **`get_unique_filename(desired_name: str)` 函数**: 在 `_slugify` 的基础上，处理命名冲突，通过添加 `_1`, `_2` 等后缀确保唯一性。

#### 2.4 Markdown 生成 (`generator.py`)

*   **目的**: 负责将处理好的内容写入磁盘，并生成符合 Obsidian 规范的 YAML Frontmatter。
*   **开发要点**:
    *   **`generate_file(filepath: Path, main_title: str, content_body: str, raw_content_for_describe: str, aliases: Optional[List[str]] = None, frontmatter_fields: Optional[Dict[str, Any]] = None)` 方法**:
        *   根据提供的路径、主标题、文件主体内容 (`content_body`)、原始描述内容 (`raw_content_for_describe`) 和 Frontmatter 字段，生成 `.md` 文件。
        *   文件顶部将包含以 `---` 包裹的 YAML Frontmatter，字段包括 `title`, `aliases`, `describe` (截取 `raw_content_for_describe` 前 100 字)，以及预留的 `type`, `ends`, `version`, `over`, `tags` (目前置空)。
        *   Frontmatter 之后是 `content_body`，其将包含指向子标题的 Obsidian 双链。

#### 2.5 链接重写 (`link_rewriter.py`)

*   **目的**: 将原始 Markdown 内容中的相对路径链接转换为 Obsidian 双链。
*   **开发要点**:
    *   **`rewrite_links(markdown_content: str, current_file_original_path: Path) -> str` 方法**:
        *   **核心挑战：路径解析**: 这是该模块的难点。需要解析 Markdown 链接中的 `url`。如果 `url` 是相对路径（如 `../../path/to/file.md`），则需要结合 `current_file_original_path` (当前正在处理的原始文件的完整相对路径，例如 `optimizing/advanced_retrieval/advanced_retrieval.md`)，使用 `pathlib` 等工具将其解析为在 `GLOBAL_LINK_MAP` 中能查找的规范化路径。
        *   **查找与转换**: 使用解析后的规范化路径作为键，在 `GLOBAL_LINK_MAP` 中查找对应的 Obsidian 链接名。如果找到，将 `[text](url)` 转换为 `[[Obsidian Link Name|text]]`。
        *   **保留**: 外部链接 (`http://`, `https://`) 和未找到映射的内部链接应保持不变。
        *   **避免修改代码块**: 确保链接重写逻辑不会修改 Markdown 代码块内部的内容。

#### 2.6 核心转换逻辑 (`converter.py`)

*   **目的**: 协调所有模块，实现整个 JSON 到 Markdown 的转换流程，并根据新的结构化要求构建文件内容。
*   **开发要点**:
    *   **`ObsidianConverter` 类**: 作为主入口，协调 `sanitizer`, `link_rewriter`, `generator` 的工作。
    *   **递归处理**: 实现 `_process_node`, `_process_file`, `_process_section` 等递归方法。
        *   `_process_node`: 处理文件夹和文件节点，维护 `current_output_path` 和 `current_original_path`。
        *   `_process_file`: 处理单个文件节点，生成其主 Markdown 文件，并启动对其内部子标题的递归处理。
            *   **关键**: 在此阶段，将原始文件的完整相对路径和其生成的 Obsidian 链接名添加到 `GLOBAL_LINK_MAP`。
            *   **内容构建**: 提取 `level=1` 的内容作为 `describe` 的原始文本。遍历其子标题，计算并收集它们的 Obsidian 链接，作为主文件的 `content_body`。
        *   `_process_section`: 处理文件内部的每个子标题，将其生成为独立 Markdown 文件。
            *   **关键**: 在此阶段，将生成的章节文件对应的规范化路径（例如 `optimizing/advanced_retrieval/advanced-retrieval-query-transformations.md`）和其 Obsidian 链接名添加到 `GLOBAL_LINK_MAP`。
            *   **内容构建**: 提取当前章节的原始内容作为 `describe` 的原始文本。遍历其子标题（如果有），计算并收集它们的 Obsidian 链接，作为当前章节文件的 `content_body`。
            *   **移除父级链接**: 不再生成任何 `Parent File` 或 `Parent Section` 链接。

### 3. 转换流程示例 (输入 -> 输出)

为了更直观地理解转换过程，我们重温之前的示例，并展示新的输出格式：

#### 3.1 示例输入 (简化版 JSON 片段)

```json
{
    "name": "optimizing",
    "type": "folder",
    "children": [
        {
            "name": "advanced_retrieval",
            "type": "folder",
            "children": [
                {
                    "name": "advanced_retrieval.md",
                    "type": "file",
                    "content": {
                        "title": "Advanced Retrieval Strategies",
                        "level": 1,
                        "content": "Some top-level content for adv_retrieval.md.",
                        "children": [
                            {
                                "title": "Query Transformations",
                                "level": 2,
                                "content": "Info about query transformations. See [Query Transformations Docs](../../optimizing/advanced_retrieval/query_transformations.md).",
                                "children": []
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

#### 3.2 示例输出 (对应的文件结构与内容)

假设输出根目录为 `output_vault`。

```
output_vault/
├── optimizing/
│   └── advanced_retrieval/
│       ├── advanced-retrieval.md
│       └── advanced-retrieval-query-transformations.md
```

**文件内容示例：`output_vault/optimizing/advanced_retrieval/advanced-retrieval.md`**

```markdown
---
title: Advanced Retrieval Strategies
aliases: [advanced-retrieval]
describe: "Some top-level content for adv_retrieval.md."
type:
ends:
version:
over:
tags: []
---
[[advanced-retrieval-query-transformations]]
```

**文件内容示例：`output_vault/optimizing/advanced_retrieval/advanced-retrieval-query-transformations.md`**

```markdown
---
title: Query Transformations
aliases: [advanced-retrieval-query-transformations]
describe: "Info about query transformations. See [Query Transformations Docs](../../optimizing/advanced_retrieval/query_transformations.md)."
type:
ends:
version:
over:
tags: []
---
```

**`GLOBAL_LINK_MAP` 中的可能条目 (部分)**：

*   `"optimizing/advanced_retrieval/advanced_retrieval.md"` : `"advanced-retrieval"`
*   `"optimizing/advanced_retrieval/advanced_retrieval-Query Transformations"` : `"advanced-retrieval-query-transformations"`
*   `"optimizing/advanced_retrieval/query_transformations.md"` : `"query-transformations"` (假设这个文件在整个 JSON 结构中存在)

### 4. 测试策略

*   **单元测试**: 为 `sanitizers`, `link_rewriter` (其功能不变), `generator` 模块编写独立测试。
*   **集成测试**: 模拟完整的 JSON 输入，验证输出目录结构、文件内容、YAML Frontmatter 和链接的正确性。
*   **边缘情况测试**: 涵盖空内容、特殊字符、重名、深层嵌套、无子标题等场景。

### 5. 改进与完善

*   **错误处理**: 增加健壮的错误捕获和日志记录。
*   **配置项**: 允许用户自定义输出路径、链接格式、拆分级别、Frontmatter 字段内容等。
*   **性能优化**: 针对大型知识库进行优化。
*   **文档**: 编写清晰的 `README.md` 和 API 文档。
*   **打包**: 准备发布到 PyPI。

### 6. 开发流程建议

1.  **自底向上，逐步迭代**:
    *   从 `models.py` 开始，定义好数据结构。
    *   接着实现 `sanitizers.py` 和 `generator.py` (包含 YAML Frontmatter 逻辑)，并确保它们工作正常。
    *   **攻克 `link_rewriter.py`**: 这是最复杂的部分，尤其是其路径解析逻辑。务必确保其能够正确地将相对路径转换为 `GLOBAL_LINK_MAP` 中的键。
    *   最后构建 `converter.py`，将所有模块集成起来，从简单的 JSON 输入开始，逐步增加复杂性，特别关注新的内容构建逻辑。
2.  **测试先行**: 每完成一个小的功能点，立即编写并运行单元测试。
3.  **版本控制**: 始终使用 Git。

---
