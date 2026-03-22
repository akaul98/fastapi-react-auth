'use client'

import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/context/auth-context'

export default function DashboardPage() {
  const { user } = useAuth()

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Welcome to your dashboard, {user?.name}!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Manage Users</CardTitle>
            <CardDescription>
              View, create, edit, or delete users
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Link href="/dashboard/users">
              <Button variant="default">Go to Users</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Manage Organizations</CardTitle>
            <CardDescription>
              View, create, edit, or delete organizations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Link href="/dashboard/organizations">
              <Button variant="default">Go to Organizations</Button>
            </Link>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Your Profile</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <p className="text-sm text-gray-600">Name</p>
            <p className="font-medium text-gray-900">{user?.name}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Email</p>
            <p className="font-medium text-gray-900">{user?.email || 'N/A'}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Phone</p>
            <p className="font-medium text-gray-900">{user?.phone}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Theme</p>
            <p className="font-medium text-gray-900 capitalize">{user?.theme}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
