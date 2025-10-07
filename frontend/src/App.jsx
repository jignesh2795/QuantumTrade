import React from "react"; 
import Signal from "./features/Signal"; 
import Portfolio from "./features/Portfolio"; 
import Risk from "./features/Risk"; 
 
function App() { 
  return ( 
    <div style={{ padding: "2rem" }}> 
      <h1>QuantumTrade Frontend</h1> 
      <p>Your app is running! Connect to the backend API at <code>/api</code>.</p> 
      <Signal /> 
      <Portfolio /> 
      <Risk /> 
    </div> 
  ); 
} 
 
export default App; 
