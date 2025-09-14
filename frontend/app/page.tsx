'use client'

import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Hero from '../components/Hero'
import Features from '../components/Features'

export default function Home() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    // Check authentication status
    fetch('/api/auth/user/')
      .then(res => res.json())
      .then(data => setUser(data))
      .catch(() => setUser(null))
  }, [])

  return (
    <main>
      <Navbar user={user} />
      <Hero />
      <Features />
    </main>
  )
}