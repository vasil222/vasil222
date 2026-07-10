'use client'

import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react'
import { useMemo, type ReactNode } from 'react'
import { TOKEN } from '@/lib/token-config'

/**
 * Phantom, Solflare and Backpack all implement the Wallet Standard, so they
 * are auto-detected by WalletProvider with an empty adapter array. No extra
 * wallet-specific packages are required.
 */
export function SolanaProvider({ children }: { children: ReactNode }) {
  const endpoint = useMemo(() => TOKEN.rpcEndpoint, [])

  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={[]} autoConnect>
        {children}
      </WalletProvider>
    </ConnectionProvider>
  )
}
