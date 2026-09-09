import CodeEditorHolder from "../CodeEditorComponents/CodeEditorHolder"
import getUserId from "../../getUserId";

interface MoveMakerHolderProps {
    socketRef: React.RefObject<WebSocket | null>;
    text: string
    setText: React.Dispatch<React.SetStateAction<string>>
}


export default function MoveMakerHolder({ socketRef, text, setText }: MoveMakerHolderProps)  {

    const userId = getUserId()
    const handleSendMessage = (mode : string) => {
        
        const the_json = {
          "userId" : userId,
          "mode" : mode,
          "text" : text
        }

        socketRef.current?.send(JSON.stringify(the_json));
    };


    return <>
        <CodeEditorHolder code={text} setCode={setText} onSubmitFunction={handleSendMessage}/>
    </>
}