'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { apiClient, getErrorMessage } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'

const organizationSchema = z.object({
  org_name: z.string().min(1, 'Organization name is required'),
  org_code: z.string().min(1, 'Organization code is required'),
  org_website: z.string().url('Invalid URL').optional().or(z.literal('')),
})

type OrganizationForm = z.infer<typeof organizationSchema>

export default function NewOrganizationPage() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<OrganizationForm>({
    resolver: zodResolver(organizationSchema),
  })

  const onSubmit = async (data: OrganizationForm) => {
    setIsLoading(true)
    setError(null)

    try {
      await apiClient.post('/api/organizations/', {
        org_name: data.org_name,
        org_code: data.org_code,
        org_website: data.org_website || null,
      })
      router.push('/dashboard/organizations')
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Create Organization</h1>
        <p className="mt-2 text-gray-600">Add a new organization</p>
      </div>

      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>Organization Information</CardTitle>
          <CardDescription>
            Fill in the details below to create a new organization
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="org_name">Organization Name *</Label>
              <Input
                id="org_name"
                placeholder="Acme Corporation"
                {...register('org_name')}
              />
              {errors.org_name && (
                <p className="text-sm text-red-600">{errors.org_name.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="org_code">Organization Code *</Label>
              <Input
                id="org_code"
                placeholder="ACME"
                {...register('org_code')}
              />
              {errors.org_code && (
                <p className="text-sm text-red-600">{errors.org_code.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="org_website">Website</Label>
              <Input
                id="org_website"
                type="url"
                placeholder="https://example.com"
                {...register('org_website')}
              />
              {errors.org_website && (
                <p className="text-sm text-red-600">{errors.org_website.message}</p>
              )}
            </div>

            <div className="flex gap-4 pt-4">
              <Button type="submit" disabled={isLoading}>
                {isLoading ? 'Creating...' : 'Create Organization'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => router.back()}
              >
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
