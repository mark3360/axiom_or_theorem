
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import RoomSelectPage from './RoomSelectPage';
import GamePage from './GamePage'



function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RoomSelectPage/>} />
        <Route path="/room/:roomCode"  element={<GamePage/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
