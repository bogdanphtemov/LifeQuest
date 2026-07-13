export interface ApiResponse<T = unknown> {
  status: 'ok' | 'error';
  message?: string;
  data?: T;
}

export interface SessionResponse {
  status: string;
  registered: boolean;
  telegram_user?: TelegramUser;
  user?: Character;
}

export interface RegisterResponse {
  status: string;
  message: string;
  user?: Character;
}

export interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
}

export interface Character {
  display_name?: string;
  username?: string;
  character_class?: string;
  avatar?: string;
  level?: number;
  experience?: number;
  coins?: number;
  telegram_id?: number;
  texture_path?: string | null;
  sprite_data?: string | null;
}
