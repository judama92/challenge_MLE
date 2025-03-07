import fastapi
from fastapi import HTTPException
import logging
import pandas as pd
from pydantic import BaseModel, root_validator, ValidationError
from typing import List, Dict
import pickle
from challenge.model import DelayModel

app = fastapi.FastAPI()

model = DelayModel()
model.load_model("/workspaces/challenge_MLE/challenge/delay_model.pkl")

class FlightData(BaseModel):
    OPERA: str  # Puedes usar datetime si es necesario
    TIPOVUELO: str
    MES: int

@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(data: Dict[str, List[FlightData]]) -> dict:
    try:
        input_data = pd.DataFrame([item.dict() for item in data['flights']])
        print("Columnas recibidas:", input_data.columns)        
        
        # Llamamos al método de preprocesamiento del modelo
        preprocessed_data = model.preprocess(input_data)  # Asegúrate de que 'preprocess' esté funcionando
        predictions = model.predict(preprocessed_data)  # Predicción utilizando el modelo
        
        return {"predict": predictions}  # Asegúrate de que sea un formato adecuado para el cliente

    except Exception as e:
        logging.exception("An error occurred during prediction")
        raise HTTPException(status_code=500, detail="An internal error occurred")