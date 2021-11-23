from fastapi import FastAPI
from fastapi.params import Body
from firebase_admin import messaging, db
from fastapi.exceptions import HTTPException


app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.put("{id}/isAlerting")
async def setIsAlerting(id: int, value: Body(bool)) -> dict:
    ref = db.reference(f"{id}/isAlerting")
    val: bool = ref.get()

    if (val is None):
        raise HTTPException(400, "Invalid Serial ID")

    if (val != value):
        ref.set_if_unchanged(value)

        if (value):
            messaging.Message(topic=str(id)).send()


