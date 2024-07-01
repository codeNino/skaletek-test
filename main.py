# from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import numpy as np
from enum import Enum
import uvicorn
import warnings
from config import Config
from security import verify_auth_header

# Ignore all UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)


class EmbarkEnum(Enum):
  C = "C"
  Q = "Q"
  S = "S"

class GenderEnum(Enum):
  MALE = "male"
  FEMALE = "female"

class PredictionInput(BaseModel): 
    Pclass: int = Field(..., gt=0, lt=4) # passenger class ranges from 1 to 3
    Sex : GenderEnum
    Age : int = Field(..., gt=0, lt=100) # set age boundary between 0 and 100 
    SibSp : int = Field(..., ge=0, lt=20) # siblings range from 0 to probable upper limit of 20
    Parch : int = Field(..., ge=0, le=2)  # parentchild ranges from 0 to 2
    Fare  : float = Field(..., gt=0, lt=1000) # fare is between 0 and 1000
    Embarked : EmbarkEnum  


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


survival_model = pickle.load(open('classifier.pkl', 'rb'))

@app.post("/api/v1/predict", dependencies=[Depends(verify_auth_header)])
def predict_survival(request: PredictionInput):
  try:
    embarked_C = True if request.Embarked == EmbarkEnum.C else False
    embarked_Q = True if request.Embarked == EmbarkEnum.Q else False
    embarked_S = True if request.Embarked == EmbarkEnum.S else False

    sex = 1 if request.Sex == GenderEnum.MALE else 0

    attrs = np.array([[request.Pclass, sex, request.Age, request.SibSp,
                       request.Parch, request.Fare, embarked_C, embarked_Q, embarked_S]])
    prediction = survival_model.predict(attrs)
    survived = "Yes" if prediction == 1 else "No"
    return JSONResponse(content={"Survived": survived}, status_code=200)
  except Exception as e:
    print("Error occured while predicting titanic survival ::: ", str(e))
    return JSONResponse(content={"error" : "Internal Server Error"}, status_code=500)


if __name__=="__main__":
  if Config.ENV.is_local:
    uvicorn.run("main:app", host="0.0.0.0", port=Config.PORT, reload=True)
  else:
    uvicorn.run("main:app", host="0.0.0.0")