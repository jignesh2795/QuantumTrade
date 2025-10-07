"""
Mock Model Server for QuantumTrade Platform
This is a placeholder implementation to allow the application to run
"""


def load_model(model_name):
    """Mock function to load a model"""
    print(f"Loading model: {model_name}")
    return {"model_name": model_name, "type": "mock"}


def predict(model, data):
    """Mock function to make predictions"""
    print(f"Making prediction with model: {model.get('model_name', 'unknown')}")
    # Return a random prediction (0 or 1)
    import random

    return random.choice([0, 1])
