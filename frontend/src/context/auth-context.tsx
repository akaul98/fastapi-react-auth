'use client'

import React, { createContext, useCallback, useEffect, useState } from 'react'
import type { LoginContextType, User, OTPSendResponse, OTPVerifyResponse } from '@/lib/types'
import { apiClient, getErrorMessage } from '@/lib/api'
import { email } from 'zod/v4'

export const AuthContext = createContext<LoginContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Initialize auth from localStorage on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('auth_token')
    const savedUser = localStorage.getItem('auth_user')
    if (savedToken && savedUser) {
      try {
        setToken(savedToken)
        setUser(JSON.parse(savedUser))
      } catch (err) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_user')
      }
    }
    setLoading(false)
  }, [])

  const login = useCallback(async (email: string, orgCode: string) => {
    try {
      setError(null)
      const response = await apiClient.post<OTPSendResponse>('/api/auth/login', {
        email,
        org_code: orgCode,
      })
      return { otp_id: response.data.otp_id,
        user_id: response.data.user_id,
        organization_id: response.data.organization_id,
        email: response.data.email,
        otp_code: response.data.otp_code
        
       }
    } catch (err) {
      const message = getErrorMessage(err)
      setError(message)
      throw err
    }
  }, [])

  const verifyOTP = useCallback(async (otp_id: string, user_id: string, organization_id: string, email: string, otp_code: string) => {
    try {
      setError(null)
      const response = await apiClient.post<OTPVerifyResponse>('/api/auth/verify', {
        otp_id,
        user_id,
        organization_id,
        email,
        otp_code,
      })

      const newToken = response.data.token
      const newUser = response.data.user

      setToken(newToken)
      setUser(newUser)
      localStorage.setItem('auth_token', newToken)
      localStorage.setItem('auth_user', JSON.stringify(newUser))
    } catch (err) {
      const message = getErrorMessage(err)
      setError(message)
      throw err
    }
  }, [])

  const logout = useCallback(() => {
    setUser(null)
    setToken(null)
    setError(null)
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
  }, [])

  const value: LoginContextType = {
    user,
    token,
    loading,
    error,
    login,
    verifyOTP,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = React.useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
