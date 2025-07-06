from fastapi import FastAPI # clean architectgure Framework layer

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "LLearn API Server"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}