'use client'

import { useWallet } from '@solana/wallet-adapter-react'
import type { WalletName } from '@solana/wallet-adapter-base'
import { useEffect, useRef, useState } from 'react'
import { Check, ChevronDown, Copy, LogOut, Wallet, X } from 'lucide-react'

type WalletMeta = {
  name: string
  url: string
  accent: string
}

// The three wallets we surface first. All implement the Wallet Standard and
// are auto-detected; we only need metadata for ordering + install links.
const PREFERRED: WalletMeta[] = [
  { name: 'Phantom', url: 'https://phantom.app/download', accent: '#ab9ff2' },
  { name: 'Solflare', url: 'https://solflare.com/download', accent: '#ffc244' },
  { name: 'Backpack', url: 'https://backpack.app/download', accent: '#e33e3f' },
]

function truncate(address: string) {
  return `${address.slice(0, 4)}...${address.slice(-4)}`
}

export function WalletButton({ className = '' }: { className?: string }) {
  const { wallets, select, connect, disconnect, connecting, connected, publicKey, wallet } = useWallet()
  const [modalOpen, setModalOpen] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [pending, setPending] = useState<WalletName | null>(null)
  const [copied, setCopied] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  // After selecting a wallet, connect once the adapter is active.
  useEffect(() => {
    if (pending && wallet?.adapter.name === pending && !connected && !connecting) {
      connect().catch(() => {}).finally(() => setPending(null))
    }
  }, [pending, wallet, connected, connecting, connect])

  // Close the modal automatically once connected.
  useEffect(() => {
    if (connected) setModalOpen(false)
  }, [connected])

  // Close the dropdown on outside click.
  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setMenuOpen(false)
    }
    document.addEventListener('mousedown', onClick)
    return () => document.removeEventListener('mousedown', onClick)
  }, [])

  function handleSelect(name: string) {
    const detected = wallets.find((w) => w.adapter.name === name)
    if (!detected || detected.readyState === 'NotDetected') {
      const meta = PREFERRED.find((p) => p.name === name)
      if (meta) window.open(meta.url, '_blank', 'noopener,noreferrer')
      return
    }
    select(name as WalletName)
    setPending(name as WalletName)
  }

  async function copyAddress() {
    if (!publicKey) return
    await navigator.clipboard.writeText(publicKey.toBase58())
    setCopied(true)
    setTimeout(() => setCopied(false), 1400)
  }

  // Merge preferred metadata with detected adapters (icon + readyState).
  const list = PREFERRED.map((meta) => {
    const detected = wallets.find((w) => w.adapter.name === meta.name)
    return {
      ...meta,
      icon: detected?.adapter.icon,
      installed: detected ? detected.readyState !== 'NotDetected' : false,
    }
  })

  if (connected && publicKey) {
    return (
      <div ref={menuRef} className={`relative ${className}`}>
        <button
          type="button"
          onClick={() => setMenuOpen((v) => !v)}
          className="inline-flex items-center gap-2 rounded-full border border-brand/40 bg-brand/10 px-4 py-2.5 text-[13px] font-extrabold text-brand transition-colors hover:bg-brand/15"
        >
          {wallet?.adapter.icon && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={wallet.adapter.icon} alt="" className="h-4 w-4 rounded-full" />
          )}
          <span className="tabular-nums">{truncate(publicKey.toBase58())}</span>
          <ChevronDown className="h-3.5 w-3.5" aria-hidden />
        </button>

        {menuOpen && (
          <div className="absolute right-0 top-[calc(100%+8px)] z-50 w-52 overflow-hidden rounded-2xl border border-white/10 glass p-1.5 shadow-[0_24px_70px_rgba(0,0,0,0.5)]">
            <button
              type="button"
              onClick={copyAddress}
              className="flex w-full items-center gap-2.5 rounded-xl px-3 py-2.5 text-left text-[13px] font-semibold text-foreground/90 transition-colors hover:bg-white/5"
            >
              {copied ? <Check className="h-4 w-4 text-brand" aria-hidden /> : <Copy className="h-4 w-4" aria-hidden />}
              {copied ? 'Скопійовано' : 'Копіювати адресу'}
            </button>
            <button
              type="button"
              onClick={() => {
                disconnect().catch(() => {})
                setMenuOpen(false)
              }}
              className="flex w-full items-center gap-2.5 rounded-xl px-3 py-2.5 text-left text-[13px] font-semibold text-[#ff7a68] transition-colors hover:bg-[#ff7a68]/10"
            >
              <LogOut className="h-4 w-4" aria-hidden />
              Відключити
            </button>
          </div>
        )}
      </div>
    )
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setModalOpen(true)}
        className={`inline-flex items-center justify-center gap-2 rounded-full border border-brand/40 bg-brand/10 px-4 py-2.5 text-[13px] font-extrabold text-brand transition-colors hover:bg-brand/15 ${className}`}
      >
        <span className="h-[7px] w-[7px] rounded-full bg-brand shadow-[0_0_12px_var(--brand)]" />
        {connecting ? 'Підключення…' : 'Connect Wallet'}
      </button>

      {modalOpen && (
        <div
          className="fixed inset-0 z-[100] grid place-items-center bg-black/70 p-4 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-label="Підключити гаманець"
          onClick={() => setModalOpen(false)}
        >
          <div
            className="w-full max-w-[380px] rounded-3xl border border-white/10 glass-brand p-6 shadow-[0_30px_90px_rgba(0,0,0,0.6)]"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-5 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <span className="grid h-9 w-9 place-items-center rounded-xl bg-brand/15 text-brand">
                  <Wallet className="h-[18px] w-[18px]" aria-hidden />
                </span>
                <div>
                  <h2 className="font-display text-[17px] leading-none">Підключити гаманець</h2>
                  <p className="mt-1 text-[11px] text-[#8b978a]">Solana</p>
                </div>
              </div>
              <button
                type="button"
                aria-label="Закрити"
                onClick={() => setModalOpen(false)}
                className="grid h-8 w-8 place-items-center rounded-lg text-[#8b978a] transition-colors hover:bg-white/5 hover:text-foreground"
              >
                <X className="h-4 w-4" aria-hidden />
              </button>
            </div>

            <div className="flex flex-col gap-2">
              {list.map((w) => (
                <button
                  key={w.name}
                  type="button"
                  onClick={() => handleSelect(w.name)}
                  className="group flex items-center justify-between rounded-2xl border border-white/10 bg-white/[0.02] px-4 py-3.5 text-left transition-colors hover:border-brand/40 hover:bg-brand/[0.06]"
                >
                  <span className="flex items-center gap-3">
                    {w.icon ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={w.icon} alt="" className="h-8 w-8 rounded-lg" />
                    ) : (
                      <span
                        className="grid h-8 w-8 place-items-center rounded-lg text-[13px] font-extrabold text-[#0a0a0a]"
                        style={{ background: w.accent }}
                      >
                        {w.name[0]}
                      </span>
                    )}
                    <span className="text-[14px] font-bold">{w.name}</span>
                  </span>
                  <span className="text-[10px] font-extrabold tracking-wide text-[#8b978a] group-hover:text-brand">
                    {w.installed ? 'ВИЯВЛЕНО' : 'ВСТАНОВИТИ'}
                  </span>
                </button>
              ))}
            </div>

            <p className="mt-5 text-center text-[11px] leading-relaxed text-[#77836f]">
              Підключаючи гаманець, ви погоджуєтесь із умовами використання. X5 ніколи не запросить вашу seed-фразу.
            </p>
          </div>
        </div>
      )}
    </>
  )
}
