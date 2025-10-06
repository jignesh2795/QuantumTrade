export default function PortfolioCard({ asset }) {
  return (
    <div className="p-4 rounded-lg shadow-md bg-blue-50">
      <h3 className="font-bold text-lg">{asset.asset}</h3>
      <div className="mt-2">
        <p>Quantity: {asset.quantity}</p>
        <p>Avg Price: ${asset.avg_price.toFixed(2)}</p>
        <p>Value: ${(asset.quantity * asset.avg_price).toFixed(2)}</p>
      </div>
    </div>
  );
}
