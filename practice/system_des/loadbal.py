from fastapi import FastAPI
from redis import Redis
from prometheus_client import Counter, Histogram, start_http_server
import random

app = FastAPI()
cache = Redis(host='redis', port=6379)
predictions_total = Counter('predictions_total', 'Total predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction Latency')

@app.post("/predict")
async def predict(data: dict):
    cache_key = f"predict:{data['input']}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return {"prediction": cached_result.decode('utf-8'), "version": "cached"}
    
    with prediction_latency.time():
        model_version = "v1" if random.random() < 0.9 else "v2"
        model = model_v1 if model_version == "v1" else model_v2
        result = model.predict(data["input"])

    cache.setex(cache_key, 3600, result)
    predictions_total.inc()
    return {"prediction": result, "version": model_version}

start_http_server(8001)
