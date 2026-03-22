'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useAuth } from '@/context/auth-context'

const verifySchema = z.object({
  code: z.string().length(5, 'OTP must be 5 digits').regex(/^\d+$/, 'OTP must contain only numbers'),
})

type VerifyForm = z.infer<typeof verifySchema>

export default function VerifyPage() {
  const router = useRouter()
  const { verifyOTP } = useAuth()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [otp_id, setOtpId] = useState<string | null>(null)

  useEffect(() => {
    const storedOtpId = sessionStorage.getItem('pending_otp_id')
    const storedUserId = sessionStorage.getItem('pending_user_id')
    const storedOrganizationId = sessionStorage.getItem('pending_organization_id')
    const storedEmail = sessionStorage.getItem('pending_email')
    if (!storedOtpId || !storedUserId || !storedOrganizationId || !storedEmail) {
      router.push('/login')
      return
    }
    setOtpId(storedOtpId)
  }, [router])

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<VerifyForm>({
    resolver: zodResolver(verifySchema),
  })

  const onSubmit = async (data: VerifyForm) => {
    if (!otp_id) return

    setIsLoading(true)
    setError(null)
    try {
      const email = sessionStorage.getItem('pending_email')
      const orgCode = sessionStorage.getItem('pending_org_code')
      const userId = sessionStorage.getItem('pending_user_id')
      const organizationId = sessionStorage.getItem('pending_organization_id')
      if (!email || !orgCode || !userId || !organizationId) {
        setError('Missing required information. Please try again.')
        return
      }
      await verifyOTP(otp_id, userId, organizationId, email, data.code)
      // Clear session storage
      sessionStorage.removeItem('pending_email')
      sessionStorage.removeItem('pending_org_code')
      sessionStorage.removeItem('pending_user_id')
      sessionStorage.removeItem('pending_organization_id')
      sessionStorage.removeItem('pending_otp_id')
      router.push('/dashboard')
    } catch (err) {
      setError('Invalid OTP. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  if (!otp_id) {
    return (
      <Card>
        <CardContent className="pt-6">
          <p className="text-center text-gray-500">Loading...</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Verify OTP</CardTitle>
        <CardDescription>
          Enter the 5-digit code we sent to your phone
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="code">OTP Code</Label>
            <Input
              id="code"
              placeholder="00000"
              type="text"
              inputMode="numeric"
              maxLength={5}
              {...register('code')}
              className="text-center text-2xl font-mono tracking-widest"
            />
            {errors.code && (
              <p className="text-sm text-red-600">{errors.code.message}</p>
            )}
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? 'Verifying...' : 'Verify OTP'}
          </Button>
        </form>

        <div className="text-center text-sm text-gray-600">
          <p>Didn't receive the code?</p>
          <Button
            variant="link"
            onClick={() => router.push('/login')}
            className="p-0 h-auto"
          >
            Try another phone number
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
