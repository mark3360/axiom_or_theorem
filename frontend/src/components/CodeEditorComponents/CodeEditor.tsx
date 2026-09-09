import Editor from "@monaco-editor/react";

export default function CodeEditor({
  code,
  setCode
}: {
  code: string
  setCode: React.Dispatch<React.SetStateAction<string>>;
}) {
  return (
    <Editor
      height="500px"
      defaultLanguage="python"
      theme="vs-dark"
      value={code}
      onChange={(value) => setCode(value ?? "")}
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        automaticLayout: true,
      }}
    />
  );
}