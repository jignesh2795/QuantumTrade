from fastapi import FastAPI
from fastapi.routing import APIRoute
from api.routes import router

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    print("Server started")
    print("Available routes:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"  {route.methods} {route.path} -> {route.name}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)