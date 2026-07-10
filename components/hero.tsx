'use client'

import Image from 'next/image'
import { useEffect, useState } from 'react'
import { useCountdown } from '@/hooks/use-countdown'

const CONTRACT = '0xX5...X5'

export function Hero() {
  const { time, progress } = useCountdown()
  const [participants, setParticipants] = useState(8742)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    const id = setInterval(() => {
      if (Math.random() > 0.55) {
        setParticipants((p) => p + Math.floor(Math.random() * 3) + 1)
      }
    }, 3200)
    return () => clearInterval(id)
  }, [])

  async function copyContract() {
    try {
      await navigator.clipboard.writeText(CONTRACT)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      setCopied(false)
    }
  }

  return (
    <section
      id="home"
      className="relative flex min-h-[920px] items-center overflow-hidden pt-[135px] pb-16 md:pt-[165px]"
      style={{
        background:
          'radial-gradient(circle at 68% 27%, rgba(104,255,15,.11), transparent 25%), radial-gradient(circle at 85% 68%, rgba(255,211,48,.08), transparent 24%)',
      }}
    >
      {/* orbs */}
      <div className="pointer-events-none absolute -left-[150px] top-[200px] h-[400px] w-[400px] rounded-full bg-[rgba(90,255,0,0.07)] blur-[120px]" />
      <div className="pointer-events-none absolute -right-[100px] bottom-10 h-[330px] w-[330px] rounded-full bg-[rgba(255,200,0,0.06)] blur-[120px]" />

      <div className="relative z-[2] mx-auto w-[min(1200px,calc(100%-36px))]">
        <div className="grid grid-cols-1 items-center gap-[70px] md:grid-cols-[0.98fr_1.02fr]">
          {/* copy */}
          <div className="reveal visible">
            <div className="inline-flex items-center gap-[9px] text-[11px] font-extrabold tracking-[0.16em] text-brand">
              <span className="h-[7px] w-[7px] rounded-full bg-brand shadow-[0_0_14px_var(--brand)]" />
              COMMUNITY MEME COIN
            </div>
            <h1 className="my-5 font-display text-[clamp(61px,8.4vw,124px)] leading-[0.82] tracking-[-0.055em]">
              BUY.
              <br />
              HOLD.
              <br />
              <em className="not-italic text-brand [text-shadow:0_0_45px_rgba(140,255,33,0.16)]">WIN X5.</em>
            </h1>
            <p className="max-w-[620px] text-[16px] leading-[1.7] text-[#aeb8aa] md:text-[18px]">
              Простий мемкоїн із бонусними раундами. Купуй X5, тримай у гаманці та отримуй можливість виграти
              винагороду до <b className="text-gold">x5</b> від суми покупки.
            </p>

            <div className="my-9 flex flex-col gap-[14px] sm:flex-row">
              <a
                href="#buy"
                className="inline-flex items-center justify-center gap-4 rounded-[13px] border border-transparent bg-gradient-to-br from-[#b9ff4a] to-[#61e600] px-6 py-[17px] text-[13px] font-extrabold text-[#061006] shadow-[0_14px_40px_rgba(106,255,15,0.16)] transition hover:-translate-y-[3px] hover:shadow-[0_18px_48px_rgba(106,255,15,0.28)]"
              >
                КУПИТИ X5 <span aria-hidden>↗</span>
              </a>
              <a
                href="#how"
                className="inline-flex items-center justify-center gap-4 rounded-[13px] border border-gold/30 bg-gold/[0.025] px-6 py-[17px] text-[13px] font-extrabold text-[#f2e4a5] transition hover:border-gold hover:text-gold"
              >
                ЯК ЦЕ ПРАЦЮЄ
              </a>
            </div>

            <div className="grid grid-cols-3 gap-6 border-t border-border pt-[30px] sm:flex sm:gap-12">
              {[
                ['LIQUIDITY', '50%'],
                ['PRIZE POOL', '15%'],
                ['TOTAL SUPPLY', '1B'],
              ].map(([label, value]) => (
                <div key={label} className="flex flex-col gap-[7px]">
                  <small className="text-[9px] tracking-[0.16em] text-[#6f7a6b]">{label}</small>
                  <strong className="font-display text-[17px]">{value}</strong>
                </div>
              ))}
            </div>
          </div>

          {/* art */}
          <div className="relative grid min-h-[420px] place-items-center md:min-h-[620px]">
            <div className="absolute h-[360px] w-[360px] rounded-full border border-brand/[0.12] animate-spin-slow md:h-[530px] md:w-[530px]" />
            <div className="absolute h-[420px] w-[420px] rounded-full border border-gold/[0.075] animate-spin-slower md:h-[650px] md:w-[650px]" />

            <div
              className="animate-float grid aspect-square w-[88%] place-items-center rounded-full p-4 drop-shadow-[0_30px_65px_rgba(0,0,0,0.5)] md:w-[min(520px,88%)]"
              style={{
                background:
                  'radial-gradient(circle, rgba(255,215,56,.17), rgba(85,255,0,.035) 58%, transparent 70%)',
              }}
            >
              <Image
                src="/x5-logo.png"
                alt="X5 coin"
                width={520}
                height={520}
                className="h-full w-full rounded-full object-cover"
                priority
              />
            </div>

            {/* round card */}
            <div className="absolute left-0 top-[5%] w-[160px] rounded-2xl border border-white/10 bg-[rgba(8,12,8,0.74)] p-[17px] shadow-[0_24px_70px_rgba(0,0,0,0.4)] backdrop-blur-md md:-left-[15px] md:top-[20%] md:w-[190px]">
              <span className="block text-[9px] tracking-[0.13em] text-[#7d8879]">НАСТУПНИЙ РАУНД</span>
              <strong className="my-2 block font-display text-2xl tabular-nums">{time}</strong>
              <div className="h-1 overflow-hidden rounded-full bg-[#1a2118]">
                <i
                  className="block h-full bg-gradient-to-r from-brand-2 to-brand transition-[width] duration-1000 ease-linear"
                  style={{ width: `${progress * 100}%` }}
                />
              </div>
            </div>

            {/* reward card */}
            <div className="absolute right-0 bottom-[5%] rounded-2xl border border-white/10 bg-[rgba(8,12,8,0.74)] p-[17px] text-center shadow-[0_24px_70px_rgba(0,0,0,0.4)] backdrop-blur-md md:-right-[5px] md:bottom-[18%]">
              <span className="block text-[9px] tracking-[0.13em] text-[#7d8879]">МАКСИМАЛЬНИЙ БОНУС</span>
              <strong className="my-2 block font-display text-[58px] leading-none text-gold">x5</strong>
              <small className="block text-[9px] tracking-[0.13em] text-[#7d8879]">із призового пулу</small>
            </div>

            {/* participants card */}
            <div className="absolute bottom-[8%] left-[8%] hidden rounded-2xl border border-white/10 bg-[rgba(8,12,8,0.74)] p-[17px] shadow-[0_24px_70px_rgba(0,0,0,0.4)] backdrop-blur-md sm:block">
              <span className="block text-[9px] tracking-[0.13em] text-[#7d8879]">УЧАСНИКІВ</span>
              <strong className="my-2 block font-display text-2xl tabular-nums">
                {participants.toLocaleString('uk-UA')}
              </strong>
            </div>
          </div>
        </div>

        {/* contract strip */}
        <div className="reveal visible relative z-[3] mt-[34px] flex flex-col items-start justify-between gap-[14px] rounded-[15px] border border-border bg-[rgba(9,13,9,0.78)] p-[18px] sm:flex-row sm:items-center">
          <div className="flex flex-col items-start gap-[6px] sm:flex-row sm:items-center sm:gap-[18px]">
            <span className="text-[9px] tracking-[0.16em] text-[#687365]">CONTRACT ADDRESS</span>
            <code className="text-gold">{CONTRACT}</code>
          </div>
          <button
            type="button"
            onClick={copyContract}
            className="text-[10px] font-extrabold text-brand transition-colors hover:text-brand-2"
          >
            {copied ? 'СКОПІЙОВАНО' : 'КОПІЮВАТИ'}
          </button>
        </div>
      </div>
    </section>
  )
}
