import { fetchTelegramSession } from '@/features/auth/api/telegramSession';

export interface CharacterCheckResult {
  exists: boolean;
  hasTextures: boolean;
  user: Record<string, unknown> | null;
  error?: string;
}

/**
 * Check if the current Telegram user has a character with textures/etc.
 * This is called when the player clicks "Start" on the main menu.
 *
 * Flow:
 *   1. Get Telegram WebApp initData
 *   2. Call the session API
 *   3. Determine if the character exists AND has textures/appearance
 *
 * @returns {Promise<CharacterCheckResult>}
 */
export async function checkCharacterExistence(): Promise<CharacterCheckResult> {
  const tg =
    window.Telegram && window.Telegram.WebApp
      ? window.Telegram.WebApp
      : null;

  if (!tg || !tg.initData) {
    return {
      exists: false,
      hasTextures: false,
      user: null,
      error: 'Open this app from the Telegram bot to see your character.',
    };
  }

  tg.ready();
  tg.expand();

  try {
    const response = await fetchTelegramSession(tg.initData);

    if (response.registered && response.user) {
      const user = response.user as Record<string, unknown>;

      // Check if character has textures / appearance info
      const textureKeys = ['textures', 'appearance', 'texture', 'texture_path', 'sprite_data'] as const;
      const hasTextures = textureKeys.some((key) => {
        const value = user[key];
        return value !== null && value !== undefined && value !== '';
      });

      return {
        exists: true,
        hasTextures,
        user,
      };
    }

    return {
      exists: false,
      hasTextures: false,
      user: null,
      error:
        'You do not have a character yet. ' +
        'Open the Telegram bot and use /start to create one!',
    };
  } catch (error) {
    console.error('Character check error:', error);
    return {
      exists: false,
      hasTextures: false,
      user: null,
      error:
        'Could not verify your Telegram session. ' +
        'Please open the bot with /start first.',
    };
  }
}
