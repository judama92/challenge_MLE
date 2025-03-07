import fastapi
from fastapi import HTTPException
import logging
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict
from challenge.model import DelayModel

app = fastapi.FastAPI()

model = DelayModel()
model.load_model("/workspaces/challenge_MLE/challenge/delay_model.pkl")
valid_airlines = [
    'American Airlines', 'Air Canada', 'Air France', 'Aeromexico', 'Aerolineas Argentinas',
    'Austral', 'Avianca', 'Alitalia', 'British Airways', 'Copa Air', 'Delta Air', 'Gol Trans',
    'Iberia', 'K.L.M.', 'Qantas Airways', 'United Airlines', 'Grupo LATAM', 'Sky Airline',
    'Latin American Wings', 'Plus Ultra Lineas Aereas', 'JetSmart SPA', 'Oceanair Linhas Aereas',
    'Lacsa'
]

class FlightData(BaseModel):
    OPERA: str
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

def validate_month(data: pd.DataFrame) -> None:
    """
    Validates if the values in the 'MES' column are between 1 and 12.
    
    Args:
        data (pd.DataFrame): The input data to validate the 'MES' column.
    
    Raises:
        HTTPException: If any value in the 'MES' column is outside the range [1, 12], 
                        an HTTP error with code 400 is raised.
    """
    if not data["MES"].between(1, 12).all():
        raise HTTPException(status_code=400, detail="The 'MES' column should be between 1 and 12.")
    
def validate_tipovuelo(data: pd.DataFrame) -> None:
    """
    Validates if the values in the 'TIPOVUELO' column are 'I' or 'N'.
    
    Args:
        data (pd.DataFrame): The input data to validate the 'TIPOVUELO' column.
    
    Raises:
        HTTPException: If any value in the 'TIPOVUELO' column is neither 'I' nor 'N',
                        an HTTP error with code 400 is raised.
    """
    invalid_values = data[~data["TIPOVUELO"].isin(["I", "N"])]
    if not invalid_values.empty:
        raise HTTPException(status_code=400, detail="Invalid 'TIPOVUELO' should be 'I' or 'N'.")

def validate_airline(data: pd.DataFrame):
    """
    Validates that the 'OPERA' column of the input DataFrame contains only valid airline names.

    Args:
        data (pd.DataFrame): The input DataFrame containing flight data. It must have a column 'OPERA'
                              that represents the airline name.

    Raises:
        HTTPException: If any airline name in the 'OPERA' column is not valid, it raises an HTTPException
                        with status code 400 and a detailed error message.
    """
    invalid_airlines = data[~data['OPERA'].isin(valid_airlines)]
    if not invalid_airlines.empty:
        raise HTTPException(status_code=400, detail="Invalid airline name in 'OPERA' column")

@app.post("/predict", status_code=200)
async def post_predict(data: Dict[str, List[FlightData]]) -> dict:    
    try:
        input_data = pd.DataFrame([item.dict() for item in data['flights']])
        validate_month(input_data)
        validate_tipovuelo(input_data)
        validate_airline(input_data)
        preprocessed_data = model.preprocess(input_data)
        predictions = model.predict(preprocessed_data)
        
        return {"predict": predictions}

    except HTTPException as e:
        logging.warning(f"Validation error: {e.detail}")
        raise e

    except Exception as e:
        logging.exception("An error occurred during prediction")
        raise HTTPException(status_code=500, detail="An internal error occurred")