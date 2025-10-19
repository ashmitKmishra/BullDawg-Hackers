import React from 'react'
import { useLocation, Navigate } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'

export default function RequireAuth({ children }) {
  const { isAuthenticated, isLoading } = useAuth0()
  const location = useLocation()

  if (isLoading) {
    return null
  }

  if (!isAuthenticated) {
    return <Navigate to="/signup" replace state={{ from: location }} />
  }

  return children
}
