from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def home():
    return{"message":"Hello! My Python FastAPI web application is running successful."}
