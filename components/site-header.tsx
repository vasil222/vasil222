'use client'

import Image from 'next/image'
import { useState } from 'react'

const links = [
  { href: '#about', label: 'Про X5' },
  { href: '#how', label: 'Як це працює' },
  { href: '#tokenomics', label: 'Токеноміка' },
  { href: '#roadmap', label: 'Roadmap' },
]

export function SiteHeader() {
  const [open, setOpen] = useState(false)

  return (
    <header className="fixed top-0 z-50 w-full border-b border-white/[0.055] bg-background/70 backdrop-blur-xl">
      <div className="mx-auto flex h-[82px] w-[min(1200px,calc(100%-36px))] items-center justify-between">
        <a href="#home" className="flex items-center gap-3">
          <Image
            src="/x5-logo.png"
            alt="X5 logo"
            width={46}
            height={46}
            className="h-[46px] w-[46px] rounded-full object-cover shadow-[0_0_28px_rgba(140,255,33,0.2)]"
            priority
          />
          <span className="flex flex-col">
            <strong className="font-display text-[22px] leading-none">X5</strong>
            <span className="mt-1 text-[9px] tracking-[0.2em] text-brand">MEME COIN</span>
          </span>
        </a>

        <button
          type="button"
          className="flex flex-col gap-[6px] p-1 md:hidden"
          aria-label="Меню"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          <span className="block h-0.5 w-6 bg-foreground transition" />
          <span className="block h-0.5 w-6 bg-foreground transition" />
          <span className="block h-0.5 w-6 bg-foreground transition" />
        </button>

        <nav
          className={`${
            open ? 'flex' : 'hidden'
          } absolute inset-x-[18px] top-[82px] flex-col items-stretch gap-4 rounded-2xl border border-border bg-card p-6 text-[13px] font-bold md:static md:flex md:flex-row md:items-center md:gap-[30px] md:border-0 md:bg-transparent md:p-0`}
        >
          {links.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={() => setOpen(false)}
              className="text-[#bbc4b8] transition-colors hover:text-brand"
            >
              {link.label}
            </a>
          ))}
          <a
            href="#buy"
            onClick={() => setOpen(false)}
            className="rounded-full border border-brand/40 px-[18px] py-3 text-center text-brand transition-colors hover:bg-brand/10"
          >
            Купити X5
          </a>
        </nav>
      </div>
    </header>
  )
}
