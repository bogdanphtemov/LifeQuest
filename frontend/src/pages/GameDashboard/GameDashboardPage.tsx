import { useAuth } from '@/features/auth';
import { useCharacter } from '@/features/character';
import { LoadingScreen } from '@/shared/ui/LoadingScreen';
import { CharacterDashboard } from '@/features/character/components/CharacterDashboard';
import { NotRegistered } from '@/features/character/components/NotRegistered';

/**
 * Game Dashboard — displayed when the player already has a character.
 * This is where the game will be launched in the future.
 * For now, it shows the Character Dashboard with stats.
 */
export function GameDashboardPage() {
  const { isNoTelegramContext, isLoading, isError, error } = useAuth();
  const { isRegistered } = useCharacter();

  if (isLoading) {
    return <LoadingScreen message="Entering the world..." />;
  }

  if (isNoTelegramContext) {
    return (
      <NotRegistered
        message="Open this app from the Telegram bot to see your character."
      />
    );
  }

  if (isError) {
    return (
      <NotRegistered
        message={
          error ??
          'Could not verify your Telegram session. Please open the bot with /start first.'
        }
      />
    );
  }

  if (isRegistered) {
    return <CharacterDashboard />;
  }

  return <NotRegistered />;
}
