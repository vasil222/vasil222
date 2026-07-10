import { About } from '@/components/about'
import { CursorGlow } from '@/components/cursor-glow'
import { FinalCta } from '@/components/final-cta'
import { Hero } from '@/components/hero'
import { How } from '@/components/how'
import { LiveRound } from '@/components/live-round'
import { Marquee } from '@/components/marquee'
import { Roadmap } from '@/components/roadmap'
import { SiteFooter } from '@/components/site-footer'
import { SiteHeader } from '@/components/site-header'
import { Tokenomics } from '@/components/tokenomics'

export default function Page() {
  return (
    <>
      <CursorGlow />
      <div className="page-grid" aria-hidden="true" />
      <SiteHeader />
      <main className="relative z-[1]">
        <Hero />
        <Marquee />
        <About />
        <How />
        <Tokenomics />
        <LiveRound />
        <Roadmap />
        <FinalCta />
      </main>
      <SiteFooter />
    </>
  )
}
