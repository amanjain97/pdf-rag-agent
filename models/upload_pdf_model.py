from pydantic import BaseModel

class UploadPDFModel(BaseModel):
    file_path: str

class AskQuestionsModel(BaseModel):
    questions: list[str]
