from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional
import uuid


class AnswerBase(BaseModel):
    user_id: str = Field(..., description="User UUID")
    text: str = Field(..., min_length=1, description="Answer text")
    
    @field_validator('text')
    def text_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Answer text cannot be empty')
        return v.strip()
    
    @field_validator('user_id')
    def validate_user_id(cls, v):
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('user_id must be a valid UUID')
        return v


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    question_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, description="Question text")
    
    @field_validator('text')
    def text_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Question text cannot be empty')
        return v.strip()


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionWithAnswers(Question):
    answers: List[Answer] = []