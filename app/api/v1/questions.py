from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models import models
from ...schemas import schemas
from ...utils.logging import logger

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[schemas.Question])
def get_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all questions"""
    logger.info(f"Fetching questions: skip={skip}, limit={limit}")
    questions = db.query(models.Question).offset(skip).limit(limit).all()
    return questions


@router.post("/", response_model=schemas.Question, status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    """Create a new question"""
    logger.info(f"Creating new question: {question.text[:50]}...")
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    logger.info(f"Question created with id: {db_question.id}")
    return db_question


@router.get("/{question_id}", response_model=schemas.QuestionWithAnswers)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get a specific question with all its answers"""
    logger.info(f"Fetching question {question_id} with answers")
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        logger.warning(f"Question {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    """Delete a question and all its answers"""
    logger.info(f"Deleting question {question_id}")
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        logger.warning(f"Question {question_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(question)
    db.commit()
    logger.info(f"Question {question_id} deleted successfully")
    return None


@router.post("/{question_id}/answers/", response_model=schemas.Answer, status_code=status.HTTP_201_CREATED)
def create_answer(
    question_id: int,
    answer: schemas.AnswerCreate,
    db: Session = Depends(get_db)
):
    """Add an answer to a question"""
    logger.info(f"Creating answer for question {question_id}")
    
    # Check if question exists
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        logger.warning(f"Cannot create answer: Question {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")
    
    db_answer = models.Answer(**answer.dict(), question_id=question_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    logger.info(f"Answer created with id: {db_answer.id}")
    return db_answer