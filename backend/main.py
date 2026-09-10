from fastapi import Depends, FastAPI, WebSocket
import subprocess
import os
import uuid
import shutil
from database import engine, Base, get_db, SessionLocal
from game import *
import models
from models import Room, Messages
import random
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from check_lean_proof import check_lean_proof
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://axiom-or-theorem.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

message_connections = {}

class JoinRoomRequest(BaseModel):
    user_id: str


@app.get("/")
def read_root():
    return {"message": "Hello!"}


@app.post("/execute")
def execute(json: dict):
    code = json["code"]

    result = check_lean_proof(code)
    return result


@app.post("/rooms")
def create_room(db: Session = Depends(get_db)):
    room_code = ""
    for _ in range(4):
        x = random.randint(0,25)
        c = chr(x + ord('A'))
        room_code += c

    room = Room(code = room_code)
    db.add(room)
    db.commit()

    return {"room_code" : room_code}

@app.post("/rooms/{room_code}/join")
def join_room(room_code : str, request: JoinRoomRequest,  db : Session = Depends(get_db)):
    room = db.get(Room, room_code)

    if room is None:
        return {"status" : "error", "reason" : "Room does not exist."}
    
    # Now that we have the room, check to see if player 1 is taken.

    if room.p1_id is None:
        room.p1_id = request.user_id 
        db.commit()
        return {"status" : "success", "is_player_1" : True}

    elif room.p2_id is None:
        room.p2_id = request.user_id
        db.commit()
        return {"status" : "success", "is_player_1" : False}
    else:
        return {"status" : "error", "reason" : "Room full."}

@app.websocket("/ws/{room_code}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, user_id: str):
    await websocket.accept()

    db = SessionLocal()
    room = db.get(Room, room_code)


    if room is None:
        await websocket.send_json({
            "status": "error",
            "reason": "Invalid Room Code."
        })
        await websocket.close()
        return

    if room_code not in message_connections:
        message_connections[room_code] = {}
        message_connections[room_code][user_id]  = websocket
    else:
        message_connections[room_code][user_id] =  websocket
    

    await websocket.send_json({"whose_turn" : (room.p1_id if room.is_p1_turn else room.p2_id)})
    try:
        while True:
            message_json = await websocket.receive_json()

            print(f"Message Json {message_json}")
            message_text = message_json['text']
            message_userId = message_json["userId"]
            message_mode = message_json["mode"]
            
            room = db.get(Room, room_code)
            db.refresh(room)


            # Players may only send messages during their turn
            
            if room.is_p1_turn:
                if room.p1_id != message_userId:
                    await websocket.send_json({"error" : "Not your turn"})
                    continue
            else:
                if room.p2_id != message_userId:
                    await websocket.send_json({"error" : "Not your turn"})
                    continue
            
            

            # Check what they are actually submitting.
            if message_mode == "add":
                result = check_valid_axiom(message_text)

                print("result:", result)

                if not result:
                    await websocket.send_json({"error" : "Axiom contains illegal characters"})
                    continue
                if not result['success']:
                    await websocket.send_json({"error" : "Invalid logical statement"})
                    continue

                # If we reach here, the axiom is good, and is ready to be added to the game. 
                the_axiom = result['stdout']
                the_axiom = the_axiom.slice(the_axiom.indexOf("def"));

                the_axiom = the_axiom[:5] + str(room.num_messages + 1) + the_axiom[5:]

                room.num_messages += 1

                # Flip the turn 
                room.is_p1_turn = not room.is_p1_turn


                # Save the message to the DB.
                message = Messages(
                    code=room_code,
                    player_id=user_id,
                    message=the_axiom
                )

                db.add(message)
                db.commit()

                
                # Fetch all entries for that room in the database.
                stmt = (
                    select(Messages)
                    .where(Messages.code == room_code)
                    .order_by(Messages.created_at)
                )
                messages_in_db = db.scalars(stmt).all()

                data = {
                    "whose_turn" : (room.p1_id if room.is_p1_turn else room.p2_id),
                    "messages" : [ msg.message for msg in messages_in_db]
                }

                # Send the list of all messages to other participants.
                for other_user, connection in message_connections[room_code].items():
                    await connection.send_json(data)

            elif message_mode == "challenge":
                # Fetch all entries for that room in the database.
                stmt = (
                    select(Messages)
                    .where(Messages.code == room_code)
                    .order_by(Messages.created_at)
                )
                messages_in_db = db.scalars(stmt).all()

                axioms = [
                    {
                        "message": msg.message
                    }
                    for msg in messages_in_db
                ]
                print(f"Pre message text {message_text}")
                result = check_valid_challenge(message_text, axioms)

                if not result['success']:
                    await websocket.send_json({"error" : "Incorrect Proof"})
                    continue
                if not is_challenge(result['stdout'], room.num_messages):
                    await websocket.send_json({"error" : "challenge signature differs from expected"})
                    continue

                # If we reach here, the game is complete.
                for other_user, connection in message_connections[room_code].items():
                    await connection.send_json({"winning_proof" : message_text, "winning_player" : user_id})
                
                break
    finally:
        message_connections[room_code].pop(user_id, None)

        if not message_connections[room_code]:
            del message_connections[room_code]
            db.delete(room)
            db.commit()
        
        db.close()

