```python
import os
from src.database import DB_CONNECTION
from src.api_integration import integrateAPI
from src.networking import networkClonedUser
from src.utils import CloneTrainingStarted

def startCloneTraining(user_id):
    user = DB_CONNECTION.find_one({"_id": user_id})
    if not user:
        raise Exception("User not found")

    clone_data = integrateAPI(user["api_key"])
    if not clone_data:
        raise Exception("Failed to fetch clone data")

    clone_id = DB_CONNECTION.insert_one(clone_data).inserted_id
    if not clone_id:
        raise Exception("Failed to save clone data")

    network_status = networkClonedUser(clone_id)
    if not network_status:
        raise Exception("Failed to network clone")

    CloneTrainingStarted.emit(clone_id)

    return clone_id
```