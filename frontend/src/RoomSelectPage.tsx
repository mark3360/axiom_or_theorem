import TextBox from "./components/Textbox";
import getUserId from "./getUserId"
import { useNavigate } from "react-router-dom";
import { useState } from "react"





export default function RoomSelectPage() {

    function SubmitButton() {
        return (
            <button onClick={() => handleJoinRoom(roomcode)}>
            Join Room
            </button>
        );
    }

    const [roomcode, setRoomcode] =  useState<string>("") 

    const navigate = useNavigate();

    const handleJoinRoom = async(roomCode : string) => {
        try {
        const userId = getUserId() 
        // Join the room
            const joinResponse = await fetch(`/api/rooms/${roomCode}/join`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_id: userId,
                }),
            });

            if (!joinResponse.ok) {
                throw new Error("Failed to join room");
            }

            const joinResult = await joinResponse.json();

            if (joinResult.status !== "success") {
                throw new Error(joinResult.reason);
            }
            navigate(`/room/${roomCode}`);

        } catch (error) {
            console.error(error);
            return false
        }
    }

    const handleCreateRoom = async () => {
    try {
            const createResponse = await fetch("/api/rooms", {
                method: "POST",
            });

            if (!createResponse.ok) {
                throw new Error("Failed to create room");
            }

            const createResult = await createResponse.json();
            const roomCode = createResult.room_code;
            
            handleJoinRoom(roomCode);

        } catch (error) {
            console.error(error);
            return false
        }
    };

    return <>
        <h1>Axiom Or Theorem</h1>

        <div style={{margin: "20px"}} >
            <button onClick={handleCreateRoom}>Create Room</button>
        </div>


        <TextBox placeholder="Enter Room Code" value={roomcode} setValue={setRoomcode}/> <SubmitButton />
    </>
}