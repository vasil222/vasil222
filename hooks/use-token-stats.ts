'use client'

import useSWR from 'swr'
import type { TokenStats } from '@/app/api/token/route'

const fetcher = (url: string) => fetch(url).then((r) => r.json() as Promise<TokenStats>)

export function useTokenStats() {
  const { data, error, isLoading } = useSWR<TokenStats>('/api/token', fetcher, {
    refreshInterval: 15_000,
    revalidateOnFocus: false,
  })
  return { stats: data, error, isLoading }
}
