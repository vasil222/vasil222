import { Reveal } from '@/components/reveal'

export function FinalCta() {
  return (
    <section id="buy" className="relative py-20 md:py-[110px]">
      <div className="mx-auto w-[min(1200px,calc(100%-36px))]">
        <Reveal
          className="relative grid min-h-[420px] grid-cols-1 items-center gap-10 overflow-hidden rounded-[28px] border border-brand/[0.18] p-8 md:grid-cols-[1fr_0.7fr] md:p-[58px]"
          style={{ background: 'linear-gradient(135deg, #0a0f0a, #071007)' }}
        >
          <div className="pointer-events-none absolute -right-[100px] -top-[100px] h-[420px] w-[420px] rounded-full bg-[rgba(105,255,15,0.12)] blur-[100px]" />
          <div className="relative">
            <div className="text-[11px] font-extrabold tracking-[0.16em] text-brand">READY FOR X5?</div>
            <h2 className="my-5 font-display text-[clamp(40px,6vw,72px)] leading-[0.98] tracking-[-0.055em]">
              Твій шанс
              <br />
              <span className="text-brand">починається тут.</span>
            </h2>
            <p className="text-muted-foreground">Підключи офіційне посилання на DEX після запуску токена.</p>
          </div>

          <div className="relative flex flex-col gap-4">
            <a
              href="#"
              className="inline-flex items-center justify-center gap-4 rounded-[13px] bg-gradient-to-br from-[#b9ff4a] to-[#61e600] px-7 py-[22px] text-[15px] font-extrabold text-[#061006] shadow-[0_14px_40px_rgba(106,255,15,0.16)] transition hover:-translate-y-[3px] hover:shadow-[0_18px_48px_rgba(106,255,15,0.28)]"
            >
              КУПИТИ X5 <span aria-hidden>↗</span>
            </a>
            <div className="grid grid-cols-2 gap-3">
              {['Telegram', 'X / Twitter'].map((s) => (
                <a
                  key={s}
                  href="#"
                  className="rounded-[12px] border border-border p-[15px] text-center text-[12px] text-[#b0b9ad] transition-colors hover:border-brand/30 hover:text-brand"
                >
                  {s}
                </a>
              ))}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  )
}
