from fastapi import FastAPI, HTTPException
from app.schemas.predict import TransactionRequest
from app.services.predict import predict_transaction
from app.model.loadmodel import  metadata

app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_version":metadata["version"],
        "model_type":metadata["model_type"],
        }

    
@app.post("/predict")
def predict(request: TransactionRequest):
    try:
        input_data = request.model_dump()
        result = predict_transaction(input_data)
    except ValueError as e:
        raise HTTPException(status_code=422,detail=str(e))    
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f"Predition error:{str(e)}")
    return{
        **result,
        "threshold":metadata["threshold"],
        "model_version" : metadata["version"],
    }