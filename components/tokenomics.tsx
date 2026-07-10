import { Reveal } from '@/components/reveal'

const allocation = [
  { label: 'Ліквідність', value: '50%', color: 'var(--brand)' },
  { label: 'Маркетинг', value: '20%', color: 'var(--gold)' },
  { label: 'Prize Pool', value: '15%', color: '#9a5cff' },
  { label: 'Спалювання', value: '10%', color: '#ff6244' },
  { label: 'Команда', value: '5%', color: '#4d8fff' },
]

export function Tokenomics() {
  return (
    <section id="tokenomics" className="relative py-20 md:py-[110px]">
      <div className="mx-auto grid w-[min(1200px,calc(100%-36px))] grid-cols-1 items-center gap-[70px] md:grid-cols-[0.9fr_1.1fr]">
        <Reveal className="token-copy">
          <div className="text-[11px] font-extrabold tracking-[0.16em] text-brand">03 / ТОКЕНОМІКА</div>
          <h2 className="my-5 font-display text-[clamp(40px,6vw,82px)] leading-[0.98] tracking-[-0.055em]">
            1 мільярд токенів.
            <br />
            <span className="text-brand">Чіткий розподіл.</span>
          </h2>
          <p className="max-w-[590px] leading-[1.75] text-muted-foreground">
            Концептуальна модель розподілу X5. Перед реальним запуском цифри потрібно узгодити зі смартконтрактом і
            юридичною моделлю.
          </p>
          <div className="mt-9 border-l-2 border-brand bg-brand/[0.035] p-[22px]">
            <span className="block text-[9px] tracking-[0.18em] text-[#778274]">TOTAL SUPPLY</span>
            <strong className="mt-2 block font-display text-2xl">1,000,000,000 X5</strong>
          </div>
        </Reveal>

        <Reveal className="grid grid-cols-1 items-center gap-12 rounded-[24px] border border-border bg-card p-[38px] sm:grid-cols-[280px_1fr]">
          <div
            className="relative mx-auto grid aspect-square w-[220px] place-items-center rounded-full shadow-[0_0_60px_rgba(140,255,33,0.08)] sm:w-[280px]"
            style={{
              background:
                'conic-gradient(var(--brand) 0 50%, var(--gold) 50% 70%, #9a5cff 70% 85%, #ff6244 85% 95%, #4d8fff 95% 100%)',
            }}
          >
            <div className="absolute h-[60%] w-[60%] rounded-full bg-[#091009]" />
            <div className="relative text-center">
              <strong className="block font-display text-[42px] sm:text-[50px]">1B</strong>
              <span className="text-[9px] tracking-[0.12em] text-[#778274]">X5 SUPPLY</span>
            </div>
          </div>

          <div>
            {allocation.map((row) => (
              <div key={row.label} className="flex items-center justify-between border-b border-border py-[15px]">
                <span className="flex items-center gap-[10px] text-[#b0b9ad]">
                  <i className="block h-[10px] w-[10px] rounded-full" style={{ background: row.color }} />
                  {row.label}
                </span>
                <b className="font-display">{row.value}</b>
              </div>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  )
}
