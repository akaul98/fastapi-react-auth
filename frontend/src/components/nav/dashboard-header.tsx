'use client'

import { useRouter } from 'next/navigation'
import { useAuth } from '@/context/auth-context'
import { Button } from '@/components/ui/button'

export function DashboardHeader() {
  const router = useRouter()
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <header className="bg-white border-b border-gray-200 px-8 py-4 flex justify-between items-center">
      <div className="flex-1">
        <h2 className="text-lg font-semibold text-gray-900">
          Welcome, {user?.name || 'User'}
        </h2>
        <p className="text-sm text-gray-500">{user?.email || user?.phone}</p>
      </div>
      <Button
        variant="outline"
        onClick={handleLogout}
      >
        Logout
      </Button>
    </header>
  )
}
