import { useAuth } from '@/features/auth';
import { NotRegistered } from '@/features/character/components/NotRegistered';

/**
 * Character Creation screen — shown when a player has no character yet.
 * Prompts them to create one via the Telegram bot.
 */
export function CharacterCreationPage() {
  const { isNoTelegramContext, isLoading } = useAuth();

  const message = isNoTelegramContext
    ? 'Open this app from the Telegram bot to create your character.'
    : "You don't have a character yet. Open the Telegram bot and use /start to create one!";

  if (isLoading) {
    return (
      <div className="screen-container pixel-art flex items-center justify-center"
        style={{ background: '#5b3a8c' }}
      >
        <p className="font-pixel text-[10px] text-[#e8d8b8] animate-pulse">
          Loading...
        </p>
      </div>
    );
  }

  return <NotRegistered message={message} />;
}
