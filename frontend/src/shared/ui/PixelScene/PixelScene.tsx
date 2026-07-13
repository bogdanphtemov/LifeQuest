import { cn } from '@/shared/lib/cn';

interface PixelSceneProps {
  className?: string;
  showVillage?: boolean;
  showWalkers?: boolean;
  showWheat?: boolean;
}

export function PixelScene({
  className,
  showVillage = true,
  showWalkers = true,
  showWheat = true,
}: PixelSceneProps) {
  return (
    <div
      className={cn(
        'absolute inset-0 z-0 pointer-events-none pixel-art',
        className,
      )}
      aria-hidden="true"
    >
      {/* Sky */}
      <div className="absolute inset-0 bg-gradient-to-b from-sky-top via-[#7a4080] via-[32%] via-sky-mid via-[55%] via-sky-low via-[78%] to-sky-glow" />

      {/* Sun */}
      <div
        className="absolute top-[8%] right-[18%] w-16 h-16 animate-sun-pulse"
        style={{
          background: '#ffe566',
          boxShadow:
            '0 0 0 4px #f0c040, 0 0 0 8px rgba(240,192,64,0.5), 0 0 40px 12px rgba(255,220,80,0.4)',
        }}
      />

      {/* Clouds */}
      <div className="absolute top-[12%] left-[8%] w-20 h-6 animate-cloud-drift opacity-35"
        style={{
          background: 'rgba(255,200,180,0.35)',
          boxShadow: '16px -8px 0 rgba(255,200,180,0.35), 32px 0 0 rgba(255,200,180,0.35), 48px -4px 0 rgba(255,200,180,0.3), -8px 4px 0 rgba(255,200,180,0.3)',
        }}
      />
      <div className="absolute top-[20%] right-[12%] w-[60px] h-5 animate-cloud-drift-reverse opacity-30"
        style={{
          background: 'rgba(255,180,160,0.3)',
          boxShadow: '12px -6px 0 rgba(255,180,160,0.3), 24px 0 0 rgba(255,180,160,0.3), -6px 4px 0 rgba(255,180,160,0.25)',
        }}
      />

      {/* Hills */}
      <div className="absolute bottom-[28%] left-0 right-0 h-[120px]">
        <div
          className="absolute bottom-0 left-[-5%] w-[110%] h-20"
          style={{
            background: '#3d2860',
            clipPath: 'polygon(0 100%, 8% 55%, 18% 70%, 30% 40%, 42% 60%, 55% 30%, 68% 55%, 80% 35%, 92% 60%, 100% 45%, 100% 100%)',
          }}
        />
        <div
          className="absolute bottom-0 left-[-5%] w-[110%] h-[60px]"
          style={{
            background: '#357040',
            clipPath: 'polygon(0 100%, 5% 60%, 15% 75%, 25% 45%, 38% 65%, 50% 35%, 62% 55%, 75% 40%, 88% 65%, 100% 50%, 100% 100%)',
          }}
        />
      </div>

      {/* Village */}
      {showVillage && (
        <div className="absolute bottom-[30%] left-0 right-0 h-[140px]">
          {/* Windmill */}
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-20 h-[120px]">
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-9 h-20 bg-[#e8e0d0]"
              style={{ borderLeft: '4px solid #a08060', borderRight: '4px solid #fff', boxShadow: 'inset -4px 0 0 rgba(0,0,0,0.08)' }}
            >
              <div className="absolute top-5 left-[6px] w-2 h-2 bg-[#555] shadow-[0_16px_0_#555,0_32px_0_#555]" />
            </div>
            <div className="animate-blade-spin absolute -top-2 left-1/2 -translate-x-1/2 w-1 h-1 bg-[#444]"
              style={{
                boxShadow: '0 -48px 0 #6b5030, 0 52px 0 #6b5030, -22px 24px 0 0 #6b5030, 22px 24px 0 0 #6b5030',
                width: '4px', height: '48px', top: '-48px', left: 0,
              }}
            />
          </div>

          {/* House left */}
          <div className="absolute bottom-0 left-[12%] w-14 h-14">
            <div className="absolute bottom-0 w-full h-[70%] bg-wall-cream"
              style={{ borderLeft: '3px solid #a08060', borderBottom: '3px solid #a08060' }}
            />
            <div className="absolute top-0 -left-1 w-[calc(100%+8px)] h-[40%] bg-roof-red"
              style={{ clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)', borderBottom: '3px solid #5c2020' }}
            />
            <div className="absolute bottom-[30%] left-1/2 -translate-x-1/2 w-[10px] h-[10px] bg-[#ffe880] animate-window-glow"
              style={{ boxShadow: '0 0 6px 2px rgba(255,220,80,0.6)' }}
            />
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-3 h-[18px] bg-wood-dark" />
          </div>

          {/* House right */}
          <div className="absolute bottom-0 right-[10%] w-12 h-12">
            <div className="absolute bottom-0 w-full h-[70%] bg-wall-cream"
              style={{ borderLeft: '3px solid #a08060', borderBottom: '3px solid #a08060' }}
            />
            <div className="absolute top-0 -left-1 w-[calc(100%+8px)] h-[40%] bg-roof-red"
              style={{ clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)', borderBottom: '3px solid #5c2020' }}
            />
            <div className="absolute bottom-[30%] left-1/2 -translate-x-1/2 w-[10px] h-[10px] bg-[#ffe880] animate-window-glow"
              style={{ boxShadow: '0 0 6px 2px rgba(255,220,80,0.6)' }}
            />
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-3 h-[18px] bg-wood-dark" />
          </div>
        </div>
      )}

      {/* Wheat field */}
      {showWheat && (
        <div className="absolute bottom-0 left-0 right-0 h-[32%] overflow-hidden"
          style={{ background: 'linear-gradient(180deg, #4a8a30 0%, #2d6b35 15%, #8b6914 100%)' }}
        >
          <div className="absolute bottom-0 w-full h-full opacity-40"
            style={{
              backgroundImage: 'repeating-linear-gradient(90deg, transparent 0px, transparent 6px, #c9a030 6px, #c9a030 7px, transparent 7px, transparent 14px)',
            }}
          />
          <div className="absolute inset-0 animate-wheat-sway"
            style={{
              backgroundImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'16\' height=\'24\' shape-rendering=\'crispEdges\'%3E%3Crect x=\'7\' y=\'8\' width=\'2\' height=\'16\' fill=\'%23a08020\'/%3E%3Crect x=\'5\' y=\'4\' width=\'2\' height=\'4\' fill=\'%23e8c547\'/%3E%3Crect x=\'7\' y=\'2\' width=\'2\' height=\'4\' fill=\'%23f0d060\'/%3E%3Crect x=\'9\' y=\'4\' width=\'2\' height=\'4\' fill=\'%23e8c547\'/%3E%3Crect x=\'6\' y=\'0\' width=\'2\' height=\'3\' fill=\'%23f0d060\'/%3E%3Crect x=\'8\' y=\'0\' width=\'2\' height=\'3\' fill=\'%23e8c547\'/%3E%3C/svg%3E")',
              backgroundSize: '16px 24px',
            }}
          />
          <div className="absolute inset-0 opacity-85 animate-wheat-sway"
            style={{
              backgroundImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'16\' height=\'24\' shape-rendering=\'crispEdges\'%3E%3Crect x=\'7\' y=\'8\' width=\'2\' height=\'16\' fill=\'%23a08020\'/%3E%3Crect x=\'5\' y=\'4\' width=\'2\' height=\'4\' fill=\'%23e8c547\'/%3E%3Crect x=\'7\' y=\'2\' width=\'2\' height=\'4\' fill=\'%23f0d060\'/%3E%3Crect x=\'9\' y=\'4\' width=\'2\' height=\'4\' fill=\'%23e8c547\'/%3E%3Crect x=\'6\' y=\'0\' width=\'2\' height=\'3\' fill=\'%23f0d060\'/%3E%3Crect x=\'8\' y=\'0\' width=\'2\' height=\'3\' fill=\'%23e8c547\'/%3E%3C/svg%3E")',
              backgroundSize: '16px 24px',
              backgroundPosition: '8px 4px',
              animationDelay: '-1s',
              animationDirection: 'reverse',
            }}
          />

          {/* Dirt path */}
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-20 h-[35%] opacity-85"
            style={{
              background: 'linear-gradient(180deg, transparent 0%, #c4a060 20%, #8b7040 100%)',
              clipPath: 'polygon(35% 0%, 65% 0%, 80% 100%, 20% 100%)',
            }}
          >
            <div className="absolute inset-0"
              style={{ background: 'repeating-linear-gradient(0deg, transparent 0px, transparent 8px, rgba(0,0,0,0.06) 8px, rgba(0,0,0,0.06) 9px)' }}
            />
          </div>

          {/* Path edges */}
          <div className="absolute bottom-[5%] w-[30px] h-[20%] opacity-60 left-[calc(50%-70px)]"
            style={{ background: 'linear-gradient(135deg, #c9a030, transparent)' }}
          />
          <div className="absolute bottom-[5%] w-[30px] h-[20%] opacity-60 right-[calc(50%-70px)]"
            style={{ background: 'linear-gradient(225deg, #c9a030, transparent)' }}
          />
        </div>
      )}

      {/* Walkers */}
      {showWalkers && (
        <>
          <div className="animate-walk-right animate-walker-bob absolute w-2 h-3 bottom-[14%]"
            style={{
              boxShadow: '2px 0 0 0 #3a2a1a, 3px 0 0 0 #3a2a1a, 4px 0 0 0 #3a2a1a, 2px 2px 0 0 #4a6a9a, 3px 2px 0 0 #4a6a9a, 4px 2px 0 0 #4a6a9a, 2px 3px 0 0 #4a6a9a, 3px 3px 0 0 #4a6a9a, 4px 3px 0 0 #4a6a9a, 2px 4px 0 0 #2a2a3a, 4px 4px 0 0 #2a2a3a, 2px 5px 0 0 #2a2a3a, 4px 5px 0 0 #2a2a3a',
            }}
          />
          <div className="animate-walk-right animate-walker-bob absolute w-2 h-3 bottom-[16%]"
            style={{
              animationDelay: '-8s, 0s',
              animationDuration: '24s, 0.45s',
              boxShadow: '2px 0 0 0 #5a3a2a, 3px 0 0 0 #5a3a2a, 4px 0 0 0 #5a3a2a, 2px 2px 0 0 #8a5040, 3px 2px 0 0 #8a5040, 4px 2px 0 0 #8a5040, 2px 3px 0 0 #8a5040, 3px 3px 0 0 #8a5040, 4px 3px 0 0 #8a5040, 2px 4px 0 0 #3a2a2a, 4px 4px 0 0 #3a2a2a, 2px 5px 0 0 #3a2a2a, 4px 5px 0 0 #3a2a2a',
            }}
          />
          <div className="animate-walk-left animate-walker-bob absolute w-2 h-3 bottom-[12%]"
            style={{
              animationDelay: '-4s, 0s',
              animationDuration: '22s, 0.42s',
              boxShadow: '2px 0 0 0 #2a4a2a, 3px 0 0 0 #2a4a2a, 4px 0 0 0 #2a4a2a, 2px 2px 0 0 #6a8a50, 3px 2px 0 0 #6a8a50, 4px 2px 0 0 #6a8a50, 2px 3px 0 0 #6a8a50, 3px 3px 0 0 #6a8a50, 4px 3px 0 0 #6a8a50, 2px 4px 0 0 #2a2a2a, 4px 4px 0 0 #2a2a2a, 2px 5px 0 0 #2a2a2a, 4px 5px 0 0 #2a2a2a',
            }}
          />
        </>
      )}

      {/* Vignette overlay */}
      <div className="absolute inset-0 pointer-events-none z-[5]"
        style={{ background: 'radial-gradient(ellipse at center 40%, transparent 40%, rgba(0,0,0,0.35) 100%)' }}
      />
    </div>
  );
}
