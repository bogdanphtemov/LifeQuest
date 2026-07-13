import { apiClient } from '@/shared/lib/apiClient';
import type { SessionResponse } from '@/shared/types/api';

export async function fetchTelegramSession(initData: string): Promise<SessionResponse> {
  return apiClient.telegramSession(initData);
}
