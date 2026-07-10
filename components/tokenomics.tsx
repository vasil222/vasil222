'use client'

import { useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Reveal } from '@/components/reveal'
import { ALLOCATION, TOKEN } from '@/lib/token-config'

const RADIUS = 90
const STROKE = 34
const CIRC = 2 * Math.PI * RADIUS

export function Tokenomics() {
  const [active, setActive] = useState<string>(ALLOCATION[0].key)
  const activeItem = ALLOCATION.find((a) => a.key === active) ?? ALLOCATION[0]

  let offset = 0
  const segments = ALLOCATION.map((item) => {
    const len = (item.value / 100) * CIRC
    const seg = { ...item, dash: len, gap: CIRC - len, rotation: (offset / CIRC) * 360 }
    offset += len
    return seg
  })

  return (
    <section id="tokenomics" className="relative py-20 md:py-[110px]">
      <div className="mx-auto grid w-[min(1200px,calc(100%-36px))] grid-cols-1 items-center gap-[70px] md:grid-cols-[0.9fr_1.1fr]">
        <Reveal>
          <div className="text-[11px] font-extrabold tracking-[0.16em] text-brand">03 / ТОКЕНОМІКА</div>
          <h2 className="my-5 font-display text-[clamp(40px,6vw,82px)] leading-[0.98] tracking-[-0.055em]">
            1 мільярд токенів.
            <br />
            <span className="text-brand text-glow">Чіткий розподіл.</span>
          </h2>
          <p className="max-w-[590px] leading-[1.75] text-muted-foreground">
            Наведи або клікни на сегмент, щоб побачити призначення кожної частини емісії X5.
          </p>

          <AnimatePresence mode="wait">
            <motion.div
              key={activeItem.key}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.25 }}
              className="mt-9 rounded-2xl border-l-2 p-[22px]"
              style={{ borderColor: activeItem.color, background: `${activeItem.color}0d` }}
            >
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 font-display text-lg">
                  <i className="h-3 w-3 rounded-full" style={{ background: activeItem.color }} />
                  {activeItem.label}
                </span>
                <strong className="font-display text-2xl" style={{ color: activeItem.color }}>
                  {activeItem.value}%
                </strong>
              </div>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{activeItem.desc}</p>
              <div className="mt-3 text-[13px] tabular-nums text-[#778274]">
                {((activeItem.value / 100) * TOKEN.totalSupply).toLocaleString('en-US')} X5
              </div>
            </motion.div>
          </AnimatePresence>
        </Reveal>

        <Reveal className="grid grid-cols-1 items-center gap-10 rounded-[24px] glass glow-brand p-[38px] sm:grid-cols-[260px_1fr]">
          <div className="relative mx-auto aspect-square w-[240px]">
            <svg viewBox="0 0 220 220" className="h-full w-full -rotate-90">
              {segments.map((seg) => {
                const isActive = seg.key === active
                return (
                  <circle
                    key={seg.key}
                    cx="110"
                    cy="110"
                    r={RADIUS}
                    fill="none"
                    stroke={seg.color}
                    strokeWidth={isActive ? STROKE + 8 : STROKE}
                    strokeDasharray={`${seg.dash} ${seg.gap}`}
                    strokeDashoffset={-((seg.rotation / 360) * CIRC)}
                    className="cursor-pointer transition-all duration-300"
                    style={{
                      opacity: isActive ? 1 : 0.72,
                      filter: isActive ? `drop-shadow(0 0 10px ${seg.color})` : 'none',
                    }}
                    onMouseEnter={() => setActive(seg.key)}
                    onClick={() => setActive(seg.key)}
                  />
                )
              })}
            </svg>
            <div className="pointer-events-none absolute inset-0 grid place-items-center rotate-0 text-center">
              <div>
                <strong className="block font-display text-[44px] leading-none">1B</strong>
                <span className="text-[9px] tracking-[0.12em] text-[#778274]">X5 SUPPLY</span>
              </div>
            </div>
          </div>

          <div>
            {ALLOCATION.map((row) => {
              const isActive = row.key === active
              return (
                <button
                  key={row.key}
                  type="button"
                  onMouseEnter={() => setActive(row.key)}
                  onClick={() => setActive(row.key)}
                  className="flex w-full items-center justify-between border-b border-border py-[13px] text-left transition-colors"
                  style={{ color: isActive ? row.color : '#b0b9ad' }}
                >
                  <span className="flex items-center gap-[10px]">
                    <i
                      className="block rounded-full transition-all"
                      style={{
                        background: row.color,
                        width: isActive ? 13 : 10,
                        height: isActive ? 13 : 10,
                        boxShadow: isActive ? `0 0 10px ${row.color}` : 'none',
                      }}
                    />
                    {row.label}
                  </span>
                  <b className="font-display tabular-nums">{row.value}%</b>
                </button>
              )
            })}
          </div>
        </Reveal>
      </div>
    </section>
  )
}
