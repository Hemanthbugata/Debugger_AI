import './App.css'
import { useState } from 'react'

function App() {
  const [error, setError] = useState('')
  const [result, setResult] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [references, setReferences] = useState<Array<{title: string, url: string, excerpt: string, source: string}>>([])
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)
    setReferences([])
    try {
      const res = await fetch('http://localhost:8000/debug/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ error })
      })
      const data = await res.json()
      setResult(data.result || data.fix || JSON.stringify(data, null, 2))
      setReferences(data.sources || [])
    } catch (err) {
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

  // Render output in chat style, code blocks with copy button
  const renderResult = () => {
    if (!result) return null
    // Remove stars, single quotes, and backticks from code blocks and text
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
          <div className="chatgpt-text copilot-text" key={idx++}>{text}</div>
        )
      }
      let code = match[2].replace(/[\*'`]/g, '')
      elements.push(
        <div className="chatgpt-code-block copilot-code-block" key={idx++}>
          <pre><code>{code}</code></pre>
          <button className="copy-btn" onClick={() => handleCopy(code)}>{copied ? 'Copied!' : 'Copy'}</button>
        </div>
      )
      lastIndex = match.index + match[0].length
    }
    if (lastIndex < result.length) {
      let text = result.slice(lastIndex).replace(/[\*'`]/g, '')
      elements.push(
        <div className="chatgpt-text copilot-text" key={idx++}>{text}</div>
      )
    }
    if (elements.length === 0) {
      return <div className="chatgpt-text copilot-text">{result.replace(/[\*'`]/g, '')}</div>
    }
    return elements
  }

  return (
    <div className="app-responsive-container">
      <nav className="navbar">
        <div className="logo-box">
          <div className="logo-img bug-icon">🐞</div>
          <span className="logo-text">Debugger <span className="ai-gradient">AI</span></span>
        </div>
        <div className="nav-links">
          <a href="#features" className="nav-link">Features</a>
          <a href="#demo" className="nav-link">Live Demo</a>
          <a href="#testimonials" className="nav-link">Testimonials</a>
        </div>
      </nav>
      <div className="announcement">✨ Instantly debug your code with AI</div>
      <section className="hero">
        <div className="hero-title">
          AI-Powered Error Debugging<br />
          <span className="highlight">Fix bugs in seconds</span>
        </div>
        <div className="hero-desc">
          Paste your error message. Let AI suggest instant solutions for Python, JavaScript, and more.
        </div>
        <a href="#demo" style={{ textDecoration: 'none' }}>
          <button className="cta-btn">Try Live Demo <span style={{fontSize:'1.2em'}}>↗</span></button>
        </a>
      </section>

      <section className="features" id="features">
        <h2 className="section-title">Why Debugger AI?</h2>
        <div className="features-list">
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <div className="feature-title">Instant Solutions</div>
            <div className="feature-desc">Get fixes for errors in seconds, not hours.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <div className="feature-title">AI-Powered</div>
            <div className="feature-desc">Advanced LLMs analyze your code and errors.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🧑‍💻</div>
            <div className="feature-title">Multi-Language</div>
            <div className="feature-desc">Supports Python, JavaScript, React, and more.</div>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <div className="feature-title">Secure</div>
            <div className="feature-desc">Your code & errors are never stored.</div>
          </div>
        </div>
      </section>

      <section className="demo" id="demo">
        <form className="demo-form" onSubmit={handleSubmit}>
          <textarea
            className="demo-input"
            placeholder="Paste your error message here..."
            value={error}
            onChange={e => setError(e.target.value)}
            required
            rows={3}
            style={{minHeight: '60px'}}
          />
          <button className="cta-btn" type="submit" disabled={loading} style={{width: '100%'}}>
            {loading ? 'Debugging...' : 'Get Solution'}
          </button>
        </form>
        {result && (
          <div className="chatgpt-output-container">
            <div className="chatgpt-bubble ai-bubble copilot-bubble">
              <div className="chatgpt-avatar copilot-avatar">🤖</div>
              <div className="chatgpt-content copilot-content">{renderResult()}</div>
            </div>
            {/* Show up to 5 most relevant references below the output */}
            {references.length > 0 && (
              <div className="references-section animate-fade-in">
                <div className="references-title">Most Relevant Community Solutions</div>
                <div className="references-desc">The following are the most accurate solutions found for your error:</div>
                <ul className="references-list">
                  {references.slice(0, 5).map((ref, idx) => (
                    <li className="reference-item" key={idx}>
                      <span className={`reference-source ${ref.url && ref.url.includes('stackoverflow.com') ? 'stackoverflow' : ref.url && ref.url.includes('reddit.com') ? 'reddit' : ''}`}
                        style={{fontWeight:'bold', fontSize:'1.08em'}}>
                        {ref.url && ref.url.includes('stackoverflow.com') ? <span style={{color:'#f48024'}}>StackOverflow</span> : ref.url && ref.url.includes('reddit.com') ? <span style={{color:'#ff4500'}}>Reddit</span> : 'Source'}
                        {ref.url && ref.url.includes('stackoverflow.com') ? ' (StackOverflow)' : ref.url && ref.url.includes('reddit.com') ? ' (Reddit)' : ''}:
                      </span>
                      <a
                        className="reference-link reference-link-animated"
                        href={ref.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{textDecoration:'underline', fontWeight:'600', color: ref.url && ref.url.includes('stackoverflow.com') ? '#f48024' : ref.url && ref.url.includes('reddit.com') ? '#ff4500' : '#0fd39f', cursor: 'pointer'}}
                        onClick={e => {
                          e.stopPropagation();
                          window.open(ref.url, '_blank', 'noopener,noreferrer');
                        }}
                      >
                        {ref.title}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </section>

      <section className="testimonials" id="testimonials">
        <h2 className="section-title">What Users Say</h2>
        <div className="testimonials-list">
          <div className="testimonial-card">
            <div className="testimonial-quote">“Fixed my Python bug in 10 seconds. Amazing!”</div>
            <div className="testimonial-user">— Jimmy, Data Scientist</div>
          </div>
          <div className="testimonial-card">
            <div className="testimonial-quote">“Way better than searching Stack Overflow for hours.”</div>
            <div className="testimonial-user">— Alex, Web Developer</div>
          </div>
          <div className="testimonial-card">
            <div className="testimonial-quote">“The live demo is a game changer for learning.”</div>
            <div className="testimonial-user">— Sam, Student</div>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div>© {new Date().getFullYear()} Debugger AI &middot; <a href="https://github.com/Hemanthbugata" target="_blank" rel="noopener" className="footer-link">GitHub</a> &middot; <a href="#" className="footer-link">Docs</a></div>
      </footer>
    </div>
  )
}

export default App
