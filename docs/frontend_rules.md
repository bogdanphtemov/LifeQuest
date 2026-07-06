# Frontend Development Rules

> This document is intended for automatic use by AI models when generating code.  
> Adherence to these rules is mandatory for all frontend parts of the project.

---

## 1. Architecture

### 1.1. General Architecture
- Use a **monorepository** (unless otherwise specified).
- Frontend is built with **React + TypeScript + Vite**.
- Styling — **Tailwind CSS**.
- State management — **Zustand** (or React Context for local state).
- Server state — **TanStack React Query**.
- Routing — **React Router v6**.
- Internationalization — **i18next** (if needed).

### 1.2. Architecture Principles
- **Feature-based** structure: each module/feature is isolated.
- **Component decomposition**: one component — one responsibility.
- **Unidirectional data flow**: data flows from top to bottom (from page/container to presentational components).
- **Business logic** is separated from UI.

---

## 2. Folder Structure

### 2.1. Overall Project Structure

```
src/
├── app/                    # Application-wide configuration
│   ├── App.tsx
│   ├── providers.tsx       # Providers (QueryClient, Theme, etc.)
│   ├── router.tsx          # Global router
│   └── i18n.ts             # i18next configuration
│
├── pages/                  # Route-level page components
│   ├── Home/
│   │   ├── index.tsx
│   │   └── Home.tsx
│   ├── About/
│   └── ...
│
├── features/               # Feature modules
│   ├── auth/
│   │   ├── components/     # Feature-specific components
│   │   ├── hooks/          # Feature-specific hooks
│   │   ├── api/            # Feature-specific API calls
│   │   ├── types/          # Feature-specific types
│   │   ├── utils/          # Feature-specific utilities
│   │   └── index.ts        # Public API (barrel export)
│   ├── users/
│   └── ...
│
├── shared/                 # Shared resources
│   ├── ui/                 # UI components (Button, Input, Modal, etc.)
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   └── ...
│   ├── lib/                # Helper libraries
│   ├── hooks/              # Global hooks
│   ├── utils/              # Global utilities
│   └── types/              # Global types
│
├── styles/                 # Global styles
│   └── globals.css
│
├── assets/                 # Static files (images, fonts, etc.)
│
└── main.tsx                # Entry point
```

### 2.2. Module Internal Structure

```
feature-name/
├── components/          # Components belonging to this module
│   ├── FeatureList.tsx
│   └── FeatureItem.tsx
├── hooks/               # Module-specific hooks
│   └── useFeatureData.ts
├── api/                 # API request functions
│   └── getFeature.ts
├── types/               # Module-specific types
│   └── feature.ts
├── utils/               # Module helper functions
│   └── formatFeature.ts
└── index.ts             # Barrel export
```

### 2.3. Structure Rules
- The `features/` folder contains **all business logic**.
- The `shared/` folder contains **reusable UI components and utilities**.
- The `pages/` folder only **composes** features into routes; it contains no business logic.
- Maximum nesting depth: **4 levels**.

---

## 3. File Naming Rules

| Type | Format | Example |
|---|---|---|
| Components | `PascalCase` | `UserProfile.tsx` |
| Hooks | `use{Name}.ts` (camelCase) | `useUserData.ts` |
| API functions | `{verb}{Name}.ts` (camelCase) | `getUser.ts`, `createPost.ts` |
| Utilities | `{name}.ts` (camelCase) | `formatDate.ts` |
| Types | `{name}.ts` (camelCase) | `user.types.ts` or `types.ts` |
| Styles | `{name}.css` | `globals.css` |
| Tests | `{FileName}.test.tsx` | `Button.test.tsx` |
| Index files | `index.ts` | `index.ts` |
| Pages | `PascalCase.tsx` | `HomePage.tsx` |

### Rules:
- Use **only Latin characters** in file names.
- No special characters (except `.` and `-`).
- TypeScript files have `.ts` or `.tsx` extensions (`.tsx` if JSX is present).
- Files in `types/` folders are named after the module, e.g., `user.types.ts`.

---

## 4. Component Naming Rules

### 4.1. Component Names
- Always **PascalCase**.
- The component name **must match the file name**.
- Prefixes for specific types:
  - `Page` — for pages: `HomePage`, `ProfilePage`
  - `Form` — for forms: `LoginForm`, `UserForm`
  - `List` / `Item` — for lists: `UserList`, `UserItem`
  - `Modal` / `Drawer` / `Dialog` — for modal windows
  - `Provider` — for context providers
  - `Layout` — for layout components
- **No abbreviations**: `UsersList` instead of `UsrsLst`.

### 4.2. Props Naming
- **camelCase**.
- Boolean props: no `is` prefix for states, but use `is` for conditional props: `isLoading`, `isDisabled`, `isActive`.
- Callbacks: `on{Event}` — `onClick`, `onChange`, `onSubmit`.
- Handler props: `handle{Action}` — `handleSubmit`, `handleDelete`.

### 4.3. Export
- Always use **named export** (not default export) for components.
- Barrel export via `index.ts` in the component's folder.

```tsx
// ✅ Correct
export function Button({ children, onClick }: ButtonProps) { ... }

// ❌ Incorrect
export default function Button() { ... }
```

---

## 5. React Usage Rules

### 5.1. General Principles
- Always use functional components (class components are forbidden).
- Declarative approach: describe **what** to show, not **how**.
- Components should be pure functions (no side effects in render).

### 5.2. Hooks
- Custom hooks — for **extracting logic** from components.
- Custom hook names must start with `use`.
- Hooks must be used **at the top level** of the component (not inside loops/conditions).
- Combine hooks through composition, not through wrapper custom hooks.

```tsx
// ✅ Correct
function UserProfile({ userId }: UserProfileProps) {
  const { data, isLoading } = useUser(userId);
  const { t } = useTranslation();

  if (isLoading) return <Spinner />;

  return <div>{t('greeting', { name: data.name })}</div>;
}

// ❌ Incorrect — hook inside a condition
if (userId) {
  const { data } = useUser(userId); // BAD
}
```

### 5.3. useMemo and useCallback
- Use **only when actually needed** (after profiling).
- `useMemo` — for expensive computations.
- `useCallback` — for stable callbacks passed to child components.

```tsx
// ✅ Expensive computation
const sortedUsers = useMemo(
  () => [...users].sort((a, b) => a.name.localeCompare(b.name)),
  [users]
);

// ✅ Stable callback for child component
const handleDelete = useCallback(
  (id: string) => deleteUser(id),
  [deleteUser]
);
```

### 5.4. Conditional Rendering
- Use `&&`, ternary operator, or early `return`.
- **Do not use** `&&` with numbers (except when guaranteed boolean).

```tsx
// ✅ Correct
{isVisible && <Modal />}
{items.length > 0 ? <List /> : <Empty />}
{isLoading && <Spinner />}

// ❌ Dangerous when items.length = 0
{items.length && <List />}
```

---

## 6. TypeScript Usage Rules

### 6.1. Typing
- **strict mode** is enabled.
- `any` is forbidden. Use `unknown` when the type is unknown.
- **Explicit typing** for props and functions; return types are inferred.
- Use interfaces for objects, types for union/intersection.

```tsx
// ✅ Correct
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  isDisabled?: boolean;
}

// ❌ Incorrect — any
function processData(data: any) { ... }
```

### 6.2. Generics
- Use for reusable types.

```tsx
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

function useFetch<T>(url: string): { data: T | null; isLoading: boolean } {
  // ...
}
```

### 6.3. Enums
- Use `as const` objects + union type instead of `enum`.

```tsx
// ✅ Correct
export const Theme = {
  LIGHT: 'light',
  DARK: 'dark',
} as const;
export type ThemeType = (typeof Theme)[keyof typeof Theme];

// ❌ Old approach
enum Theme { LIGHT, DARK }
```

### 6.4. Utility Types
- Use `Pick`, `Omit`, `Partial`, `Required`, `Readonly` for derived types.

```tsx
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

type UserUpdatePayload = Partial<Pick<User, 'name' | 'email'>>;
type UserPublic = Omit<User, 'email'>;
```

---

## 7. Tailwind Usage Rules

### 7.1. Styling
- All styles — through Tailwind utility classes.
- **Forbidden**: CSS modules, styled-components, inline styles.
- Use `cn()` (clsx + tailwind-merge) for dynamic classes.

```tsx
// ✅ Correct
import { cn } from '@/shared/lib/cn';

function Button({ variant = 'primary', className }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-lg px-4 py-2 font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        {
          'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
          'bg-gray-100 text-gray-700 hover:bg-gray-200': variant === 'secondary',
        },
        className
      )}
    >
      {children}
    </button>
  );
}
```

### 7.2. Custom Styles
- Custom colors/fonts — only through `tailwind.config.ts`.
- **Forbidden** to use `@apply` unless for global base classes.
- Use `@layer base` only for CSS reset.

### 7.3. Responsive Design
- Mobile-first approach: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`.
- Minimum supported width: 320px.

```tsx
// Mobile-first: base styles for mobile, then larger screens
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4 md:p-6 lg:p-8">
```

### 7.4. Animations
- Use built-in Tailwind: `transition-{property}`, `duration-{time}`, `animate-{name}`.
- Custom animations — in `tailwind.config.ts` via `extend.animation`.

---

## 8. Optimization Rules

### 8.1. Performance
- **Code splitting**: React.lazy + Suspense for pages.
- **Image optimization**: lazy loading for `<img>` tags.
- **Virtualization**: for large lists, use `react-window` or `@tanstack/virtual`.

```tsx
// ✅ Code splitting for pages
const HomePage = React.lazy(() => import('@/pages/Home/HomePage'));
const AboutPage = React.lazy(() => import('@/pages/About/AboutPage'));
```

### 8.2. Memoization
- `React.memo` — for components that re-render often with the same props.
- `useMemo`/`useCallback` — only when proven necessary.

```tsx
// ✅ Only if the component re-renders often with the same props
const UserCard = React.memo(function UserCard({ user }: UserCardProps) {
  return <div>{user.name}</div>;
});
```

### 8.3. Data Loading
- **Prefetching** data that will be needed soon.
- **Pagination** / **Infinite scroll** for large lists.
- **Request deduplication** (built into TanStack Query).

### 8.4. Bundle
- **Tree shaking** — import only what is needed.
- **Dynamic imports** for heavy libraries.
- Minimize bundle size: analyze with `vite-bundle-visualizer`.

---

## 9. Component Reusability Rules

### 9.1. Component Levels
- **Atomic design** (atoms → molecules → organisms), but not dogmatic.
- **shared/ui** — base components (Button, Input, Modal, Select, etc.).
- **features/*/components** — feature-specific components.

### 9.2. Composition
- Compose components through **children** and **render props**.
- Avoid wrapper components that add only one level of div.

```tsx
// ✅ Composition via children
function Card({ title, children }: CardProps) {
  return (
    <div className="rounded-xl border p-4 shadow-sm">
      <h2 className="text-lg font-semibold">{title}</h2>
      <div className="mt-2">{children}</div>
    </div>
  );
}

// ✅ Specialization via composition
function UserCard({ user }: UserCardProps) {
  return (
    <Card title={user.name}>
      <p>{user.email}</p>
    </Card>
  );
}
```

### 9.3. Props
- Always type props via a separate interface.
- Props interface name: `{ComponentName}Props`.
- Default values — via destructuring.

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  isDisabled?: boolean;
  children: React.ReactNode;
}

function Button({ variant = 'primary', isDisabled = false, children }: ButtonProps) {
  // ...
}
```

---

## 10. Code Formatting Rules

### 10.1. Code Style
- **Prettier** for formatting (config in `.prettierrc`).
- **ESLint** with rules:
  - `@typescript-eslint`
  - `eslint-plugin-react` (react/jsx-key, react/no-array-index-key)
  - `eslint-plugin-react-hooks`
  - `eslint-plugin-tailwindcss` (classnames order)
- Maximum line length: **100 characters**.
- Indentation: **2 spaces**.

### 10.2. Imports
- Import order (groups separated by a blank line):
  1. External libraries (`react`, `react-dom`, `@tanstack/react-query`)
  2. Internal modules (`@/app`, `@/pages`, `@/features`, `@/shared`)
  3. Relative imports (`./`, `../`)
  4. Styles (`*.css`)

```tsx
import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';

import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui/Button';
import { useAuth } from '@/features/auth/hooks/useAuth';

import { UserCard } from './UserCard';
import type { User } from '../types/user.types';
```

### 10.3. JSX Formatting
- Attributes: one per line if more than 3.
- Double quotes for JSX attributes.
- Self-closing tags if no children.

```tsx
// ✅ Many attributes — each on its own line
<Button
  variant="primary"
  size="md"
  isDisabled={isSubmitting}
  onClick={handleSubmit}
  className="mt-4"
>
  {t('submit')}
</Button>

// ✅ Few attributes — single line
<Input type="email" value={email} onChange={handleChange} />
```

### 10.4. Comments
- Comments — only for complex business rules.
- **Do not comment** obvious code.
- **Do not leave** commented-out code (remove immediately).
- JSDoc — for public API functions.

---

## 11. State Management Rules

### 11.1. Types of State
- **Server state** (data from API) → TanStack React Query.
- **Client state** (UI state, forms) → Zustand or React Context.
- **URL state** (params, filters) — React Router (useSearchParams).

### 11.2. TanStack React Query (Server State)

```tsx
// ✅ Fetching data
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser(userId),
    enabled: !!userId,
    staleTime: 5 * 60 * 1000, // 5 min
    retry: 2,
  });
}

// ✅ Mutating data
export function useUpdateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: updateUser,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.setQueryData(['users', data.id], data);
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });
}
```

### 11.3. Zustand (Client State)

```tsx
import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: false,
  theme: 'light',
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setTheme: (theme) => set({ theme }),
}));
```

### 11.4. Local State
- `useState` for simple values.
- `useReducer` for complex state logic.
- Forms: **React Hook Form** + **Zod** for validation.

```tsx
// ✅ Form with React Hook Form + Zod
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});

type LoginFormData = z.infer<typeof loginSchema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const mutation = useLogin();

  return (
    <form onSubmit={handleSubmit((data) => mutation.mutate(data))}>
      {/* ... */}
    </form>
  );
}
```

### 11.5. State Rules
- State is the single source of truth.
- **Do not duplicate** data between server and client state.
- **Minimize global state**: anything that can be stored locally — store locally.
- **Do not copy** TanStack Query cache data into Zustand.
- Use `reset()` to clear state.

---

## 12. API Interaction Rules

### 12.1. General Principles
- All API calls go through functions in `features/*/api/`.
- Single HTTP client (axios/fetch) + interceptors for tokens.
- Base URL — through environment variables `VITE_API_URL`.

### 12.2. API Function Structure

```tsx
// ✅ features/users/api/getUsers.ts
import { apiClient } from '@/shared/lib/apiClient';
import type { User } from '../types/user';

interface GetUsersParams {
  page?: number;
  limit?: number;
  search?: string;
}

export async function getUsers(params: GetUsersParams = {}): Promise<{
  users: User[];
  total: number;
}> {
  const { data } = await apiClient.get('/users', { params });
  return data;
}

// ✅ features/users/api/createUser.ts
export async function createUser(body: CreateUserPayload): Promise<User> {
  const { data } = await apiClient.post('/users', body);
  return data;
}
```

### 12.3. API Client

```tsx
// ✅ shared/lib/apiClient.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// Interceptor for adding token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Refresh token or redirect to login
    }
    return Promise.reject(error);
  }
);
```

### 12.4. Error Handling
- API functions **do not handle errors** — they propagate them upward.
- Errors are handled in TanStack Query mutations or in components.
- Show understandable messages to the user (i18n).

```tsx
// ✅ Error handling at the component level
function CreateUserForm() {
  const mutation = useCreateUser();
  
  return (
    <form onSubmit={handleSubmit((data) => mutation.mutate(data))}>
      {mutation.isError && (
        <Alert variant="error">
          {mutation.error?.message || t('errors.somethingWentWrong')}
        </Alert>
      )}
      {/* ... */}
    </form>
  );
}
```

### 12.5. API Typing
- All API responses must have corresponding TypeScript interfaces.
- Shared types (pagination, errors) — in `shared/types/api.ts`.

```tsx
// ✅ shared/types/api.ts
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

export interface ApiError {
  message: string;
  code: string;
  status: number;
}
```

---

## 13. Additional Rules

### 13.1. Accessibility (a11y)
- All form elements must have `<label>`.
- Interactive elements must have `aria-label` or `aria-labelledby`.
- Keyboard navigation: `tabIndex`, `onKeyDown`.
- Colors must have sufficient contrast (WCAG AA).

### 13.2. Testing
- **Vitest** + **React Testing Library**.
- Test behavior, not implementation.
- Components: userEvent + screen.
- Hooks: renderHook.
- API functions: msw.

### 13.3. Import Aliases
```ts
// vite.config.ts
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

### 13.4. Environment Variables
```env
VITE_API_URL=http://localhost:3000/api
VITE_APP_TITLE=My App
```
- All environment variables must have the `VITE_` prefix.
- Validate environment variables at application startup.

---

> **Important**: The AI model must strictly follow these rules when generating code.  
> Every generated file must conform to the folder structure, naming conventions, and architectural principles described above.
