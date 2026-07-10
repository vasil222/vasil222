import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import { Manrope, Space_Grotesk } from 'next/font/google'
import './globals.css'

const manrope = Manrope({
  subsets: ['latin', 'cyrillic'],
  weight: ['400', '500', '600', '700', '800'],
  variable: '--font-manrope',
  display: 'swap',
})

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  weight: ['500', '600', '700'],
  variable: '--font-space-grotesk',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'X5 — Buy. Hold. Win.',
  description: 'X5 — мемкоїн з бонусними раундами та шансом отримати винагороду до x5 від суми покупки.',
  generator: 'v0.app',
  openGraph: {
    title: 'X5 — Buy. Hold. Win.',
    description: 'Простий мемкоїн із бонусними раундами. Купуй X5, тримай та отримуй шанс на винагороду до x5.',
    images: ['/x5-logo.png'],
  },
  icons: {
    icon: '/x5-logo.png',
    apple: '/x5-logo.png',
  },
}

export const viewport: Viewport = {
  colorScheme: 'dark',
  themeColor: '#050805',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="uk" className={`${manrope.variable} ${spaceGrotesk.variable} bg-background`}>
      <body className="font-sans antialiased">
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
