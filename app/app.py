from fastapi import FastAPI
from fastapi.params import Body
from firebase_admin import messaging, db
from fastapi.exceptions import HTTPException
import time


app = FastAPI(title="Gleak Backend")


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.put("/{id}/isAlerting", response_model=bool)
async def setIsAlerting(id: str, value: bool = Body(...)) -> bool:
    alertRef = db.reference(f"{id}/isAlerting")
    valRef = db.reference(f"{id}/value")
    notificRef = db.reference(f"{id}/notifications")

    val: bool = alertRef.get()

    if (val is None):
        raise HTTPException(400, "Invalid Serial ID")

    if (val != value):
        alertRef.set(value)

        if (value):

            notificData = {
                'title': 'Alert! Gas Leak!',
                'body': f'Sensor reads {valRef.get()}',
                'time': round(time.time())
            }

            notific = messaging.Notification(
                    title=notificData['title'],
                    body=notificData['body'])

            # print(messaging.send(messaging.Message(
            #     notification=notific, topic=id)))

            notificRef.push(value=notificData)

    return value



@app.put("/{id}/value", response_model=int)
def setCurrentVal(id: str, value: int = Body(...)): 
    alertRef = db.reference(f"{id}/isAlerting")
    valRef = db.reference(f"{id}/value")

    val: bool = alertRef.get()

    if (val is None):
        raise HTTPException(400, "Invalid Serial ID")

    valRef.set(value)

    return value