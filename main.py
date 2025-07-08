import json
from src.Obsidian_Knowledge_Converter.converter import ObsidianConverter

def main():
    print("Starting Obsidian Knowledge Conversion...")

    # 示例输入 JSON 数据
    input_json_data = {
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
                            "content": "Some top-level content for adv_retrieval.md. See [Query Transformations Docs](../../optimizing/advanced_retrieval/query_transformations.md).",
                            "children": [
                                {
                                    "title": "Query Transformations",
                                    "level": 2,
                                    "content": "Info about query transformations. This is a sub-section.",
                                    "children": []
                                }
                            ]
                        }
                    },
                    {
                        "name": "query_transformations.md",
                        "type": "file",
                        "content": {
                            "title": "Query Transformations",
                            "level": 1,
                            "content": "This is a separate file about query transformations.",
                            "children": []
                        }
                    }
                ]
            }
        ]
    }

    output_directory = "./output_vault"
    converter = ObsidianConverter(output_directory)
    converter.convert(input_json_data)

    print(f"Conversion complete. Check the '{output_directory}' directory.")


if __name__ == "__main__":
    main()
