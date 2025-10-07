import { useEffect, useState } from "react";

const PriceTicker = ({
  symbols = ["BTC-USD", "ETH-USD", "AAPL", "GOOGL", "TSLA"],
}) => {
  const [prices, setPrices] = useState({});
  const [changes, setChanges] = useState({});

  // Simulate real-time price updates
  useEffect(() => {
    const generatePrices = () => {
      const newPrices = {};
      const newChanges = {};

      symbols.forEach((symbol) => {
        // Generate a random price based on symbol
        let basePrice;
        switch (symbol) {
          case "BTC-USD":
            basePrice = 45000;
            break;
          case "ETH-USD":
            basePrice = 3000;
            break;
          case "AAPL":
            basePrice = 150;
            break;
          case "GOOGL":
            basePrice = 2500;
            break;
          case "TSLA":
            basePrice = 200;
            break;
          default:
            basePrice = 100;
        }

        // Add some random fluctuation
        const changePercent = (Math.random() - 0.5) * 0.02; // ±1% change
        const newPrice = basePrice * (1 + changePercent);
        const change = newPrice - basePrice;

        newPrices[symbol] = newPrice;
        newChanges[symbol] = {
          value: change,
          percent: changePercent * 100,
        };
      });

      setPrices(newPrices);
      setChanges(newChanges);
    };

    // Generate initial prices
    generatePrices();

    // Update prices every 5 seconds
    const interval = setInterval(generatePrices, 5000);

    return () => clearInterval(interval);
  }, [symbols]);

  return (
    <div className="price-ticker">
      <div className="ticker-header">
        <h3>Live Prices</h3>
      </div>
      <div className="ticker-content">
        {symbols.map((symbol) => (
          <div key={symbol} className="ticker-item">
            <div className="symbol">{symbol}</div>
            <div className="price">${prices[symbol]?.toFixed(2) || "0.00"}</div>
            <div
              className={`change ${
                changes[symbol]?.value >= 0 ? "positive" : "negative"
              }`}
            >
              {changes[symbol]?.value >= 0 ? "+" : ""}
              {changes[symbol]?.value?.toFixed(2) || "0.00"}(
              {changes[symbol]?.percent >= 0 ? "+" : ""}
              {changes[symbol]?.percent?.toFixed(2) || "0.00"}%)
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PriceTicker;
