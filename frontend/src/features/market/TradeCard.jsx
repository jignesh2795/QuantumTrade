export default function TradeCard({ trade }) {
  return (
    <div className={`p-4 rounded-lg shadow-md ${trade.trade_type === 'BUY' ? 'bg-green-100' : 'bg-red-100'}`}>
      <div className="flex justify-between">
        <h3 className="font-bold">{trade.asset}</h3>
        <span className={`font-semibold ${trade.trade_type === 'BUY' ? 'text-green-800' : 'text-red-800'}`}>
          {trade.trade_type}
        </span>
      </div>
      <div className="mt-2">
        <p>Amount: {trade.amount}</p>
        <p>Price: ${trade.price.toFixed(2)}</p>
        <p className="text-sm text-gray-500">
          {new Date(trade.timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
}
