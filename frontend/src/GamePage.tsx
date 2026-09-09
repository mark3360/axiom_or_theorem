
import MoveMakerHolder from './components/MoveMaker/MoveMakerHolder'
import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import getUserId from "./getUserId"
import AxiomsHolder from './components/AxiomsHolder/AxiomsHolder';

function GamePage() {
  const { roomCode } = useParams();
  const socketRef = useRef<WebSocket | null>(null);
  const [axioms, setAxioms] = useState<string[]>([])
  const [text, setText] =  useState<string>("")
  const [errorText, setErrorText] =  useState<string>("")
  const [gameStatusText, setGameStatusText] =  useState<string>("")
  const [winningProof, setWinningProof] = useState<string>("")


  useEffect(() => {
        const userId = getUserId();

        const socket = new WebSocket(
            `${import.meta.env.VITE_BACKEND_URL.replace(/^http/, "ws")}/ws/${roomCode}/${userId}`
        );

        socketRef.current = socket;

        socket.onopen = () => {
            console.log("Connected to room:", roomCode);
        };

        socket.onmessage = (event) => {
            const data: {whose_turn : string, messages? : string[]} | {"error" : string} | {"winning_proof" : string, "winning_player" : string} = JSON.parse(event.data);
            if ("error" in data) {
                console.log("ERROR", data)
                setErrorText(data["error"])
                return
            }
            setErrorText("")

            if ("winning_player" in data) {
                if (userId == data["winning_player"]) {
                    setGameStatusText("You Win!")
                } else {
                    setGameStatusText("You Lose.")
                }

                setWinningProof(data["winning_proof"])

                return 
            }

            if (data["whose_turn"] == userId) {
                setGameStatusText("Your Turn.")
            } else {
                setGameStatusText("Opponent is thinking.")
            }
            if (data.messages) {
                console.log("Received:", data["messages"]);
                setAxioms(data["messages"])
            }
        };

        socket.onclose = () => {
            console.log("Disconnected from room");
        };

        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        // Cleanup when leaving the page
        return () => {
            socket.close();
        };
    }, [roomCode]);
  return (
    <>
    <h1>Axiom or Theorem</h1>
    <div style={{margin: "20px"}}>
      <MoveMakerHolder text={text} setText={setText} socketRef={socketRef} />
    </div>

    <span style={{ color: "red" }}>{errorText}</span>
    <span>{gameStatusText}</span>

    <pre
        style={{
            fontFamily: "monospace",
            whiteSpace: "pre-wrap",
        }}
        >
        {winningProof}
    </pre>

    <div style={{margin: "20px"}}>
      <AxiomsHolder axioms={axioms} setText={setText} />
    </div>
    </>
  )
}

export default GamePage
