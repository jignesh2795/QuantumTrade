'use client'

import { Activity, Settings, Bell, TrendingUp } from 'lucide-react'

interface DashboardHeaderProps {
  isConnected: boolean
}

export default function DashboardHeader({ isConnected }: DashboardHeaderProps) {
  return (
    <header className="glass border-b border-dark-700 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo & Title */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-8 h-8 text-primary-500" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                QuantumTrade
              </h1>
            </div>
            <span className="text-sm text-dark-400">v0.4.0</span>
          </div>
          
          {/* Center - Connection Status */}
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-success animate-pulse' : 'bg-danger'}`} />
            <span className="text-sm text-dark-300">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          
          {/* Right - Actions */}
          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-dark-800 rounded-lg transition-colors">
              <Bell className="w-5 h-5 text-dark-300" />
            </button>
            <button className="p-2 hover:bg-dark-800 rounded-lg transition-colors">
              <Settings className="w-5 h-5 text-dark-300" />
            </button>
            <button className="px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors flex items-center space-x-2">
              <Activity className="w-4 h-4" />
              <span>New Bot</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}