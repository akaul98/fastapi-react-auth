// API Responses and Request types

export interface User {
  id: string
  organization_id: string
  name: string
  email: string
  phone: string
  theme: 'light' | 'dark'
  status: boolean
  created_at: string
  updated_at: string
}

export interface Organization {
  id: string
  org_name: string
  org_code: string
  org_website?: string
  status: boolean
  created_at: string
  updated_at: string
}

export interface OTPStatusEnum {
  value: string
  label: string
}

export interface OTP {
  id: string
  user_id?: string
  organization_id?: string
  email: string
  orgCode: string
  code: string
  status: string
  expires_at: string
  verified_at?: string
  created_at: string
  updated_at: string
}

export interface OTPSendRequest {
  email: string
  orgCode: string
}

export interface OTPSendResponse {
  message: string
  otp_id: string
}

export interface OTPVerifyRequest {
  otp_id: string
  code: string
}

export interface OTPVerifyResponse {
  message: string
  token: string
  user: User
}

export interface LoginContextType {
  user: User | null
  token: string | null
  loading: boolean
  error: string | null
  login: (email: string, orgCode: string) => Promise<{ otp_id: string }>
  verifyOTP: (otp_id: string, code: string) => Promise<void>
  logout: () => void
}

export interface ApiErrorResponse {
  detail: string | { [key: string]: string[] }
}
