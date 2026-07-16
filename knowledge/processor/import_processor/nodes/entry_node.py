import logging

from knowledge.processor.import_processor.base import BaseNode, T
from knowledge.processor.import_processor.exceptions import StateFieldError, ValidationError
from knowledge.processor.import_processor.state import ImportGraphState
from pathlib import Path

class EntryNode(BaseNode):
    name = "entry_node"
    def process(self, state: ImportGraphState) -> ImportGraphState:

        #获取state中的文件路径，还有文件url
        import_file_path = state.get("import_file_path")
        file_dir = state.get("file_dir")
        if not import_file_path :
            self.logger.error("导入文件路径不存在1")
            raise StateFieldError(node_name=self.name,field_name=import_file_path,expected_type=str)
        if not file_dir:
            self.logger.error("文件目录不存在1")
            raise StateFieldError(node_name=self.name, field_name=file_dir,expected_type=str)

        import_file_path_obj=Path(import_file_path)
        file_dir_obj=Path(file_dir)
        if not import_file_path_obj.exists() :
            self.logger.error("导入文件路径不存在2")
            raise StateFieldError(node_name=self.name,field_name=import_file_path,expected_type=str)
        if not file_dir_obj:
            self.logger.error("文件目录不存在2")
            raise StateFieldError(node_name=self.name, field_name=file_dir,expected_type=str)

        #拿后缀
        file_suffix = import_file_path_obj.suffix

        if file_suffix==".pdf":
            state["is_pdf_read_enabled"]=True
            state["pdf_path"]=import_file_path

        elif file_suffix==".md":
            state["is_md_read_enabled"]=True
            state["md_path"]=import_file_path
        else:
            self.logger.error(f"不支持的文件类型{file_suffix}")
            raise ValidationError(message="不支持这个文件格式",node_name=self.name)

        #获取文件名
        state["file_title"]=import_file_path_obj.stem

        return state


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    entry_node=EntryNode()

    init_state={
        "import_file_path": "test.pdf",
        "file_dir": "test_dir"
    }

    state=entry_node(init_state)