'use client'

import { useEffect, useState } from 'react'
import { Play, Pause, Trash2, MoreVertical, Activity } from 'lucide-react'
import axios from 'axios'

interface Bot {
  id: string
  name: string
  status: string
  mode: string
  symbol: string
  strategy: string
  capital: number
  pnl: number
  pnl_pct: number
  trades_today: number
  uptime: number
}

export default function BotList() {
  const [bots, setBots] = useState<Bot[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBots()
    const interval = setInterval(fetchBots, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchBots = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/bots')
      setBots(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching bots:', error)
      setLoading(false)
    }
  }

  const handleStartStop = async (botId: string, currentStatus: string) => {
    try {
      const action = currentStatus === 'running' ? 'stop' : 'start'
      await axios.post(`http://localhost:8000/api/bots/${botId}/${action}`)
      fetchBots()
    } catch (error) {
      console.error('Error toggling bot:', error)
    }
  }

  const handleDelete = async (botId: string) => {
    if (!confirm('Are you sure you want to delete this bot?')) return
    
    try {
      await axios.delete(`http://localhost:8000/api/bots/${botId}`)
      fetchBots()
    } catch (error) {
      console.error('Error deleting bot:', error)
    }
  }

  if (loading) {
    return (
      <div className="glass rounded-xl p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-dark-800 rounded w-1/3" />
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-20 bg-dark-800 rounded" />
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="glass rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold">Active Bots</h2>
        <span className="text-dark-400 text-sm">{bots.length} running</span>
      </div>

      <div className="space-y-3">
        {bots.map((bot) => (
          <BotCard
            key={bot.id}
            bot={bot}
            onStartStop={() => handleStartStop(bot.id, bot.status)}
            onDelete={() => handleDelete(bot.id)}
          />
        ))}

        {bots.length === 0 && (
          <div className="text-center py-12 text-dark-400">
            <Activity className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>No active bots</p>
            <button className="mt-4 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors">
              Create Your First Bot
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

interface BotCardProps {
  bot: Bot
  onStartStop: () => void
  onDelete: () => void
}

function BotCard({ bot, onStartStop, onDelete }: BotCardProps) {
  const isRunning = bot.status === 'running'
  const isProfitable = bot.pnl > 0

  return (
    <div className="bg-dark-900 rounded-lg p-4 hover:bg-dark-800 transition-all duration-300">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <div className={`w-2 h-2 rounded-full ${isRunning ? 'bg-success animate-pulse' : 'bg-dark-600'}`} />
            <h3 className="font-semibold">{bot.name}</h3>
            <span className={`text-xs px-2 py-0.5 rounded ${
              bot.mode === 'live' ? 'bg-danger/20 text-danger' : 'bg-primary/20 text-primary-400'
            }`}>
              {bot.mode.toUpperCase()}
            </span>
          </div>

          <div className="flex items-center space-x-4 text-sm text-dark-400">
            <span>{bot.symbol}</span>
            <span>•</span>
            <span>{bot.strategy}</span>
            <span>•</span>
            <span>{bot.trades_today} trades</span>
          </div>

          <div className="flex items-center space-x-4 mt-2">
            <div className="text-sm">
              <span className="text-dark-400">Capital: </span>
              <span className="font-semibold">${bot.capital.toLocaleString()}</span>
            </div>
            <div className="text-sm">
              <span className="text-dark-400">P&L: </span>
              <span className={`font-semibold ${isProfitable ? 'text-success' : 'text-danger'}`}>
                ${Math.abs(bot.pnl).toFixed(2)} ({bot.pnl_pct.toFixed(2)}%)
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={onStartStop}
            className={`p-2 rounded-lg transition-colors ${
              isRunning 
                ? 'bg-warning/20 hover:bg-warning/30 text-warning' 
                : 'bg-success/20 hover:bg-success/30 text-success'
            }`}
            title={isRunning ? 'Stop Bot' : 'Start Bot'}
          >
            {isRunning ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>
          <button
            onClick={onDelete}
            className="p-2 bg-danger/20 hover:bg-danger/30 text-danger rounded-lg transition-colors"
            title="Delete Bot"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}