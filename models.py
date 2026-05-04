from pydantic import BaseModel, Field


class FinalResponse(BaseModel):
    answer: str = Field(description= "The answer for the query user asked")
    explanation: str = Field(description= "Explanation for the answer. This will be the exact text from the context provided")
    file_name: str = Field(description= "Name of the file for the context used")
    page_number: int = Field(description= "Page number of the context node")