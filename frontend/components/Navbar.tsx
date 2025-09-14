'use client'

import Link from 'next/link'

interface NavbarProps {
  user: any
}

export default function Navbar({ user }: NavbarProps) {
  return (
    <nav className="navbar-grid">
      <div className="logo">
        <Link href="/" style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#667eea', textDecoration: 'none' }}>
          ModernSite
        </Link>
      </div>
      
      <div className="nav-links" style={{ display: 'flex', gap: '2rem', justifyContent: 'center' }}>
        <Link href="/" style={{ textDecoration: 'none', color: '#333', fontWeight: '500' }}>Home</Link>
        <Link href="/about" style={{ textDecoration: 'none', color: '#333', fontWeight: '500' }}>About</Link>
        <Link href="/services" style={{ textDecoration: 'none', color: '#333', fontWeight: '500' }}>Services</Link>
        <Link href="/contact" style={{ textDecoration: 'none', color: '#333', fontWeight: '500' }}>Contact</Link>
      </div>
      
      <div className="auth-links" style={{ display: 'flex', gap: '1rem' }}>
        {user ? (
          <>
            <Link href="/dashboard" style={{ textDecoration: 'none', color: '#667eea' }}>Dashboard</Link>
            <button onClick={() => window.location.href = '/api/auth/logout/'}>Logout</button>
          </>
        ) : (
          <>
            <Link href="/login" style={{ textDecoration: 'none', color: '#667eea' }}>Login</Link>
            <Link href="/signup" style={{ textDecoration: 'none', color: '#667eea' }}>Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  )
}