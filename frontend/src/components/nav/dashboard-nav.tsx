'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useAuth } from '@/context/auth-context'
import { cn } from '@/lib/utils'

const navItems = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/dashboard/users', label: 'Users' },
  { href: '/dashboard/organizations', label: 'Organizations' },
]

export function DashboardNav() {
  const pathname = usePathname()

  return (
    <nav className="hidden md:flex flex-col w-64 bg-white border-r border-gray-200 p-4">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-indigo-600">MyApp</h1>
      </div>

      <ul className="space-y-2 flex-1">
        {navItems.map((item) => (
          <li key={item.href}>
            <Link
              href={item.href}
              className={cn(
                'block px-4 py-2 rounded-lg transition-colors',
                pathname === item.href
                  ? 'bg-indigo-50 text-indigo-600 font-medium'
                  : 'text-gray-700 hover:bg-gray-50'
              )}
            >
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  )
}
