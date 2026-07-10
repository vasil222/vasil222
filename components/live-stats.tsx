'use client'

import { Area, AreaChart, ResponsiveContainer, YAxis } from 'recharts'
import { motion } from 'framer-motion'
import { useTokenStats } from '@/hooks/use-token-stats'
import { Reveal } from '@/components/reveal'

function fmtUsd(n: number, opts: Intl.NumberFormatOptions = {}) {
  return n.toLocaleString('en-US', { style: 'currency', currency: 'USD', ...opts })
}
function fmtCompact(n: number) {
  return n.toLocaleString('en-US', { notation: 'compact', maximumFractionDigits: 2 })
}

export function LiveStats() {
  const { stats, isLoading } = useTokenStats()
  const up = (stats?.priceChange24h ?? 0) >= 0
  const trend = up ? '#8cff21' : '#ff6244'

  const cards = stats
    ? [
        { label: 'VOLUME 24H', value: `$${fmtCompact(stats.volume24h)}` },
        { label: 'LIQUIDITY', value: `$${fmtCompact(stats.liquidityUsd)}` },
        { label: 'MARKET CAP', value: `$${fmtCompact(stats.marketCap)}` },
        { label: 'HOLDERS', value: fmtCompact(stats.holders) },
      ]
    : []

  return (
    <section id="live" className="relative py-16 md:py-[90px]">
      <div className="mx-auto w-[min(1200px,calc(100%-36px))]">
        <Reveal>
          <div className="grad-border overflow-hidden p-[26px] md:p-[38px]">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <span className="animate-pulse-dot h-2.5 w-2.5 rounded-full bg-brand shadow-[0_0_15px_var(--brand)]" />
                <span className="text-[11px] font-bold tracking-[0.16em] text-brand">
                  {stats?.live ? 'LIVE MARKET DATA' : 'МАРКЕТ-ДАНІ (SIMULATED)'}
                </span>
              </div>
              <span className="text-[10px] tracking-[0.12em] text-[#727d70]">
                {stats?.live ? 'DEXSCREENER' : 'ДЕМО — під\u0027єднайте контракт у lib/token-config.ts'}
              </span>
            </div>

            <div className="mt-6 grid grid-cols-1 gap-8 lg:grid-cols-[1fr_1.15fr]">
              {/* Price + chart */}
              <div>
                <div className="flex items-end gap-4">
                  <div>
                    <span className="block text-[10px] tracking-[0.14em] text-[#727d70]">X5 / USD</span>
                    <motion.strong
                      key={stats?.priceUsd}
                      initial={{ opacity: 0.4 }}
                      animate={{ opacity: 1 }}
                      className="block font-display text-[38px] leading-none tabular-nums md:text-[52px]"
                    >
                      {isLoading || !stats ? '—' : fmtUsd(stats.priceUsd, { maximumFractionDigits: 6 })}
                    </motion.strong>
                  </div>
                  {stats && (
                    <span
                      className="mb-1 rounded-full px-3 py-1 text-sm font-bold tabular-nums"
                      style={{ color: trend, background: `${trend}1a` }}
                    >
                      {up ? '▲' : '▼'} {Math.abs(stats.priceChange24h).toFixed(2)}%
                    </span>
                  )}
                </div>

                <div className="mt-5 h-[150px] w-full">
                  {stats && (
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={stats.series} margin={{ top: 6, right: 0, bottom: 0, left: 0 }}>
                        <defs>
                          <linearGradient id="x5fill" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor={trend} stopOpacity={0.4} />
                            <stop offset="100%" stopColor={trend} stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <YAxis hide domain={['dataMin', 'dataMax']} />
                        <Area
                          type="monotone"
                          dataKey="p"
                          stroke={trend}
                          strokeWidth={2}
                          fill="url(#x5fill)"
                          isAnimationActive
                          animationDuration={600}
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  )}
                </div>
              </div>

              {/* Stat cards */}
              <div className="grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-border bg-border">
                {cards.map((c) => (
                  <div key={c.label} className="bg-card p-5">
                    <span className="block text-[9px] tracking-[0.14em] text-[#727d70]">{c.label}</span>
                    <strong className="mt-2 block font-display text-[22px] tabular-nums md:text-[26px]">
                      {isLoading || !stats ? '—' : c.value}
                    </strong>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  )
}
