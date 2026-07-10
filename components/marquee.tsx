const items = ['X5 MEME COIN', 'BUY • HOLD • WIN', 'COMMUNITY POWERED', 'UP TO X5 REWARD']

export function Marquee() {
  const loop = [...items, ...items, ...items]
  return (
    <section className="overflow-hidden border-y border-brand/[0.14] bg-[#080b08]" aria-hidden="true">
      <div className="animate-marquee flex w-max gap-[34px] py-[18px] font-display font-bold text-brand">
        {loop.map((item, i) => (
          <span key={i} className="flex items-center gap-[34px]">
            {item}
            <i className="not-italic text-gold">✦</i>
          </span>
        ))}
      </div>
    </section>
  )
}
