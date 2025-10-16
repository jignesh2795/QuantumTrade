'use client'

import { useState, useEffect } from 'react'
import DashboardHeader from '@/components/dashboard/DashboardHeader'
import StatsGrid from '@/components/dashboard/StatsGrid'
import ChartContainer from '@/components/charts/ChartContainer'
import BotList from '@/components/bots/BotList'
import AgentPanel from '@/components/agents/AgentPanel'
import TradeHistory from '@/components/dashboard/TradeHistory'

export default function Home() {
  const [isConnected, setIsConnected] = useState(false)
  const [currentPrice, setCurrentPrice] = useState(43125.50)

  useEffect(() => {
    // Connect to WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws')
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      setIsConnected(true)
    }
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('Received:', data)
      
      // Update price (mock for now)
      if (data.type === 'price_update') {
        setCurrentPrice(data.price)
      }
    }
    
    ws.onclose = () => {
      console.log('WebSocket disconnected')
      setIsConnected(false)
    }
    
    // Simulate price updates
    const priceInterval = setInterval(() => {
      setCurrentPrice(prev => prev + (Math.random() - 0.5) * 100)
    }, 2000)
    
    return () => {
      ws.close()
      clearInterval(priceInterval)
    }
  }, [])

  return (
    <main className="min-h-screen bg-dark-950 text-white">
      <DashboardHeader isConnected={isConnected} />
      
      <div className="container max-w-7xl py-8 space-y-8">
        {/* Stats Grid */}
        <StatsGrid currentPrice={currentPrice} />
        
        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chart - Takes 2 columns */}
          <div className="lg:col-span-2">
            <ChartContainer currentPrice={currentPrice} />
          </div>
          
          {/* Agent Panel */}
          <div>
            <AgentPanel />
          </div>
        </div>
        
        {/* Bottom Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Bot List */}
          <BotList />
          
          {/* Trade History */}
          <TradeHistory />
        </div>
      </div>
    </main>
  )
}