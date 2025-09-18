from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from ...models import models
from ...schemas import schemas
from ...utils.logging import logger

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}", response_model=schemas.Answer)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    """Get a specific answer"""
    logger.info(f"Fetching answer {answer_id}")
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        logger.warning(f"Answer {answer_id} not found")
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    """Delete an answer"""
    logger.info(f"Deleting answer {answer_id}")
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        logger.warning(f"Answer {answer_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Answer not found")
    
    db.delete(answer)
    db.commit()
    logger.info(f"Answer {answer_id} deleted successfully")
    return None