import type { ReactNode } from 'react';
import { cn } from '@/shared/lib/cn';

interface WoodSignProps {
  children: ReactNode;
  className?: string;
}

export function WoodSign({ children, className }: WoodSignProps) {
  return (
    <div className="relative z-10 flex flex-col items-center origin-top animate-sign-sway max-w-[92vw]">
      {/* Hook */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-5 h-3 z-[11]"
        style={{ border: '4px solid #8a8a9a', borderBottom: 'none', borderRadius: '10px 10px 0 0' }}
      />

      {/* Chains */}
      <div className="flex justify-between w-full max-w-[420px] h-[52px] px-6"
        style={{ width: 'min(420px, 88vw)' }}
      >
        <div className="w-[10px] h-full -rotate-3 origin-top"
          style={{
            background: 'repeating-linear-gradient(180deg, #8a8a9a 0px, #8a8a9a 6px, #4a4a58 6px, #4a4a58 8px, #aaa 8px, #aaa 14px, #4a4a58 14px, #4a4a58 16px)',
            borderLeft: '2px solid #bbb',
            borderRight: '2px solid #4a4a58',
          }}
        />
        <div className="w-[10px] h-full rotate-3 origin-top"
          style={{
            background: 'repeating-linear-gradient(180deg, #8a8a9a 0px, #8a8a9a 6px, #4a4a58 6px, #4a4a58 8px, #aaa 8px, #aaa 14px, #4a4a58 14px, #4a4a58 16px)',
            borderLeft: '2px solid #bbb',
            borderRight: '2px solid #4a4a58',
          }}
        />
      </div>

      {/* Sign board */}
      <div
        className={cn(
          'relative w-full max-w-[420px] p-7 pb-6 border-[6px] border-wood-edge',
          'shadow-wood-sign pixel-art',
          className,
        )}
        style={{
          width: 'min(420px, 88vw)',
          background: 'repeating-linear-gradient(0deg, transparent 0px, transparent 3px, rgba(0,0,0,0.04) 3px, rgba(0,0,0,0.04) 4px), linear-gradient(180deg, #c8956c 0%, #a06840 50%, #6b4423 100%)',
          boxShadow: 'inset 0 2px 0 rgba(255,255,255,0.15), inset 0 -4px 0 rgba(0,0,0,0.2), 0 8px 0 #4a2e18, 0 12px 24px rgba(0,0,0,0.45)',
        }}
      >
        {/* Nail details */}
        <div className="absolute top-[10px] left-[14px] w-2 h-2 rounded-full"
          style={{ background: 'radial-gradient(circle, #888 30%, #555 70%)', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.3)' }}
        />
        <div className="absolute top-[10px] right-[14px] w-2 h-2 rounded-full"
          style={{ background: 'radial-gradient(circle, #888 30%, #555 70%)', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.3)' }}
        />

        {/* Plank lines */}
        <div className="absolute inset-0 pointer-events-none rounded-inherit"
          style={{ background: 'repeating-linear-gradient(90deg, transparent 0px, transparent 60px, rgba(0,0,0,0.06) 60px, rgba(0,0,0,0.06) 62px)' }}
        />

        {children}
      </div>
    </div>
  );
}
