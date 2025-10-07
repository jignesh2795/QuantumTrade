from api.server import app

def check_routes():
    print("Available routes:")
    for route in app.routes:
        print(f"  {route.methods} {route.path} -> {route.name}")

if __name__ == "__main__":
    check_routes()