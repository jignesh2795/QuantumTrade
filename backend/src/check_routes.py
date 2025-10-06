from api.server import app
from fastapi.routing import APIRoute

def check_routes():
    print("Available routes:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"  {route.methods} {route.path} -> {route.name}")
        else:
            print(f"  {route}")

if __name__ == "__main__":
    check_routes()