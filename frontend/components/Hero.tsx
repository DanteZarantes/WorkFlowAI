'use client'

import { useState, useEffect } from 'react'

export default function Hero() {
  const [shapes, setShapes] = useState([
    { id: 1, x: 10, y: 20, size: 80 },
    { id: 2, x: 80, y: 60, size: 120 },
    { id: 3, x: 70, y: 30, size: 60 }
  ])

  useEffect(() => {
    const interval = setInterval(() => {
      setShapes(prev => prev.map(shape => ({
        ...shape,
        x: shape.x + (Math.random() - 0.5) * 2,
        y: shape.y + (Math.random() - 0.5) * 2
      })))
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  return (
    <section className="hero-grid" style={{ position: 'relative', overflow: 'hidden' }}>
      <div className="hero-content" style={{ zIndex: 2 }}>
        <h1 style={{ fontSize: '3.5rem', fontWeight: '700', color: 'white', marginBottom: '1rem' }}>
          Welcome to ModernSite
        </h1>
        <p style={{ fontSize: '1.3rem', color: 'rgba(255,255,255,0.9)', marginBottom: '2rem' }}>
          Experience React, Next.js, and CSS Grid in perfect harmony
        </p>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button style={{
            padding: '15px 30px',
            background: 'linear-gradient(45deg, #667eea, #764ba2)',
            color: 'white',
            border: 'none',
            borderRadius: '50px',
            fontWeight: '600',
            cursor: 'pointer'
          }}>
            Get Started
          </button>
          <button style={{
            padding: '15px 30px',
            background: 'transparent',
            color: 'white',
            border: '2px solid white',
            borderRadius: '50px',
            fontWeight: '600',
            cursor: 'pointer'
          }}>
            Learn More
          </button>
        </div>
      </div>
      
      <div className="hero-animation" style={{ position: 'relative' }}>
        {shapes.map(shape => (
          <div
            key={shape.id}
            style={{
              position: 'absolute',
              width: `${shape.size}px`,
              height: `${shape.size}px`,
              background: 'rgba(255,255,255,0.1)',
              borderRadius: '50%',
              left: `${shape.x}%`,
              top: `${shape.y}%`,
              transition: 'all 2s ease',
              animation: `float${shape.id} 6s ease-in-out infinite`
            }}
          />
        ))}
      </div>
      
      <style jsx>{`
        @keyframes float1 {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
        @keyframes float2 {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-30px) rotate(180deg); }
        }
        @keyframes float3 {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-15px) rotate(180deg); }
        }
      `}</style>
    </section>
  )
}