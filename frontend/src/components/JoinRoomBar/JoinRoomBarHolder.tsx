import TextBox from "../Textbox";
import { useState } from "react"

function SubmitButton() {
  return (
    <button onClick={() => console.log("Submitted")}>
      Join Room
    </button>
  );
}

export default function JoinRoomBarHolder() {
    const [text, setText] =  useState<string>("") 
    return <>
        <TextBox placeholder="Enter Room Code" value={text} setValue={setText}/> <SubmitButton />
    </>
}