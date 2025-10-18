import { useEffect, useRef } from 'react'
import { motion, useScroll, useTransform, useInView } from 'framer-motion'

// ============================================
// LANDING PAGE COMPONENT
// Premium AI-powered insurance assistant
// ============================================
export default function LandingPage() {
  const backgroundRef = useRef(null)
  const { scrollYProgress } = useScroll()
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.5], [1, 0.8])

  // ============================================
  // Create floating orbs with pure CSS animations
  // ============================================
  useEffect(() => {
    const container = backgroundRef.current
    if (!container) return

    const orbs = []
    // Create 15 floating orbs
    for (let i = 0; i < 15; i++) {
      const orb = document.createElement('div')
      
      // Random positioning and size
      const x = Math.random() * 100
      const y = Math.random() * 100
      const size = Math.random() * 150 + 50
      const duration = Math.random() * 10 + 10 // 10-20s
      const delay = Math.random() * 5
      
      orb.style.cssText = `
        position: absolute;
        left: ${x}%;
        top: ${y}%;
        width: ${size}px;
        height: ${size}px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, rgba(59, 130, 246, 0.1) 100%);
        filter: blur(40px);
        pointer-events: none;
        animation: float ${duration}s ease-in-out ${delay}s infinite;
      `
      
      container.appendChild(orb)
      orbs.push(orb)
    }

    // Cleanup
    return () => {
      orbs.forEach(orb => orb.remove())
    }
  }, [])

  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      {/* ============================================
          Animated Background with Orbs
          ============================================ */}
      <div 
        ref={backgroundRef} 
        className="fixed inset-0 -z-10"
        style={{ 
          background: 'linear-gradient(135deg, #0a0a0f 0%, #1e1b4b 50%, #312e81 100%)'
        }}
      />

      {/* ============================================
          HERO SECTION
          Bold tagline with smooth animations
          ============================================ */}
      <motion.section 
        className="relative min-h-screen flex flex-col items-center justify-center px-6 md:px-12 lg:px-24"
        style={{ opacity, scale }}
      >
        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgyNTUsMjU1LDI1NSwwLjAzKSIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] opacity-30" />

        <motion.div
          className="relative z-10 text-center max-w-5xl"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ 
            duration: 1, 
            ease: [0.22, 1, 0.36, 1] 
          }}
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2, duration: 0.6 }}
            className="inline-block mb-6"
          >
            <span className="px-4 py-2 rounded-full bg-gradient-to-r from-blue-500/10 to-purple-500/10 backdrop-blur-sm border border-blue-500/20 text-blue-300 text-sm font-medium">
              ✨ AI-Powered Insurance Assistant
            </span>
          </motion.div>

          {/* Main Headline */}
          <motion.h1
            className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ 
              delay: 0.3, 
              duration: 0.8,
              ease: [0.22, 1, 0.36, 1]
            }}
            whileHover={{ 
              scale: 1.02,
              transition: { duration: 0.3 }
            }}
          >
            Claim Smarter,
            <br />
            Not Harder.
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            className="text-xl md:text-2xl text-gray-300 mb-10 max-w-2xl mx-auto leading-relaxed"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.8 }}
          >
            AI-powered insights to simplify your insurance experience.
            <br />
            <span className="text-blue-400">Fast. Smart. Effortless.</span>
          </motion.p>

          {/* CTA Button with Glow */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.6 }}
          >
            <motion.button
              className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg font-semibold rounded-full overflow-hidden shadow-2xl"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
            >
              {/* Glow effect */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 opacity-0 group-hover:opacity-100 blur-xl"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0, 0.5, 0]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              
              <span className="relative z-10 flex items-center gap-1">
                Get Started
                <motion.span
                  animate={{ x: [0, 5, 0] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                >
                  →
                </motion.span>
              </span>
            </motion.button>
          </motion.div>

          {/* Stats or Social Proof */}
          <motion.div
            className="mt-16 flex flex-wrap justify-center gap-8 md:gap-12"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 0.8 }}
          >
            {[
              { value: '10K+', label: 'Active Users' },
              { value: '98%', label: 'Satisfaction' },
              { value: '$2M+', label: 'Claims Processed' }
            ].map((stat, i) => (
              <motion.div
                key={i}
                className="text-center"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 + i * 0.1 }}
              >
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-400 mt-1">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="w-6 h-10 border-2 border-blue-400/30 rounded-full flex justify-center pt-2">
            <motion.div
              className="w-1.5 h-1.5 bg-blue-400 rounded-full"
              animate={{ y: [0, 16, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </div>
        </motion.div>
      </motion.section>

      {/* ============================================
          FEATURES SECTION
          4 cards with scroll-triggered animations
          ============================================ */}
      <section className="relative py-24 px-6 md:px-12 lg:px-24">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          className="max-w-7xl mx-auto"
        >
          {/* Section Header */}
          <div className="text-center mb-16">
            <motion.h2
              className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
            >
              Powerful Features
            </motion.h2>
            <motion.p
              className="text-gray-400 text-lg max-w-2xl mx-auto"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
            >
              Everything you need to make smarter insurance decisions, powered by AI
            </motion.p>
          </div>

          {/* Feature Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: '📊',
                title: 'Coverage Summary',
                description: 'See deductibles, out-of-pocket costs, and gaps at a glance',
                gradient: 'from-blue-500/20 to-cyan-500/20',
                border: 'border-blue-500/30'
              },
              {
                icon: '🤖',
                title: 'Smart Recommendations',
                description: 'AI-backed prioritized action items to reduce your risk',
                gradient: 'from-purple-500/20 to-pink-500/20',
                border: 'border-purple-500/30'
              },
              {
                icon: '📈',
                title: 'Insights & Charts',
                description: 'Beautiful visualizations to explain tradeoffs and savings',
                gradient: 'from-cyan-500/20 to-blue-500/20',
                border: 'border-cyan-500/30'
              },
              {
                icon: '👤',
                title: 'Personalized Analysis',
                description: 'Tailored to your lifestyle and financial goals',
                gradient: 'from-pink-500/20 to-purple-500/20',
                border: 'border-pink-500/30'
              }
            ].map((feature, index) => (
              <FeatureCard 
                key={index} 
                feature={feature} 
                index={index} 
              />
            ))}
          </div>
        </motion.div>
      </section>

      {/* ============================================
          FOOTER
          Minimal footer with gradient line
          ============================================ */}
      <motion.footer
        className="relative py-8 px-6 border-t border-white/5"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        {/* Gradient line */}
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-50" />
        
        <div className="max-w-7xl mx-auto text-center">
          <motion.p
            className="text-gray-400 text-sm"
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            Built with <span className="text-purple-400">💜</span> by{' '}
            <span className="font-semibold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              BullDawg Hackers
            </span>
          </motion.p>
          
          <motion.div
            className="mt-4 flex justify-center gap-6 text-gray-500 text-xs"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
          >
            <a href="#" className="hover:text-blue-400 transition-colors">Privacy</a>
            <a href="#" className="hover:text-blue-400 transition-colors">Terms</a>
            <a href="#" className="hover:text-blue-400 transition-colors">Contact</a>
          </motion.div>
        </div>
      </motion.footer>
    </div>
  )
}

// ============================================
// FEATURE CARD COMPONENT
// Individual feature card with hover effects
// ============================================
function FeatureCard({ feature, index }) {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.5 })

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{
        duration: 0.6,
        delay: index * 0.1,
        ease: [0.22, 1, 0.36, 1]
      }}
      whileHover={{ 
        y: -10,
        transition: { duration: 0.3 }
      }}
      className={`group relative p-8 rounded-2xl bg-gradient-to-br ${feature.gradient} backdrop-blur-xl border ${feature.border} overflow-hidden`}
    >
      {/* Hover glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:to-purple-500/10 transition-all duration-500" />
      
      {/* Icon */}
      <motion.div
        className="text-5xl mb-4 inline-block"
        whileHover={{ 
          scale: 1.2,
          rotate: [0, -10, 10, 0],
          transition: { duration: 0.5 }
        }}
      >
        {feature.icon}
      </motion.div>

      {/* Content */}
      <h3 className="text-xl font-bold text-white mb-3 relative z-10">
        {feature.title}
      </h3>
      <p className="text-gray-300 text-sm leading-relaxed relative z-10">
        {feature.description}
      </p>

      {/* Animated corner accent */}
      <motion.div
        className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-500/20 to-transparent rounded-bl-full"
        initial={{ scale: 0, opacity: 0 }}
        animate={isInView ? { scale: 1, opacity: 1 } : {}}
        transition={{ delay: index * 0.1 + 0.3 }}
      />
    </motion.div>
  )
}
