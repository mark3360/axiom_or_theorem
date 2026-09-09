import AxiomList from "./AxiomsList"

interface AxiomListProps {
    axioms: string[];
    setText: React.Dispatch<React.SetStateAction<string>>,
}


export default function AxiomsHolder({axioms, setText} : AxiomListProps) {
    return (<>
        <h2>Current Axioms</h2>
        <AxiomList axioms={axioms} setText={setText}/>
    </>
    )
}