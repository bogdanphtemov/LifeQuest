import { useAuth } from '@/features/auth';
import { useCharacter } from '@/features/character';
import { LoadingScreen } from '@/shared/ui/LoadingScreen';
import { NotRegistered } from '@/features/character/components/NotRegistered';

/**
 * Game Dashboard — displayed when the player already has a character.
 *
 * Acts as the main game hub after the player enters the world.
 * Shows character stats at the top and placeholder areas for future
 * game features (adventure log, inventory, quests, etc.).
 */
export function GameDashboardPage() {
  const { isNoTelegramContext, isLoading, isError, error } = useAuth();
  const { character, isRegistered } = useCharacter();

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

  if (!isRegistered || !character) {
    return <NotRegistered />;
  }

  return (
    <div
      className="screen-container pixel-art flex flex-col overflow-y-auto"
      style={{ background: '#0d1b0e' }}
    >
      {/* ── Header ── */}
      <div className="w-full px-4 py-3 text-center border-b border-[#2a4a2a] bg-[#0f200f]">
        <h1 className="font-pixel text-[12px] text-[#b8d8b8] tracking-wider">
          ⚔ LIFEQUEST ⚔
        </h1>
        <p className="font-pixel text-[7px] text-[#6a8a6a] mt-1">
          The adventure awaits...
        </p>
      </div>

      {/* ── Character Portrait & Stats ── */}
      <div className="mx-4 mt-3 p-3 rounded border border-[#2a4a2a] bg-[#0f200f]">
        <div className="flex items-center gap-3">
          {/* Avatar */}
          <div className="w-16 h-16 rounded-full border-2 border-[#4a6a4a] bg-[#1a3a1a] flex items-center justify-center shrink-0">
            <span className="font-pixel text-[28px]">
              {character.characterClass === 'mage' ? '🧙' :
               character.characterClass === 'warrior' ? '⚔️' :
               character.characterClass === 'archer' ? '🏹' :
               character.characterClass === 'rogue' ? '🗡️' : '🧭'}
            </span>
          </div>

          {/* Stats */}
          <div className="flex-1 min-w-0">
            <p className="font-pixel text-[11px] text-[#b8d8b8] truncate">
              {character.displayName || character.username}
            </p>
            <p className="font-pixel text-[8px] text-[#8aaa6a]">
              Level {character.level} {character.characterClass?.toUpperCase()}
            </p>
            <div className="flex gap-3 mt-1">
              <span className="font-pixel text-[7px] text-[#6a8a6a]">
                XP: {character.experience ?? 0}
              </span>
              <span className="font-pixel text-[7px] text-[#d4af37]">
                🪙 {character.coins ?? 0}
              </span>
            </div>

            {/* XP Bar */}
            <div className="mt-1 w-full h-2 bg-[#1a3a1a] rounded-full overflow-hidden border border-[#2a4a2a]">
              <div
                className="h-full bg-[#4aaa4a] transition-all duration-500"
                style={{ width: `${Math.min((character.experience ?? 0) % 100, 100)}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* ── Game Hub Placeholder Cards ── */}
      <div className="mx-4 mt-3 grid grid-cols-2 gap-2">
        {/* Adventure */}
        <div className="p-3 rounded border border-[#2a4a2a] bg-[#0f200f] text-center">
          <span className="font-pixel text-[20px]">🗺️</span>
          <p className="font-pixel text-[8px] text-[#b8d8b8] mt-1">ADVENTURE</p>
          <p className="font-pixel text-[6px] text-[#6a8a6a] mt-1">Coming soon</p>
        </div>

        {/* Inventory */}
        <div className="p-3 rounded border border-[#2a4a2a] bg-[#0f200f] text-center">
          <span className="font-pixel text-[20px]">🎒</span>
          <p className="font-pixel text-[8px] text-[#b8d8b8] mt-1">INVENTORY</p>
          <p className="font-pixel text-[6px] text-[#6a8a6a] mt-1">Coming soon</p>
        </div>

        {/* Quests */}
        <div className="p-3 rounded border border-[#2a4a2a] bg-[#0f200f] text-center">
          <span className="font-pixel text-[20px]">📜</span>
          <p className="font-pixel text-[8px] text-[#b8d8b8] mt-1">QUESTS</p>
          <p className="font-pixel text-[6px] text-[#6a8a6a] mt-1">Coming soon</p>
        </div>

        {/* Tavern */}
        <div className="p-3 rounded border border-[#2a4a2a] bg-[#0f200f] text-center">
          <span className="font-pixel text-[20px]">🍺</span>
          <p className="font-pixel text-[8px] text-[#b8d8b8] mt-1">TAVERN</p>
          <p className="font-pixel text-[6px] text-[#6a8a6a] mt-1">Coming soon</p>
        </div>
      </div>

      {/* ── Daily Rewards ── */}
      <div className="mx-4 mt-3 p-3 rounded border border-[#2a4a2a] bg-[#0f200f] text-center">
        <p className="font-pixel text-[9px] text-[#d4af37]">🎁 DAILY REWARDS</p>
        <p className="font-pixel text-[7px] text-[#6a8a6a] mt-1">
          Check back tomorrow for your daily bonus!
        </p>
      </div>

      {/* ── Footer ── */}
      <div className="w-full px-4 py-4 text-center mt-3 border-t border-[#2a4a2a]">
        <p className="font-pixel text-[6px] text-[#4a6a4a]">
          LifeQuest v0.1.0 — More features coming soon!
        </p>
      </div>

      <div className="h-6" />
    </div>
  );
}
