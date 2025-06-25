# from app.db.mongodb import get_database
from app.db.db import db
from app.models.metrics_model import ExperimentMetrics
from bson import ObjectId

# db = get_database()
test_metrics_collection = db.experiment_metrics
metrics_collection = db.automation_metrics

async def create_metric(metric: ExperimentMetrics):
    # return await metrics_collection.insert_one(metric.model_dump())
    # Convert to dict, alias _id, but EXCLUDE the model's `id` field
    data = metric.model_dump(by_alias=True, exclude={"id"})
    return await metrics_collection.insert_one(data)

async def get_metrics(skip: int = 0, limit: int = 100):
    # metrics = list(metrics_collection.find().skip(skip).limit(limit))
    cursor = metrics_collection.find().skip(skip).limit(limit)
    metrics = []
    # Convert ObjectId to string
    # async for metric in cursor:
    #     metric["_id"] = str(metric["_id"])
    #     metrics.append(metric)
    async for doc in cursor:
        # Pull out Mongo's _id, stringify it, and rename to "id"
        doc["id"] = str(doc.pop("_id"))
        metrics.append(doc)
    return metrics

async def get_metric_by_id(metric_id: str) -> dict | None:
    # return metrics_collection.find_one({"_id": ObjectId(metric_id)})
    """
    Fetch a single metric by its string ID. Returns a dict with 'id' field,
    or None if not found.
    """
    doc = await metrics_collection.find_one({"_id": ObjectId(metric_id)})
    if not doc:
        return None
    # Convert Mongo’s _id to string and rename
    doc["id"] = str(doc.pop("_id"))
    return doc

async def update_metric_success(metric_id: str, success: bool):
    """
    Sets the 'success' field of the given metric to True/False.
    Returns the update result.
    """
    result = await metrics_collection.update_one(
        {"_id": ObjectId(metric_id)},
        {"$set": {"success": success}}
    )
    return result
