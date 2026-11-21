import uvicorn

def run_server():
    uvicorn.run("app.main:app", reload=True)
