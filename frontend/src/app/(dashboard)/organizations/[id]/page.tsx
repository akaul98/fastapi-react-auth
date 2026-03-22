'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { apiClient, getErrorMessage } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import type { Organization } from '@/lib/types'

const organizationSchema = z.object({
  org_name: z.string().min(1, 'Organization name is required'),
  org_code: z.string().min(1, 'Organization code is required'),
  org_website: z.string().url('Invalid URL').optional().or(z.literal('')),
})

type OrganizationForm = z.infer<typeof organizationSchema>

export default function EditOrganizationPage() {
  const router = useRouter()
  const params = useParams()
  const orgId = params.id as string
  const [organization, setOrganization] = useState<Organization | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isLoadingOrg, setIsLoadingOrg] = useState(true)

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<OrganizationForm>({
    resolver: zodResolver(organizationSchema),
  })

  useEffect(() => {
    fetchOrganization()
  }, [orgId])

  const fetchOrganization = async () => {
    try {
      setIsLoadingOrg(true)
      setError(null)
      const response = await apiClient.get<Organization>(`/api/organizations/${orgId}`)
      setOrganization(response.data)
      reset({
        org_name: response.data.org_name,
        org_code: response.data.org_code,
        org_website: response.data.org_website || '',
      })
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setIsLoadingOrg(false)
    }
  }

  const onSubmit = async (data: OrganizationForm) => {
    if (!organization) return

    setIsLoading(true)
    setError(null)

    try {
      await apiClient.put(`/api/organizations/${orgId}`, {
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

  if (isLoadingOrg) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-500">Loading organization...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Edit Organization</h1>
        <p className="mt-2 text-gray-600">Update organization information</p>
      </div>

      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>Organization Information</CardTitle>
          <CardDescription>
            Update the details below
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
                {isLoading ? 'Updating...' : 'Update Organization'}
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
