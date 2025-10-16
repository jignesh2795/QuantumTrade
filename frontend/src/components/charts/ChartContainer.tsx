'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import {
  createChart,
  IChartApi,
  ISeriesApi,
  CandlestickData,
  UTCTimestamp,
} from 'lightweight-charts'
import { TrendingUp, Maximize2, Settings } from 'lucide-react'

interface ChartContainerProps {
  currentPrice: number
}

function generateInitialData(price: number, timeframe: string): CandlestickData[] {
  const intervals: Record<string, number> = {
    '1M': 60,
    '5M': 300,
    '15M': 900,
    '1H': 3600,
    '4H': 14400,
    '1D': 86400,
  }

  const interval = intervals[timeframe] ?? 3600
  const points = 120
  const now = Math.floor(Date.now() / 1000) as UTCTimestamp
  const data: CandlestickData[] = []
  let basePrice = price

  for (let i = points; i >= 0; i--) {
    const time = (now - i * interval) as UTCTimestamp
    const open = basePrice
    const change = (Math.random() - 0.5) * 0.02 * basePrice
    const close = Math.max(1, open + change)
    const high = Math.max(open, close) + Math.random() * 0.01 * basePrice
    const low = Math.max(1, Math.min(open, close) - Math.random() * 0.01 * basePrice)

    data.push({
      time,
      open,
      high,
      low,
      close,
    })

    basePrice = close
  }

  return data
}

function calculateSMA(data: CandlestickData[], period: number) {
  const result: { time: UTCTimestamp; value: number }[] = []

  for (let i = period - 1; i < data.length; i++) {
    const slice = data.slice(i - period + 1, i + 1)
    const sum = slice.reduce((acc, candle) => acc + candle.close, 0)
    result.push({ time: data[i].time as UTCTimestamp, value: sum / period })
  }

  return result
}

export default function ChartContainer({ currentPrice }: ChartContainerProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const candleSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null)
  const smaFastRef = useRef<ISeriesApi<'Line'> | null>(null)
  const smaSlowRef = useRef<ISeriesApi<'Line'> | null>(null)
  const candleDataRef = useRef<CandlestickData[]>([])
  const [timeframe, setTimeframe] = useState('1H')

  const timeframes = useMemo(() => ['1M', '5M', '15M', '1H', '4H', '1D'], [])

  const initialData = useMemo(() => {
    return generateInitialData(currentPrice, timeframe)
  }, [currentPrice, timeframe])

  useEffect(() => {
    if (!chartContainerRef.current) return

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: '#0f172a' },
        textColor: '#94a3b8',
      },
      grid: {
        vertLines: { color: '#1e293b' },
        horzLines: { color: '#1e293b' },
      },
      width: chartContainerRef.current.clientWidth,
      height: 500,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
    })

    chartRef.current = chart

    const candleSeries = chart.addCandlestickSeries({
      upColor: '#10b981',
      downColor: '#ef4444',
      borderVisible: false,
      wickUpColor: '#10b981',
      wickDownColor: '#ef4444',
    })

    candleSeriesRef.current = candleSeries

    candleDataRef.current = initialData
    candleSeries.setData(initialData)

    const smaFast = chart.addLineSeries({
      color: '#0ea5e9',
      lineWidth: 2,
      title: 'SMA 10',
    })

    const smaSlow = chart.addLineSeries({
      color: '#f59e0b',
      lineWidth: 2,
      title: 'SMA 30',
    })

    smaFastRef.current = smaFast
    smaSlowRef.current = smaSlow

    smaFast.setData(calculateSMA(initialData, 10))
    smaSlow.setData(calculateSMA(initialData, 30))

    chart.timeScale().fitContent()

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentRect.width && chartRef.current) {
          chartRef.current.applyOptions({ width: entry.contentRect.width })
        }
      }
    })

    resizeObserver.observe(chartContainerRef.current)

    return () => {
      resizeObserver.disconnect()
      chart.remove()
    }
  }, [initialData])

  useEffect(() => {
    if (!candleSeriesRef.current) return

    candleDataRef.current = initialData
    candleSeriesRef.current.setData(initialData)
    smaFastRef.current?.setData(calculateSMA(initialData, 10))
    smaSlowRef.current?.setData(calculateSMA(initialData, 30))
    chartRef.current?.timeScale().fitContent()
  }, [initialData])

  useEffect(() => {
    if (!candleSeriesRef.current || candleDataRef.current.length === 0) return

    const data = candleDataRef.current
    const lastIndex = data.length - 1
    const lastCandle = data[lastIndex]

    const updatedCandle: CandlestickData = {
      ...lastCandle,
      close: currentPrice,
      high: Math.max(lastCandle.high, currentPrice),
      low: Math.min(lastCandle.low, currentPrice),
    }

    data[lastIndex] = updatedCandle
    candleSeriesRef.current.update(updatedCandle)

    smaFastRef.current?.setData(calculateSMA(data, 10))
    smaSlowRef.current?.setData(calculateSMA(data, 30))
  }, [currentPrice])

  return (
    <div className="glass rounded-xl p-6">
      {/* Chart Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-4">
          <h2 className="text-xl font-bold">BTCUSDT</h2>
          <div className="flex items-center space-x-2 text-2xl font-bold">
            <span className="text-success">
              ${currentPrice.toLocaleString('en-US', { minimumFractionDigits: 2 })}
            </span>
            <TrendingUp className="w-5 h-5 text-success" />
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Timeframe Selector */}
          <div className="flex items-center space-x-1 bg-dark-900 rounded-lg p-1">
            {timeframes.map((tf) => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={`px-3 py-1 rounded text-sm transition-colors ${
                  timeframe === tf
                    ? 'bg-primary-600 text-white'
                    : 'text-dark-400 hover:text-white'
                }`}
              >
                {tf}
              </button>
            ))}
          </div>

          <button className="p-2 hover:bg-dark-800 rounded-lg transition-colors">
            <Settings className="w-5 h-5 text-dark-400" />
          </button>
          <button className="p-2 hover:bg-dark-800 rounded-lg transition-colors">
            <Maximize2 className="w-5 h-5 text-dark-400" />
          </button>
        </div>
      </div>

      {/* Chart */}
      <div ref={chartContainerRef} className="rounded-lg overflow-hidden" />

      {/* Chart Legend */}
      <div className="flex items-center space-x-6 mt-4 text-sm">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-0.5 bg-primary-500" />
          <span className="text-dark-400">SMA 10</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-0.5 bg-warning" />
          <span className="text-dark-400">SMA 30</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-success rounded-sm" />
          <span className="text-dark-400">Buy Signal</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-danger rounded-sm" />
          <span className="text-dark-400">Sell Signal</span>
        </div>
      </div>
    </div>
  )
}