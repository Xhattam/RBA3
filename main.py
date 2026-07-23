from fastapi import Depends, HTTPException, status, FastAPI, Request
from fastapi.exceptions import RequestValidationError


app = FastAPI(name="RBA3 - Reading Berkshire Archives Automation App")

@app.get("/health")
def health_check():
    return {"status": "ok"}