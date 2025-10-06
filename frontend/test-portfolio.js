// Simple test script to verify frontend can communicate with backend
async function testPortfolio() {
  try {
    console.log("Testing portfolio API call...");
    const response = await fetch("http://localhost:8000/portfolio/list");
    const data = await response.json();
    console.log("Success! Received data:", data);
  } catch (error) {
    console.error("Error:", error);
  }
}

testPortfolio();