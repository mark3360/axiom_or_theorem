import { useState } from "react";

interface AxiomListProps {
    axioms: string[];
    setText: React.Dispatch<React.SetStateAction<string>>,
}



export default function AxiomList({ axioms, setText }: AxiomListProps) {
    const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

    const handleClick = (k: number) => {
        const hypothesisNames = [
            ...Array.from({ length: axioms.length }, (_, i) => i)
                .filter(i => i !== k),
            k,
        ].map(i => `h${i + 1} (D := D)`);


        const implication1 = hypothesisNames.join(" -> ");

        hypothesisNames[hypothesisNames.length -1] = "Not (" + hypothesisNames.at(-1) + ")" 

        const implication2 = hypothesisNames.join(" -> ");

        const code = `theorem challenge : Or (${implication1}) (${implication2}) := by`;
        console.log(code)
        setText(code);
    };

    return (
        <div>
            {axioms.map((axiom, index) => (
                <div
                    key={index}
                    onMouseEnter={() => setHoveredIndex(index)}
                    onMouseLeave={() => setHoveredIndex(null)}
                    onClick={() => handleClick(index)}
                    style={{
                        fontFamily: "monospace",
                        border: "1px solid black",
                        padding: "8px",
                        marginBottom: "8px",
                        cursor: "pointer",
                        backgroundColor:
                            hoveredIndex === index ? "rgba(255, 255, 255, 0.08)" : "transparent",
                    }}
                >
                    {axiom}
                </div>
            ))}
        </div>
    );
}
