'use client'

import { useEffect, useState } from 'react'
import { Brain, Shield, Zap, TrendingUp, Activity } from 'lucide-react'
import axios from 'axios'

interface Agent {
  name: string
  type: string
  status: string
  confidence: number
  last_action: string
}

export default function AgentPanel() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAgents()
    const interval = setInterval(fetchAgents, 3000)
    return () => clearInterval(interval)
  }, [])

  const fetchAgents = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/analytics/agent-status')
      setAgents(response.data.agents)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching agents:', error)
      setLoading(false)
    }
  }

  const getAgentIcon = (type: string) => {
    switch (type) {
      case 'execution':
        return <Zap className="w-5 h-5" />
      case 'risk':
        return <Shield className="w-5 h-5" />
      case 'coordinator':
        return <Brain className="w-5 h-5" />
      case 'optimizer':
        return <TrendingUp className="w-5 h-5" />
      default:
        return <Activity className="w-5 h-5" />
    }
  }

  const getAgentColor = (type: string) => {
    switch (type) {
      case 'execution':
        return 'text-primary-500 bg-primary-500/10'
      case 'risk':
        return 'text-success bg-success/10'
      case 'coordinator':
        return 'text-purple-500 bg-purple-500/10'
      case 'optimizer':
        return 'text-warning bg-warning/10'
      default:
        return 'text-dark-400 bg-dark-800'
    }
  }

  if (loading) {
    return (
      <div className="glass rounded-xl p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-dark-800 rounded w-1/2" />
          <div className="space-y-3">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-24 bg-dark-800 rounded" />
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="glass rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold flex items-center space-x-2">
          <Brain className="w-6 h-6 text-purple-500" />
          <span>AI Agents</span>
        </h2>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
          <span className="text-xs text-dark-400">All Active</span>
        </div>
      </div>

      <div className="space-y-3">
        {agents.map((agent) => (
          <AgentCard key={agent.name} agent={agent} getIcon={getAgentIcon} getColor={getAgentColor} />
        ))}
      </div>
    </div>
  )
}

interface AgentCardProps {
  agent: Agent
  getIcon: (type: string) => React.ReactNode
  getColor: (type: string) => string
}

function AgentCard({ agent, getIcon, getColor }: AgentCardProps) {
  return (
    <div className="bg-dark-900 rounded-lg p-4 hover:bg-dark-800 transition-all duration-300">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-lg ${getColor(agent.type)}`}>
            {getIcon(agent.type)}
          </div>
          <div>
            <h3 className="font-semibold">{agent.name}</h3>
            <p className="text-xs text-dark-400 capitalize">{agent.type}</p>
          </div>
        </div>
        <span className={`text-xs px-2 py-1 rounded ${
          agent.status === 'active' ? 'bg-success/20 text-success' : 'bg-dark-700 text-dark-400'
        }`}>
          {agent.status}
        </span>
      </div>

      {/* Confidence Bar */}
      <div className="mb-2">
        <div className="flex items-center justify-between text-xs text-dark-400 mb-1">
          <span>Confidence</span>
          <span>{(agent.confidence * 100).toFixed(0)}%</span>
        </div>
        <div className="w-full bg-dark-800 rounded-full h-2 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              agent.confidence >= 0.7 ? 'bg-success' : agent.confidence >= 0.5 ? 'bg-warning' : 'bg-danger'
            }`}
            style={{ width: `${agent.confidence * 100}%` }}
          />
        </div>
      </div>

      {/* Last Action */}
      <div className="text-xs text-dark-400">
        <span className="font-medium">Last: </span>
        <span className="capitalize">{agent.last_action.replace(/_/g, ' ')}</span>
      </div>
    </div>
  )
}