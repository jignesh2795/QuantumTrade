'use client'

import { TrendingUp, TrendingDown, Wallet, Activity, AlertCircle, Shield } from 'lucide-react'
import { useEffect, useState } from 'react'

interface StatsGridProps {
  currentPrice: number
}

export default function StatsGrid({ currentPrice }: StatsGridProps) {
  const [stats, setStats] = useState({
    totalBalance: 10250.50,
    dailyPnl: 250.50,
    dailyPnlPct: 2.51,
    activeBots: 3,
    totalTrades: 47,
    winRate: 65.5,
  })

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Portfolio Value */}
      <StatCard
        title="Portfolio Value"
        value={`$${stats.totalBalance.toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
        change={stats.dailyPnlPct}
        icon={<Wallet className="w-5 h-5" />}
        trend={stats.dailyPnl > 0 ? 'up' : 'down'}
      />

      {/* Daily P&L */}
      <StatCard
        title="Daily P&L"
        value={`$${Math.abs(stats.dailyPnl).toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
        change={stats.dailyPnlPct}
        icon={stats.dailyPnl > 0 ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
        trend={stats.dailyPnl > 0 ? 'up' : 'down'}
      />

      {/* Active Bots */}
      <StatCard
        title="Active Bots"
        value={stats.activeBots.toString()}
        subtitle={`${stats.totalTrades} trades today`}
        icon={<Activity className="w-5 h-5" />}
        trend="neutral"
      />

      {/* Win Rate */}
      <StatCard
        title="Win Rate"
        value={`${stats.winRate}%`}
        subtitle="Last 30 days"
        icon={<Shield className="w-5 h-5" />}
        trend={stats.winRate >= 60 ? 'up' : 'down'}
      />
    </div>
  )
}

interface StatCardProps {
  title: string
  value: string
  change?: number
  subtitle?: string
  icon: React.ReactNode
  trend: 'up' | 'down' | 'neutral'
}

function StatCard({ title, value, change, subtitle, icon, trend }: StatCardProps) {
  const trendColor = {
    up: 'text-success',
    down: 'text-danger',
    neutral: 'text-dark-400'
  }[trend]

  const bgColor = {
    up: 'bg-success/10',
    down: 'bg-danger/10',
    neutral: 'bg-dark-800'
  }[trend]

  return (
    <div className="glass rounded-xl p-6 hover:glow transition-all duration-300">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-dark-400 text-sm mb-1">{title}</p>
          <h3 className="text-2xl font-bold mb-2">{value}</h3>
          {change !== undefined && (
            <div className={`flex items-center space-x-1 text-sm ${trendColor}`}>
              {trend === 'up' ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
              <span>{Math.abs(change).toFixed(2)}%</span>
            </div>
          )}
          {subtitle && (
            <p className="text-dark-400 text-xs mt-1">{subtitle}</p>
          )}
        </div>
        <div className={`${bgColor} p-3 rounded-lg ${trendColor}`}>
          {icon}
        </div>
      </div>
    </div>
  )
}