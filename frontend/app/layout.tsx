import './globals.css'

export const metadata = {
  title: 'Modern Website',
  description: 'A modern website with React and Django',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}