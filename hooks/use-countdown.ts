'use client'

import { useEffect, useState } from 'react'

const START = 5 * 3600 + 23 * 60 + 47
const DAY = 24 * 3600

/**
 * Shared round countdown. Ticks down every second, resetting to a full
 * day when it hits zero. Returns the formatted HH:MM:SS string and the
 * progress ratio (0-1) of the current round window.
 */
export function useCountdown() {
  const [seconds, setSeconds] = useState(START)

  useEffect(() => {
    const id = setInterval(() => {
      setSeconds((prev) => (prev > 0 ? prev - 1 : DAY))
    }, 1000)
    return () => clearInterval(id)
  }, [])

  const h = String(Math.floor(seconds / 3600)).padStart(2, '0')
  const m = String(Math.floor((seconds % 3600) / 60)).padStart(2, '0')
  const s = String(seconds % 60).padStart(2, '0')

  return {
    time: `${h}:${m}:${s}`,
    progress: Math.max(0.04, seconds / DAY),
  }
}
