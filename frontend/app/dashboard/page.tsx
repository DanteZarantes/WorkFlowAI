'use client'

import { useState, useEffect } from 'react'

export default function Dashboard() {
  const [user, setUser] = useState(null)

  return (
    <div className="dashboard-grid" style={{ paddingTop: '100px' }}>
      <aside style={{ background: 'white', borderRadius: '20px', padding: '2rem' }}>
        <h3>Quick Actions</h3>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <button style={{ padding: '1rem', border: 'none', borderRadius: '10px', background: '#f8f9fa' }}>
            Edit Profile
          </button>
          <button style={{ padding: '1rem', border: 'none', borderRadius: '10px', background: '#f8f9fa' }}>
            Settings
          </button>
        </div>
      </aside>

      <main style={{ background: 'white', borderRadius: '20px', padding: '2rem' }}>
        <h1>Dashboard</h1>
        <div className="grid-container">
          <div className="grid-item">
            <h3>📊 Analytics</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <div style={{ fontSize: '2rem', color: '#667eea' }}>24</div>
                <div>Visits</div>
              </div>
              <div>
                <div style={{ fontSize: '2rem', color: '#667eea' }}>12</div>
                <div>Actions</div>
              </div>
            </div>
          </div>
          <div className="grid-item">
            <h3>🔔 Notifications</h3>
            <div>Welcome to ModernSite!</div>
          </div>
        </div>
      </main>

      <aside style={{ background: 'white', borderRadius: '20px', padding: '2rem' }}>
        <h3>Activity</h3>
        <div>Recent login</div>
      </aside>
    </div>
  )
}