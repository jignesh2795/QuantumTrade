// Comprehensive test to check frontend-backend communication
async function testConnection() {
  console.log("Testing connection to backend...");
  
  try {
    // Test basic connectivity
    console.log("1. Testing basic connectivity...");
    const response = await fetch("http://localhost:8000/health");
    const healthData = await response.json();
    console.log("Health check:", healthData);
    
    // Test portfolio endpoint
    console.log("2. Testing portfolio endpoint...");
    const portfolioResponse = await fetch("http://localhost:8000/portfolio/list");
    const portfolioData = await portfolioResponse.json();
    console.log("Portfolio data:", portfolioData);
    
    // Test CORS headers
    console.log("3. Checking CORS headers...");
    console.log("Response headers:", [...portfolioResponse.headers.entries()]);
    
    console.log("All tests passed!");
  } catch (error) {
    console.error("Test failed:", error);
  }
}

testConnection();