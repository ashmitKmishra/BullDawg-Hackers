import { useAuth0 } from '@auth0/auth0-react'
import LoginButton from './components/LoginButton'
import LogoutButton from './components/LogoutButton'
import Profile from './components/Profile'
import PDFUpload from './components/PDFUpload'
import './App.css'

function App() {
  const { isAuthenticated, isLoading, error } = useAuth0()

  if (isLoading) {
    return <div>Loading...</div>
  }

  // Handle Auth0 errors (like existing account)
  if (error) {
    return (
      <div className="App">
        <h1>Benefits & Financial Wellness Advisor</h1>
        <div className="error-section">
          <h2>Authentication Error</h2>
          <p className="error-message">{error.message}</p>
          {error.message.toLowerCase().includes('already') || 
           error.message.toLowerCase().includes('exist') ? (
            <div className="error-help">
              <p>It looks like you already have an account.</p>
              <LoginButton />
            </div>
          ) : (
            <LoginButton />
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="App">
      <h1>Benefits & Financial Wellness Advisor</h1>
      <div className="auth-section">
        {!isAuthenticated ? (
          <LoginButton />
        ) : (
          <>
            <Profile />
            <LogoutButton />
          </>
        )}
      </div>
      {isAuthenticated && (
        <div className="main-content">
          <PDFUpload />
          <div className="content">
            <p>Welcome! Upload your benefits PDF above to get AI-powered insurance plan recommendations.</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
