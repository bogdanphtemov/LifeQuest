import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from './useAuthStore';
import { fetchTelegramSession } from '../api/telegramSession';

export function useAuth() {
  const store = useAuthStore();

  useEffect(() => {
    store.initialize();
  }, []);

  const query = useQuery({
    queryKey: ['telegram-session', store.initData],
    queryFn: () => fetchTelegramSession(store.initData!),
    enabled: !!store.initData,
    retry: 2,
    staleTime: 5 * 60 * 1000,
  });

  useEffect(() => {
    if (query.data) {
      store.setSession(query.data);
    }
    if (query.error) {
      store.setError(query.error instanceof Error ? query.error.message : 'Unknown error');
    }
  }, [query.data, query.error]);

  return {
    isNoTelegramContext: !store.initData && store.isInitialized,
    isLoading: !store.isInitialized || query.isLoading,
    isError: !!query.error || !!store.error,
    error: query.error?.message ?? store.error,
    session: store.session,
    isRegistered: store.session?.registered ?? false,
    character: store.session?.user ?? null,
  };
}
