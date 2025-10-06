// Simple test script to verify frontend can communicate with backend
async function testFrontendBackend() {
  try {
    console.log("Testing frontend-backend communication...");
    
    // Test strategy signal endpoint
    console.log("1. Testing strategy signal endpoint...");
    const signalResponse = await fetch("http://localhost:8000/strategy/signal?symbol=BTC-USD");
    const signalData = await signalResponse.json();
    console.log("Signal data:", signalData);
    
    // Test portfolio list endpoint
    console.log("2. Testing portfolio list endpoint...");
    const portfolioResponse = await fetch("http://localhost:8000/portfolio/list");
    const portfolioData = await portfolioResponse.json();
    console.log("Portfolio data:", portfolioData);
    
    // Test risk assessment endpoint
    console.log("3. Testing risk assessment endpoint...");
    const riskResponse = await fetch("http://localhost:8000/risk/assess?position_size=1500&account_balance=10000");
    const riskData = await riskResponse.json();
    console.log("Risk data:", riskData);
    
    console.log("All tests passed!");
  } catch (error) {
    console.error("Test failed:", error);
  }
}

testFrontendBackend();