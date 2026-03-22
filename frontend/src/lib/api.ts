import axios, { AxiosInstance, AxiosError } from 'axios'
import type { ApiErrorResponse } from './types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_TIMEOUT = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '5000')

class ApiClient {
  private instance: AxiosInstance

  constructor() {
    this.instance = axios.create({
      baseURL: API_URL,
      timeout: API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add request interceptor to inject auth token
    this.instance.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Add response interceptor to handle errors
    this.instance.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiErrorResponse>) => {
        if (error.response?.status === 401) {
          // Clear token and redirect to login
          localStorage.removeItem('auth_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  async get<T>(url: string) {
    return this.instance.get<T>(url)
  }

  async post<T>(url: string, data?: any) {
    return this.instance.post<T>(url, data)
  }

  async put<T>(url: string, data?: any) {
    return this.instance.put<T>(url, data)
  }

  async delete<T>(url: string) {
    return this.instance.delete<T>(url)
  }
}

export const apiClient = new ApiClient()

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail
      if (typeof detail === 'string') {
        return detail
      }
      if (typeof detail === 'object') {
        return Object.values(detail).flat().join(', ')
      }
    }
    return error.message || 'An error occurred'
  }
  return 'An unexpected error occurred'
}
