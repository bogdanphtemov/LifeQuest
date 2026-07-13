import { PixelScene } from '@/shared/ui/PixelScene';
import { WoodSign } from '@/shared/ui/WoodSign';
import { useCharacter } from '../hooks/useCharacter';

export function CharacterDashboard() {
  const { character } = useCharacter();

  if (!character) {
    return null;
  }

  return (
    <div className="screen-container flex items-center justify-center px-4 py-6 pixel-art"
      style={{ background: '#5b3a8c', overflow: 'hidden' }}
    >
      <PixelScene showWheat={false} showVillage={false} showWalkers={false} />
      <WoodSign>
        <div className="px-1 py-1">
          {/* Header */}
          <div className="text-center border-b-4 border-dashed border-wood-edge pb-4 mb-5"
            style={{ borderBottom: '3px dashed #4a2e18' }}
          >
            <h1 className="game-title font-pixel text-[clamp(14px,3.5vw,20px)] text-wood-edge"
              style={{ textShadow: '2px 2px 0 rgba(0,0,0,0.15)', letterSpacing: '2px', lineHeight: '1.6' }}
            >
              ⚔️ LIFE QUEST
            </h1>
            <p className="font-pixel text-[clamp(8px,2vw,10px)] text-[#6b4423] mt-2 leading-relaxed">
              Your Character Dashboard
            </p>
          </div>

          {/* Character Card */}
          <div className="bg-primary/50 border border-border rounded p-3.5 mb-4">
            <StatRow label="Name" value={character.displayName ?? '—'} />
            <StatRow label="Login" value={character.username ?? '—'} />
            <StatRow label="Class" value={character.characterClass ?? 'adventurer'} />
            <StatRow label="Avatar" value={character.avatar ?? 'pixel_adventurer'} />
            <StatRow label="Level" value={character.level?.toString() ?? '—'} />
            <StatRow label="Experience" value={character.experience?.toString() ?? '—'} />
            <StatRow label="Coins" value={character.coins?.toString() ?? '—'} />
          </div>

          <p className="text-center text-text-secondary text-xs italic mt-2.5 pt-2.5 border-t border-border">
            ⚡ Data is pulled from your Telegram character.
            Use the bot to manage your adventure.
          </p>
        </div>
      </WoodSign>
    </div>
  );
}

interface StatRowProps {
  label: string;
  value: string;
}

function StatRow({ label, value }: StatRowProps) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-border/30 last:border-b-0">
      <span className="text-sm uppercase tracking-wider text-text-secondary">
        {label}
      </span>
      <span className="text-base font-bold text-accent-gold font-mono">
        {value}
      </span>
    </div>
  );
}
