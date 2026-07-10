import { Reveal } from '@/components/reveal'

const features = [
  ['01', 'Проста участь'],
  ['02', 'Публічні правила'],
  ['03', 'Прозорий prize pool'],
]

export function About() {
  return (
    <section id="about" className="relative py-20 md:py-[110px]">
      <div className="mx-auto grid w-[min(1200px,calc(100%-36px))] grid-cols-1 gap-10 md:grid-cols-[0.35fr_1.65fr]">
        <Reveal className="inline-flex h-fit items-center gap-[9px] text-[11px] font-extrabold tracking-[0.16em] text-brand">
          01 / ПРО X5
        </Reveal>
        <Reveal className="max-w-[900px]">
          <h2 className="my-5 font-display text-[clamp(40px,6vw,82px)] leading-[0.98] tracking-[-0.055em] text-balance">
            Мемкоїн, який дає <span className="text-brand">додатковий шанс.</span>
          </h2>
          <p className="max-w-[820px] text-[18px] leading-[1.75] text-[#aeb7ab] md:text-[20px]">
            X5 поєднує енергію мем-культури, сильну спільноту та зрозумілу бонусну механіку. Ніяких складних рівнів:
            придбав токени, тримаєш їх у гаманці та береш участь у поточному раунді за опублікованими правилами.
          </p>
          <div className="mt-[45px] grid grid-cols-1 gap-[14px] sm:grid-cols-3">
            {features.map(([num, label]) => (
              <article key={num} className="flex gap-5 border-t border-border pt-[22px]">
                <b className="text-[12px] text-brand">{num}</b>
                <span className="font-bold">{label}</span>
              </article>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  )
}
