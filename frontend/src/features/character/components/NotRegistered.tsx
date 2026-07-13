import { PixelScene } from '@/shared/ui/PixelScene';
import { WoodSign } from '@/shared/ui/WoodSign';

interface NotRegisteredProps {
  message?: string;
}

export function NotRegistered({
  message = 'You don\'t have a character yet. Open the Telegram bot and use /start to create one!',
}: NotRegisteredProps) {
  return (
    <div className="screen-container flex items-center justify-center px-4 py-6 pixel-art"
      style={{ background: '#5b3a8c', overflow: 'hidden' }}
    >
      <PixelScene showWheat={false} showVillage={false} showWalkers={false} />
      <WoodSign>
        <div className="text-center px-1 py-1">
          <h1 className="game-title font-pixel text-[clamp(14px,3.5vw,20px)] text-wood-edge mb-5"
            style={{ textShadow: '2px 2px 0 rgba(0,0,0,0.15)', letterSpacing: '2px', lineHeight: '1.6' }}
          >
            NO CHARACTER
          </h1>
          <p className="text-text-primary text-base leading-relaxed mb-2.5">
            {message}
          </p>
          <p className="text-text-secondary text-xs italic">
            After registration, come back here to see your stats.
          </p>
        </div>
      </WoodSign>
    </div>
  );
}
