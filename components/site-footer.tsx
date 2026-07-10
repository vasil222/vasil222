import Image from 'next/image'

export function SiteFooter() {
  return (
    <footer className="border-t border-border py-10 pb-14">
      <div className="mx-auto grid w-[min(1200px,calc(100%-36px))] grid-cols-1 items-center gap-9 md:grid-cols-[auto_1fr_auto]">
        <div className="flex items-center gap-3">
          <Image
            src="/x5-logo.png"
            alt="X5 logo"
            width={46}
            height={46}
            className="h-[46px] w-[46px] rounded-full object-cover"
          />
          <div className="flex flex-col">
            <strong className="font-display text-[22px] leading-none">X5</strong>
            <span className="mt-1 text-[9px] tracking-[0.2em] text-brand">MEME COIN</span>
          </div>
        </div>
        <p className="max-w-[700px] text-[11px] leading-[1.6] text-[#697365]">
          X5 — концепт мем-токена для розважальних цілей. Це не фінансова порада, не гарантія прибутку та не готова
          юридична модель лотереї.
        </p>
        <span className="text-[11px] text-[#697365]">© 2026 X5</span>
      </div>
    </footer>
  )
}
