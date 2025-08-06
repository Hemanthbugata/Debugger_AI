'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'

// Animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      delayChildren: 0.1,
      staggerChildren: 0.08,
      duration: 0.6
    }
  }
}

const itemVariants = {
  hidden: { y: 30, opacity: 0, scale: 0.9 },
  visible: {
    y: 0,
    opacity: 1,
    scale: 1,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 12,
      duration: 0.6
    }
  }
}

const cardVariants = {
  hidden: { scale: 0.8, opacity: 0, rotateY: -15 },
  visible: {
    scale: 1,
    opacity: 1,
    rotateY: 0,
    transition: {
      type: "spring",
      stiffness: 100,
      damping: 15,
      duration: 0.8
    }
  },
  hover: {
    scale: 1.05,
    y: -10,
    rotateY: 5,
    boxShadow: "0 20px 40px rgba(0,0,0,0.15)",
    transition: {
      type: "spring",
      stiffness: 400,
      damping: 10
    }
  }
}

const floatingVariants = {
  animate: {
    y: [-5, 5, -5],
    transition: {
      duration: 3,
      repeat: Infinity,
      ease: "easeInOut"
    }
  }
}

const pulseVariants = {
  animate: {
    scale: [1, 1.05, 1],
    opacity: [0.8, 1, 0.8],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: "easeInOut"
    }
  }
}

export default function Home() {
  const [error, setError] = useState('')
  const [result, setResult] = useState<string | null>(null)
  const [summary, setSummary] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [references, setReferences] = useState<Array<{ title: string, link: string }>>([])
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)
    setReferences([])
    setSummary(null)
    try {
      const res = await fetch('http://localhost:8000/debug/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ error })
      })
      const data = await res.json()
      setSummary(data.summary || null)
      setResult(data.fix || data.result || JSON.stringify(data, null, 2))
      setReferences(data.sources || [])
    } catch (err) {
      setSummary(null)
      setResult('Error connecting to backend.')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 1200)
  }

  const renderResult = () => {
    if (!result) return null
    const codeRegex = /```([a-zA-Z0-9]*\n)?([\s\S]*?)```/g
    let lastIndex = 0
    let match: RegExpExecArray | null
    const elements = []
    let idx = 0
    
    while ((match = codeRegex.exec(result)) !== null) {
      if (match.index > lastIndex) {
        let text = result.slice(lastIndex, match.index)
        text = text.replace(/[\*'`]/g, '')
        elements.push(
          <motion.div 
            key={idx++} 
            className="chatgpt-text"
            initial={{ opacity: 0, y: 10, x: -10 }}
            animate={{ opacity: 1, y: 0, x: 0 }}
            transition={{ delay: idx * 0.1, type: "spring", stiffness: 100 }}
          >
            {text}
          </motion.div>
        )
      }
      let code = match[2].replace(/[\*'`]/g, '')
      elements.push(
        <motion.div 
          key={idx++} 
          className="chatgpt-code-block"
          initial={{ opacity: 0, scale: 0.9, rotateX: -10 }}
          animate={{ opacity: 1, scale: 1, rotateX: 0 }}
          transition={{ delay: idx * 0.15, type: "spring", stiffness: 120 }}
          whileHover={{ scale: 1.02, boxShadow: "0 10px 30px rgba(0,0,0,0.1)" }}
        >
          <pre><code>{code}</code></pre>
          <motion.button 
            className="copy-btn" 
            onClick={() => handleCopy(code)}
            whileHover={{ scale: 1.05, backgroundColor: "#0fd39f" }}
            whileTap={{ scale: 0.95 }}
            animate={copied ? { scale: [1, 1.1, 1], backgroundColor: "#22c55e" } : {}}
          >
            <motion.span
              animate={copied ? { rotate: [0, 360] } : {}}
              transition={{ duration: 0.5 }}
            >
              {copied ? '✓ Copied!' : '📋 Copy'}
            </motion.span>
          </motion.button>
        </motion.div>
      )
      lastIndex = match.index + match[0].length
    }
    
    if (lastIndex < result.length) {
      let text = result.slice(lastIndex).replace(/[\*'`]/g, '')
      elements.push(
        <motion.div 
          key={idx++} 
          className="chatgpt-text"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.1 }}
        >
          {text}
        </motion.div>
      )
    }
    
    if (elements.length === 0) {
      return (
        <motion.div 
          className="chatgpt-text"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: "spring", stiffness: 100 }}
        >
          {result.replace(/[\*'`]/g, '')}
        </motion.div>
      )
    }
    return elements
  }

  return (
    <div className="app-responsive-container">
      {/* Animated background elements */}
      <motion.div
        className="fixed inset-0 -z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-green-50" />
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-blue-300 rounded-full opacity-30"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [-20, 20, -20],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </motion.div>

      <motion.nav 
        className="navbar"
        initial={{ y: -80, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ type: "spring", stiffness: 100, damping: 20, delay: 0.2 }}
      >
        <motion.div 
          className="logo-box"
          whileHover={{ scale: 1.1, rotate: 2 }}
          whileTap={{ scale: 0.95 }}
        >
          <motion.div 
            className="logo-img bug-icon"
            animate={{ 
              rotate: [0, 10, -10, 0],
              scale: [1, 1.1, 1]
            }}
            transition={{ 
              duration: 4, 
              repeat: Infinity, 
              repeatDelay: 2,
              ease: "easeInOut"
            }}
            whileHover={{ scale: 1.2, rotate: 360 }}
          >
            🐞
          </motion.div>
          <span className="logo-text">Debugger <span className="ai-gradient">AI</span></span>
        </motion.div>
        <motion.div 
          className="nav-links"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {['Features', 'Live Demo', 'Testimonials'].map((item, idx) => (
            <motion.div 
              key={item}
              variants={itemVariants}
              whileHover={{ scale: 1.1, y: -2 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link href={`#${item.toLowerCase().replace(' ', '')}`} className="nav-link">
                {item}
              </Link>
            </motion.div>
          ))}
        </motion.div>
      </motion.nav>

      <motion.div 
        className="announcement"
        initial={{ scale: 0, opacity: 0, rotate: -5 }}
        animate={{ scale: 1, opacity: 1, rotate: 0 }}
        transition={{ 
          delay: 0.5, 
          type: "spring", 
          stiffness: 200,
          damping: 15
        }}
        variants={pulseVariants}
        whileInView="animate"
        viewport={{ once: true }}
      >
        ✨ Instantly debug your code with AI
      </motion.div>

      <motion.section 
        className="hero"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div 
          className="hero-title" 
          variants={itemVariants}
        >
          AI-Powered Error Debugging<br />
          <motion.span 
            className="highlight"
            animate={{ 
              backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"],
            }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            Fix bugs in seconds
          </motion.span>
        </motion.div>
        <motion.div 
          className="hero-desc" 
          variants={itemVariants}
          animate="animate"
        >
          Paste your error message. Let AI suggest instant solutions for Python, JavaScript, and more.
        </motion.div>
        <motion.div variants={itemVariants}>
          <Link href="#demo" style={{ textDecoration: 'none' }}>
            <motion.button 
              className="cta-btn"
              whileHover={{ 
                scale: 1.05, 
                y: -5,
                boxShadow: "0 15px 35px rgba(15, 211, 159, 0.3)",
              }}
              whileTap={{ scale: 0.95 }}
              animate={{
                boxShadow: [
                  "0 5px 15px rgba(15, 211, 159, 0.2)",
                  "0 10px 25px rgba(15, 211, 159, 0.3)",
                  "0 5px 15px rgba(15, 211, 159, 0.2)"
                ]
              }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <motion.span
                animate={{ x: [0, 2, 0] }}
                transition={{ duration: 1.5, repeat: Infinity }}
              >
                Try Live Demo
              </motion.span>
              <motion.span 
                style={{fontSize:'1.2em', marginLeft: '8px'}}
                animate={{ rotate: [0, 45, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                ↗
              </motion.span>
            </motion.button>
          </Link>
        </motion.div>
      </motion.section>

      <motion.section 
        className="features" 
        id="features"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <motion.h2 
          className="section-title"
          initial={{ y: 50, opacity: 0, scale: 0.8 }}
          whileInView={{ y: 0, opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2, type: "spring", stiffness: 100 }}
        >
          Why Debugger AI?
        </motion.h2>
        <motion.div 
          className="features-list"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {[
            { icon: "⚡", title: "Instant Solutions", desc: "Get fixes for errors in seconds, not hours." },
            { icon: "🤖", title: "AI-Powered", desc: "Advanced LLMs analyze your code and errors." },
            { icon: "🧑‍💻", title: "Multi-Language", desc: "Supports Python, JavaScript, React, and more." },
            { icon: "🔒", title: "Secure", desc: "Your code & errors are never stored." }
          ].map((feature, idx) => (
            <motion.div 
              key={idx}
              className="feature-card"
              variants={cardVariants}
              whileHover="hover"
              whileTap={{ scale: 0.95 }}
            >
              <motion.div 
                className="feature-icon"
                animate={{ 
                  rotate: [0, 15, -15, 0],
                  scale: [1, 1.1, 1]
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity, 
                  repeatDelay: 4, 
                  delay: idx * 0.5 
                }}
                whileHover={{ 
                  scale: 1.3, 
                  rotate: 360,
                  transition: { duration: 0.5 }
                }}
              >
                {feature.icon}
              </motion.div>
              <motion.div 
                className="feature-title"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                transition={{ delay: 0.3 + idx * 0.1 }}
              >
                {feature.title}
              </motion.div>
              <motion.div 
                className="feature-desc"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                transition={{ delay: 0.4 + idx * 0.1 }}
              >
                {feature.desc}
              </motion.div>
            </motion.div>
          ))}
        </motion.div>
      </motion.section>

      <motion.section 
        className="demo" 
        id="demo"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <motion.form 
          className="demo-form" 
          onSubmit={handleSubmit}
          initial={{ y: 50, opacity: 0, scale: 0.9 }}
          whileInView={{ y: 0, opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2, type: "spring", stiffness: 100 }}
        >
          <motion.textarea
            className="demo-input"
            placeholder="Paste your error message here..."
            value={error}
            onChange={e => setError(e.target.value)}
            required
            rows={3}
            style={{minHeight: '60px'}}
            whileFocus={{ 
              scale: 1.02, 
              boxShadow: "0 0 20px rgba(15, 211, 159, 0.3)",
              borderColor: "#0fd39f"
            }}
            transition={{ type: "spring", stiffness: 300 }}
          />
          <motion.button 
            className="cta-btn" 
            type="submit" 
            disabled={loading} 
            style={{width: '100%'}}
            whileHover={{ 
              scale: loading ? 1 : 1.02,
              boxShadow: loading ? undefined : "0 10px 30px rgba(15, 211, 159, 0.3)"
            }}
            whileTap={{ scale: loading ? 1 : 0.98 }}
            animate={loading ? {
              background: [
                "linear-gradient(45deg, #0fd39f, #22c55e)",
                "linear-gradient(45deg, #22c55e, #0fd39f)",
                "linear-gradient(45deg, #0fd39f, #22c55e)"
              ]
            } : {}}
            transition={{ duration: 1, repeat: loading ? Infinity : 0 }}
          >
            <motion.span
              animate={loading ? { x: [0, 10, 0] } : {}}
              transition={{ duration: 0.8, repeat: loading ? Infinity : 0 }}
            >
              {loading ? 'Debugging...' : 'Debug Now'}
            </motion.span>
            {loading && (
              <motion.span
                className="ml-2"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              >
                ⚙️
              </motion.span>
            )}
          </motion.button>
        </motion.form>

        <AnimatePresence>
          {(summary || result) && (
            <motion.div 
              className="chatgpt-output-container"
              initial={{ opacity: 0, y: 50, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -50, scale: 0.9 }}
              transition={{ 
                type: "spring", 
                stiffness: 100,
                damping: 20
              }}
            >
              <motion.div 
                className="chatgpt-bubble ai-bubble"
                initial={{ scale: 0.8, opacity: 0, rotateY: -20 }}
                animate={{ scale: 1, opacity: 1, rotateY: 0 }}
                transition={{ delay: 0.2, type: "spring", stiffness: 100 }}
                whileHover={{ scale: 1.02, boxShadow: "0 20px 40px rgba(0,0,0,0.1)" }}
              >
                <motion.div 
                  className="chatgpt-avatar"
                  animate={{ 
                    rotate: [0, 360],
                    scale: [1, 1.1, 1]
                  }}
                  transition={{ 
                    rotate: { duration: 2, ease: "easeInOut" },
                    scale: { duration: 1, repeat: Infinity, repeatType: "reverse" }
                  }}
                >
                  🤖
                </motion.div>
                <div className="chatgpt-content">
                  {summary && (
                    <motion.div 
                      className="chatgpt-summary"
                      initial={{ opacity: 0, x: -30, scale: 0.9 }}
                      animate={{ opacity: 1, x: 0, scale: 1 }}
                      transition={{ delay: 0.4, type: "spring", stiffness: 100 }}
                    >
                      {summary}
                    </motion.div>
                  )}
                  <motion.div 
                    style={{marginTop: summary ? '0.5em' : 0}}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6 }}
                  >
                    {renderResult()}
                  </motion.div>
                </div>
              </motion.div>

              <AnimatePresence>
                {references.length > 0 && (
                  <motion.div 
                    className="references-section"
                    initial={{ opacity: 0, y: 30, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -30, scale: 0.95 }}
                    transition={{ delay: 0.8, type: "spring", stiffness: 100 }}
                  >
                    <motion.div 
                      className="references-title"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.9 }}
                    >
                      Most Relevant Community Solutions
                    </motion.div>
                    <motion.div 
                      className="references-desc"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 1.0 }}
                    >
                      The following are the most accurate solutions found for your error:
                    </motion.div>
                    <ul className="references-list">
                      {references.slice(0, 5).map((ref, idx) => (
                        <motion.li 
                          className="reference-item" 
                          key={idx}
                          initial={{ opacity: 0, x: -30, scale: 0.9 }}
                          animate={{ opacity: 1, x: 0, scale: 1 }}
                          transition={{ delay: 1.1 + idx * 0.1, type: "spring", stiffness: 100 }}
                          whileHover={{ 
                            scale: 1.03, 
                            y: -3,
                            boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
                            backgroundColor: "rgba(15, 211, 159, 0.05)"
                          }}
                        >
                          <span className={`reference-source ${ref.link && ref.link.includes('stackoverflow.com') ? 'stackoverflow' : ref.link && ref.link.includes('reddit.com') ? 'reddit' : ''}`}>
                            {ref.link && ref.link.includes('stackoverflow.com') ? 'StackOverflow' : ref.link && ref.link.includes('reddit.com') ? 'Reddit' : 'Source'}:
                          </span>
                          <motion.a
                            className="reference-link"
                            href={ref.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                          >
                            {ref.title}
                          </motion.a>
                        </motion.li>
                      ))}
                    </ul>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.section>

      <motion.section 
        className="testimonials" 
        id="testimonials"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <motion.h2 
          className="section-title"
          initial={{ y: 50, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2, type: "spring", stiffness: 100 }}
        >
          What Users Say
        </motion.h2>
        <motion.div 
          className="testimonials-list"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {[
            { quote: "Fixed my Python bug in 10 seconds. Amazing!", user: "Jimmy, Data Scientist" },
            { quote: "Way better than searching Stack Overflow for hours.", user: "Alex, Web Developer" },
            { quote: "The live demo is a game changer for learning.", user: "Sam, Student" }
          ].map((testimonial, idx) => (
            <motion.div 
              key={idx}
              className="testimonial-card"
              variants={cardVariants}
              whileHover={{ 
                scale: 1.05, 
                y: -8,
                boxShadow: "0 15px 35px rgba(0,0,0,0.15)",
                rotateY: 2
              }}
              whileTap={{ scale: 0.95 }}
            >
              <motion.div 
                className="testimonial-quote"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                transition={{ delay: 0.3 + idx * 0.1 }}
              >
                "{testimonial.quote}"
              </motion.div>
              <motion.div 
                className="testimonial-user"
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + idx * 0.1 }}
              >
                — {testimonial.user}
              </motion.div>
            </motion.div>
          ))}
        </motion.div>
      </motion.section>

      <motion.footer 
        className="footer"
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <motion.div
          whileHover={{ scale: 1.02 }}
        >
          © {new Date().getFullYear()} Debugger AI &middot; 
          <motion.a 
            href="https://github.com/Hemanthbugata" 
            target="_blank" 
            rel="noopener" 
            className="footer-link"
            whileHover={{ scale: 1.1, color: "#0fd39f" }}
          >
            GitHub
          </motion.a> &middot; 
          <motion.a 
            href="#" 
            className="footer-link"
            whileHover={{ scale: 1.1, color: "#0fd39f" }}
          >
            Docs
          </motion.a>
        </motion.div>
      </motion.footer>
    </div>
  )
}
