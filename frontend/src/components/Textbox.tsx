type TextBoxProps = {
  placeholder?: string;
  value: string;
  setValue: React.Dispatch<React.SetStateAction<string>>;
};

export default function TextBox({ placeholder, value, setValue }: TextBoxProps) {
  return (
    <input
      type="text"
      value={value}
      onChange={(e) => setValue(e.target.value)}
      placeholder={placeholder}
      style={{
        fontFamily: "monospace",
        fontSize: "14px",
        width: "100%",
        padding: "8px 12px",
        boxSizing: "border-box",
      }}
    />
  );
}