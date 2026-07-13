import { create } from 'zustand';
import type { AuthStore } from '../types/auth.types';
import type { SessionResponse } from '@/shared/types/api';

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        initData: string;
        ready: () => void;
        expand: () => void;
      };
    };
  }
}

export const useAuthStore = create<AuthStore>((set) => ({
  isInitialized: false,
  isLoading: true,
  initData: null,
  session: null,
  error: null,

  initialize: () => {
    const tg = window.Telegram?.WebApp;
    const initData = tg?.initData ?? null;

    if (tg && initData) {
      tg.ready();
      tg.expand();
    }

    set({ initData, isLoading: false, isInitialized: true });
  },

  setSession: (session: SessionResponse) => {
    set({ session, error: null });
  },

  setError: (error: string) => {
    set({ error, session: null });
  },

  reset: () => {
    set({
      isInitialized: false,
      isLoading: true,
      initData: null,
      session: null,
      error: null,
    });
  },
}));
