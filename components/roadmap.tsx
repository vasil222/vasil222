import { Check } from 'lucide-react'
import { Reveal } from '@/components/reveal'

const phases = [
  { phase: 'PHASE 01', title: 'Launch', items: ['Токен і сайт', 'Соціальні мережі', 'Початкова ліквідність'] },
  { phase: 'PHASE 02', title: 'Growth', items: ['Перші раунди', 'Маркетинг', 'Ріст спільноти'] },
  { phase: 'PHASE 03', title: 'Expansion', items: ['Нові лістинги', 'Аудит контракту', 'Партнерства'] },
  { phase: 'PHASE 04', title: 'X5 Legacy', items: ['Глобальний бренд', 'Нові utility', 'Масштабування'] },
]

export function Roadmap() {
  return (
    <section id="roadmap" className="relative py-20 md:py-[110px]">
      <div className="mx-auto w-[min(1200px,calc(100%-36px))]">
        <Reveal className="mb-12">
          <div className="text-[11px] font-extrabold tracking-[0.16em] text-brand">04 / ROADMAP</div>
          <h2 className="mt-5 font-display text-[clamp(40px,6vw,82px)] leading-[0.98] tracking-[-0.055em]">
            Від запуску
            <br />
            до масштабування.
          </h2>
        </Reveal>

        <div className="grid grid-cols-1 gap-9 sm:grid-cols-2 lg:grid-cols-4">
          {phases.map((p, i) => (
            <Reveal key={p.phase} as="article" delay={i * 80} className="pr-6">
              <span className="text-[10px] font-extrabold tracking-[0.15em] text-brand">{p.phase}</span>
              <div className="relative my-[22px] h-px bg-border">
                <span className="absolute -top-1 left-0 h-2 w-2 rounded-full bg-brand shadow-[0_0_12px_rgba(140,255,33,0.8)]" />
              </div>
              <h3 className="font-display text-[29px]">{p.title}</h3>
              <ul className="mt-3 space-y-2 text-[#8d978a]">
                {p.items.map((item) => (
                  <li key={item} className="flex items-center gap-2">
                    <Check className="h-4 w-4 shrink-0 text-brand" />
                    {item}
                  </li>
                ))}
              </ul>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}
