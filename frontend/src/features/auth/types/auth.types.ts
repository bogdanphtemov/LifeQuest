import type { SessionResponse } from '@/shared/types/api';

export interface AuthState {
  isInitialized: boolean;
  isLoading: boolean;
  initData: string | null;
  session: SessionResponse | null;
  error: string | null;
}

export interface AuthActions {
  initialize: () => void;
  setSession: (session: SessionResponse) => void;
  setError: (error: string) => void;
  reset: () => void;
}

export type AuthStore = AuthState & AuthActions;
