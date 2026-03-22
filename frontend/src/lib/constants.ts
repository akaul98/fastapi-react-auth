export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const API_ENDPOINTS = {
  OTP: {
    SEND: '/api/otp/send',
    VERIFY: '/api/otp/verify',
  },
  USERS: {
    LIST: '/api/users/',
    CREATE: '/api/users/',
    GET: (userId: string, orgId: string) => `/api/users/${userId}/${orgId}`,
    UPDATE: (userId: string, orgId: string) => `/api/users/${userId}/${orgId}`,
    DELETE: (userId: string, orgId: string) => `/api/users/${userId}/${orgId}`,
  },
  ORGANIZATIONS: {
    LIST: '/api/organizations/',
    CREATE: '/api/organizations/',
    GET: (orgId: string) => `/api/organizations/${orgId}`,
    UPDATE: (orgId: string) => `/api/organizations/${orgId}`,
    DELETE: (orgId: string) => `/api/organizations/${orgId}`,
  },
}

export const THEME = {
  LIGHT: 'light',
  DARK: 'dark',
} as const

export const OTP_CODE_LENGTH = 5
