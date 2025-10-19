import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Welcome from './pages/Welcome'
import Signup from './pages/Signup'
import Questionnaire from './pages/Questionnaire'
import Dashboard from './pages/Dashboard'
import LandingPage from './pages/LandingPage'
import './App.css'
import RequireAuth from './components/RequireAuth'

function AnimatedRoutes(){
  const location = useLocation()
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Welcome />} />
        <Route path="/landing" element={<LandingPage />} />
        <Route path="/signup" element={<Signup />} />
  <Route path="/questionnaire" element={<RequireAuth><Questionnaire /></RequireAuth>} />
  <Route path="/dashboard" element={<RequireAuth><Dashboard /></RequireAuth>} />
      </Routes>
    </AnimatePresence>
  )
}

export default function App(){
  return (
    <BrowserRouter>
      <AnimatedRoutes />
    </BrowserRouter>
  )
}
