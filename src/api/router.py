from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history
from src.logger import log_message

router = APIRouter(prefix="/api" ,tags=["water_intake"])

agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id : str
    intake_ml : int

@router.post("/water_intake")
def add_water_intake(request:WaterIntakeRequest):
    log_intake(request.user_id,request.intake_ml)
    analysis = agent.analyze_intake(intake_ml=request.intake_ml)
    log_message(f"user {request.user_id} logged {request.intake_ml}")
    return {"message": "Water intake logged successfully", "analysis": analysis}

@router.get("/history/{user_id}")
def get_history(user_id:str):
    history = get_intake_history(user_id)
    return {"user_id":user_id,"message": history}