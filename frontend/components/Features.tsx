'use client'

const features = [
  {
    icon: '🚀',
    title: 'React/Next.js',
    description: 'Modern React with Next.js for optimal performance and SEO'
  },
  {
    icon: '🎨',
    title: 'CSS Grid Layout',
    description: 'Advanced CSS Grid for responsive and flexible layouts'
  },
  {
    icon: '⚡',
    title: 'Django API',
    description: 'Powerful Django backend with REST API integration'
  },
  {
    icon: '📱',
    title: 'Responsive Design',
    description: 'Mobile-first approach with perfect display on all devices'
  },
  {
    icon: '🔒',
    title: 'Authentication',
    description: 'Secure user authentication and profile management'
  },
  {
    icon: '✨',
    title: 'Animations',
    description: 'Smooth animations and interactive micro-interactions'
  }
]

export default function Features() {
  return (
    <section style={{ padding: '4rem 0', background: 'white' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ fontSize: '2.5rem', color: '#333', marginBottom: '1rem' }}>
          Modern Tech Stack
        </h2>
        <p style={{ fontSize: '1.2rem', color: '#666' }}>
          Built with the latest technologies for optimal performance
        </p>
      </div>
      
      <div className="grid-container">
        {features.map((feature, index) => (
          <div key={index} className="grid-item" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>
              {feature.icon}
            </div>
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: '#333' }}>
              {feature.title}
            </h3>
            <p style={{ color: '#666', lineHeight: '1.6' }}>
              {feature.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  )
}