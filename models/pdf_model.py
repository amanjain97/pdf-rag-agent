from pydantic import BaseModel
class PDFModel(BaseModel):
    file_path: str

class QuestionsModel(BaseModel):
    questions: list[str]
