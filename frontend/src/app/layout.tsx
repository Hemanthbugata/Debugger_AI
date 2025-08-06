// app/layout.tsx
import './globals.css'
import { Inter } from 'next/font/google'
import type { Metadata } from 'next'
import AnimatedLayout from './AnimatedLayout'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Debugger AI - AI-Powered Error Debugging',
  description: 'Fix bugs in seconds with AI-powered debugging for Python, JavaScript, React, and more.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className={inter.className}>
        <AnimatedLayout>
          {children}
        </AnimatedLayout>
      </body>
    </html>
  )
}
