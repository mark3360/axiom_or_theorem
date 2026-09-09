import CodeEditor from "./CodeEditor"

export default function CodeEditorHolder({
    code,
    setCode, 
    onSubmitFunction
} : {
    code : string
    setCode: React.Dispatch<React.SetStateAction<string>>,
    onSubmitFunction : (arg0 : string) => void
}) {
    return <>
        <CodeEditor code={code} setCode={setCode}/>

        <button onClick={() => {onSubmitFunction("add")}}>Add Axiom</button>
        <button onClick={() => {onSubmitFunction("challenge")}}>Challenge</button>
    </>
}