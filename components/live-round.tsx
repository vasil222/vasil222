'use client'

import { useCountdown } from '@/hooks/use-countdown'

export function LiveRound() {
  const { time } = useCountdown()

  return (
    <section className="relative py-20 md:py-[110px]">
      <div
        className="reveal visible mx-auto grid min-h-[320px] w-[min(1200px,calc(100%-36px))] grid-cols-1 items-center gap-12 rounded-[25px] border border-brand/20 p-8 md:grid-cols-[0.8fr_1.2fr] md:p-12"
        style={{
          background:
            'radial-gradient(circle at 82% 50%, rgba(100,255,10,.10), transparent 35%), var(--card)',
        }}
      >
        <div>
          <div className="flex items-center gap-[9px] text-[10px] tracking-[0.16em] text-brand">
            <span className="animate-pulse-dot h-2 w-2 rounded-full bg-brand shadow-[0_0_15px_var(--brand)]" />
            LIVE ROUND
          </div>
          <h2 className="my-[18px] font-display text-[44px] md:text-[56px]">
            Раунд <span className="text-gold">#12</span>
          </h2>
          <p className="text-muted-foreground">Приклад інтерактивного блоку майбутнього кабінету X5.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3">
          {[
            ['PRIZE POOL', '$125,430'],
            ['PARTICIPANTS', '8,742'],
            ['TIME LEFT', time],
          ].map(([label, value]) => (
            <div key={label} className="border-t border-border p-5 sm:border-l sm:border-t-0">
              <span className="block text-[9px] tracking-[0.14em] text-[#727d70]">{label}</span>
              <strong className="mt-[10px] block font-display text-[25px] tabular-nums">{value}</strong>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
