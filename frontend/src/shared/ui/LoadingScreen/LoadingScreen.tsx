import { PixelScene } from '@/shared/ui/PixelScene';
import { WoodSign } from '@/shared/ui/WoodSign';

interface LoadingScreenProps {
  message?: string;
}

export function LoadingScreen({ message = 'Connecting to the realm...' }: LoadingScreenProps) {
  return (
    <div className="screen-container flex items-center justify-center pixel-art"
      style={{ background: '#5b3a8c', overflow: 'hidden' }}
    >
      <PixelScene showWheat showVillage showWalkers />
      <WoodSign>
        <div className="text-center px-5 py-2">
          <h1 className="game-title font-pixel text-[clamp(14px,3.5vw,20px)] text-wood-edge"
            style={{ textShadow: '2px 2px 0 rgba(0,0,0,0.15)', letterSpacing: '2px', lineHeight: '1.6' }}
          >
            LIFE QUEST
          </h1>
          <p className="text-text-primary text-base italic mt-5 animate-pulse-text">
            {message}
          </p>
        </div>
      </WoodSign>
    </div>
  );
}
