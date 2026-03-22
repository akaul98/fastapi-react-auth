# FastAPI React Auth - Frontend

A modern Next.js boilerplate with TypeScript, shadcn/ui components, and Tailwind CSS for building authentication and CRUD operations with a FastAPI backend.

## Features

- ✅ Next.js 15+ with App Router
- ✅ TypeScript strict mode
- ✅ Tailwind CSS + shadcn/ui components
- ✅ OTP-based authentication flow
- ✅ Full CRUD operations for Users and Organizations
- ✅ React Hook Form + Zod validation
- ✅ Axios API client with auth interceptors
- ✅ Context API for state management
- ✅ Responsive design

## Getting Started

### Prerequisites

- Node.js 18+ or Bun
- npm or bun package manager

### Installation

```bash
npm install
# or
bun install
```

### Environment Variables

Create a `.env.local` file based on `.env.example`:

```bash
cp .env.example .env.local
```

Update the API URL if your backend runs on a different port:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_TIMEOUT=5000
```

### Development

```bash
npm run dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

### Production Build

```bash
npm run build
npm run start
```

## Project Structure

```
src/
├── app/                          # Next.js App Router
│   ├── (auth)/                  # Auth pages group
│   │   ├── login/page.tsx       # Login page
│   │   └── verify/page.tsx      # OTP verification
│   ├── (dashboard)/             # Protected pages group
│   │   ├── users/               # Users CRUD
│   │   ├── organizations/       # Organizations CRUD
│   │   └── page.tsx             # Dashboard home
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home (redirect logic)
│   └── globals.css
├── components/
│   ├── ui/                      # shadcn/ui components
│   ├── nav/                     # Navigation components
│   └── forms/                   # Form components
├── context/
│   └── auth-context.tsx         # Auth state management
├── hooks/
│   └── use-auth.ts              # Auth hook
├── lib/
│   ├── api.ts                   # API client
│   ├── types.ts                 # TypeScript types
│   ├── utils.ts                 # Utility functions
│   └── constants.ts             # Constants
└── styles/                      # Global styles
```

## Pages

### Authentication
- **Login** (`/login`) - Enter phone number to receive OTP
- **Verify** (`/verify`) - Verify 5-digit OTP code

### Dashboard
- **Dashboard Home** (`/dashboard`) - Overview and quick links
- **Users** (`/dashboard/users`) - List, create, edit, delete users
- **Organizations** (`/dashboard/organizations`) - List, create, edit, delete organizations

## API Integration

The app connects to a FastAPI backend with the following endpoints:

- `POST /api/otp/send` - Send OTP to phone
- `POST /api/otp/verify` - Verify OTP code
- `GET /api/users/` - List all users
- `POST /api/users/` - Create user
- `GET /api/users/{user_id}/{org_id}` - Get user details
- `PUT /api/users/{user_id}/{org_id}` - Update user
- `DELETE /api/users/{user_id}/{org_id}` - Delete user
- `GET /api/organizations/` - List all organizations
- `POST /api/organizations/` - Create organization
- `GET /api/organizations/{org_id}` - Get organization details
- `PUT /api/organizations/{org_id}` - Update organization
- `DELETE /api/organizations/{org_id}` - Delete organization

## Development

### Code Quality

- TypeScript strict mode
- ESLint ready
- Tailwind CSS
- Responsive design

### Styling

Uses Tailwind CSS with custom component library. To add more shadcn/ui components:

```bash
npx shadcn-ui@latest add [component-name]
```

### Form Validation

Forms use `react-hook-form` with `zod` for schema validation:

```typescript
const mySchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
})
```

## License

MIT
