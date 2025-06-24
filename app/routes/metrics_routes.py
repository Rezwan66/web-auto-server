from fastapi import APIRouter, HTTPException
# from app.db.mongodb import get_database  # Add this import, adjust the path as needed
from app.db.db import db
from app.utils.crud.metrics_crud import create_metric, get_metrics, get_metric_by_id
from app.models.metrics_model import ExperimentMetrics

router = APIRouter()

@router.get("/test-connection")
async def test_connection():
    try:
        # db = get_database()
        await db.command('ping')
        return {"status": "success", "message": "✅Connected to MongoDB Atlas!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {str(e)}")

@router.post("/test-metric")
async def create_test_metric():
    # Create a test metric
    test_metric = ExperimentMetrics(
        use_case="Form Filling",
        context_level="A",
        iteration=1,
        prompt="Test prompt",
        url="http://localhost:5173/form",
        success=True,
        total_duration_ms=123456789,
        api_time_ms=150
    )
    # Save to MongoDB
    result = await create_metric(test_metric)
    return {
        "status": "success",
        "metric_id": str(result.inserted_id)
    }

@router.get("/test-metric")
async def read_test_metric():
    # Read from MongoDB
    result = await get_metrics()
    print(result)
    return result

@router.get("/test-metric/{metric_id}")
async def read_test_metric_by_id(metric_id: str):
    """
    Retrieve a single ExperimentMetrics by its ID.
    """
    metric = await get_metric_by_id(metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found.")
    return metric
