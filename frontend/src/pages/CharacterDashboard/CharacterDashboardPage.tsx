import { useCharacter } from '@/features/character';
import { useAuth } from '@/features/auth';
import { LoadingScreen } from '@/shared/ui/LoadingScreen';
import { CharacterDashboard } from '@/features/character/components/CharacterDashboard';
import { NotRegistered } from '@/features/character/components/NotRegistered';

export function CharacterDashboardPage() {
  const { isNoTelegramContext, isLoading, isError, error } = useAuth();
  const { isRegistered } = useCharacter();

  // Show loading screen while initializing and resolving session
  if (isLoading) {
    return <LoadingScreen message="Verifying your identity..." />;
  }

  // No Telegram context (opened outside Telegram)
  if (isNoTelegramContext) {
    return (
      <NotRegistered
        message="Open this app from the Telegram bot to see your character."
      />
    );
  }

  // Error during session resolution
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

  // User is registered — show dashboard
  if (isRegistered) {
    return <CharacterDashboard />;
  }

  // User is not registered
  return <NotRegistered />;
}
