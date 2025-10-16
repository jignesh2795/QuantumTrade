'use client'

import { useEffect, useState } from 'react'
import { TrendingUp, TrendingDown, Clock } from 'lucide-react'
import axios from 'axios'

interface Trade {
  id: string
  timestamp: string
  symbol: string
  side: string
  quantity: number
  price: number
  pnl: number
  strategy: string
}

export default function TradeHistory() {
  const [trades, setTrades] = useState<Trade[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTrades()
    const interval = setInterval(fetchTrades, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchTrades = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/analytics/trades')
      setTrades(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching trades:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="glass rounded-xl p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-dark-800 rounded w-1/3" />
          <div className="space-y-2">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="h-16 bg-dark-800 rounded" />
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="glass rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Trade History</h2>
        <button className="text-primary-500 text-sm hover:text-primary-400">
          View All
        </button>
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {trades.map((trade) => (
          <TradeRow key={trade.id} trade={trade} />
        ))}

        {trades.length === 0 && (
          <div className="text-center py-12 text-dark-400">
            <Clock className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>No trades yet</p>
          </div>
        )}
      </div>
    </div>
  )
}

function TradeRow({ trade }: { trade: Trade }) {
  const isBuy = trade.side === 'buy'
  const isProfitable = trade.pnl > 0
  const timeAgo = getTimeAgo(new Date(trade.timestamp))

  return (
    <div className="flex items-center justify-between p-3 bg-dark-900 rounded-lg hover:bg-dark-800 transition-colors">
      <div className="flex items-center space-x-3">
        <div className={`p-2 rounded-lg ${isBuy ? 'bg-success/20' : 'bg-danger/20'}`}>
          {isBuy ? (
            <TrendingUp className={`w-4 h-4 ${isBuy ? 'text-success' : 'text-danger'}`} />
          ) : (
            <TrendingDown className="w-4 h-4 text-danger" />
          )}
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-semibold">{trade.symbol}</span>
            <span className={`text-xs px-2 py-0.5 rounded ${
              isBuy ? 'bg-success/20 text-success' : 'bg-danger/20 text-danger'
            }`}>
              {trade.side.toUpperCase()}
            </span>
          </div>
          <div className="text-xs text-dark-400 flex items-center space-x-2">
            <span>{trade.quantity.toFixed(6)}</span>
            <span>@</span>
            <span>${trade.price.toLocaleString()}</span>
          </div>
        </div>
      </div>

      <div className="text-right">
        <div className={`font-semibold ${isProfitable ? 'text-success' : 'text-danger'}`}>
          {isProfitable ? '+' : ''} ${Math.abs(trade.pnl).toFixed(2)}
        </div>
        <div className="text-xs text-dark-400">{timeAgo}</div>
      </div>
    </div>
  )
}

function getTimeAgo(date: Date): string {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000)
  
  if (seconds < 60) return `${seconds}s ago`
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  return `${Math.floor(seconds / 86400)}d ago`
}