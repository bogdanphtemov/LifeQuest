import { StartScreen } from '@/shared/ui/StartScreen';

/**
 * Entry point of the app — shows the animated pixel start screen.
 * When the user clicks "Start", the StartScreen component will
 * check character existence and redirect accordingly:
 *   - character exists → /game-dashboard
 *   - no character    → /character-creation
 */
export function StartGamePage() {
  return <StartScreen />;
}
