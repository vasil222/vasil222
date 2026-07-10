import { ArrowUpRight, ShoppingCart, Target, Trophy, Wallet } from 'lucide-react'
import { Reveal } from '@/components/reveal'

const steps = [
  { num: '01', Icon: ShoppingCart, title: 'Купи X5', text: 'Придбай будь-яку кількість токенів через офіційне посилання.' },
  { num: '02', Icon: Wallet, title: 'Тримай токени', text: 'Зберігай X5 у своєму гаманці до завершення раунду.' },
  { num: '03', Icon: Target, title: 'Потрап у раунд', text: 'Гаманець враховується за правилами поточного розіграшу.' },
  { num: '04', Icon: Trophy, title: 'Отримай бонус', text: 'Переможець отримує винагороду до x5 із призового пулу.', active: true },
]

export function How() {
  return (
    <section id="how" className="relative py-20 md:py-[110px]">
      <div className="mx-auto w-[min(1200px,calc(100%-36px))]">
        <Reveal className="mb-12 flex flex-col items-start justify-between gap-6 md:flex-row md:items-end">
          <div>
            <div className="text-[11px] font-extrabold tracking-[0.16em] text-brand">02 / МЕХАНІКА</div>
            <h2 className="mt-5 font-display text-[clamp(40px,6vw,82px)] leading-[0.98] tracking-[-0.055em]">
              Чотири кроки
              <br />
              до участі.
            </h2>
          </div>
          <p className="max-w-[420px] leading-[1.7] text-muted-foreground">
            Усе побудовано так, щоб користувач зрозумів механіку за кілька секунд.
          </p>
        </Reveal>

        <div className="grid grid-cols-1 gap-[14px] sm:grid-cols-2 lg:grid-cols-4">
          {steps.map(({ num, Icon, title, text, active }, i) => (
            <Reveal
              key={num}
              delay={i * 80}
              as="article"
              className={`group relative min-h-[330px] overflow-hidden rounded-[20px] border p-[25px] transition duration-300 hover:-translate-y-[7px] hover:border-brand/[0.28] ${
                active
                  ? 'border-brand/[0.35] shadow-[inset_0_0_55px_rgba(108,255,15,0.05)]'
                  : 'border-border'
              }`}
              style={{
                background: 'linear-gradient(145deg, rgba(255,255,255,.032), rgba(255,255,255,.012))',
              }}
            >
              <div className="flex justify-between text-[12px] text-[#5f6a5c]">
                <span>{num}</span>
                <ArrowUpRight className="h-4 w-4 text-brand" />
              </div>
              <Icon className="mt-[65px] mb-[22px] h-10 w-10 text-brand" strokeWidth={1.5} />
              <h3 className="mb-[13px] font-display text-[23px]">{title}</h3>
              <p className="text-[14px] leading-[1.65] text-[#909a8d]">{text}</p>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
