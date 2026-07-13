import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { checkCharacterExistence } from './checkCharacter';
import { cn } from '@/shared/lib/cn';



export function StartScreen() {
  const [isProcessing, setIsProcessing] = useState(false);
  const navigate = useNavigate();

  const handleStart = useCallback(async () => {
    if (isProcessing) return;
    setIsProcessing(true);

    try {
      const result = await checkCharacterExistence();

      if (result.exists && result.user) {
        // Character exists — redirect to Dashboard (game entry point)
        navigate('/dashboard');
      } else {
        // No character — redirect to character creation
        navigate('/character-creation');
      }
    } catch {
      navigate('/character-creation');
    } finally {
      setIsProcessing(false);
    }
  }, [isProcessing, navigate]);

  return (
    <div className="start-screen fixed inset-0 w-full h-full overflow-hidden pixel-art">
      {/* ==================== LAYER 1 — Background ==================== */}
      <div className="scene-layer layer-background" aria-hidden="true">
        {/* Sky */}
        <div className="pixel-sky" />
        {/* Sun */}
        <div className="pixel-sun" />
        {/* Clouds */}
        <div className="pixel-cloud pixel-cloud-1" />
        <div className="pixel-cloud pixel-cloud-2" />
        {/* Hills */}
        <div className="pixel-hills">
          <div className="pixel-hill pixel-hill-far" />
          <div className="pixel-hill pixel-hill-near" />
        </div>
        {/* Village grass */}
        <div className="village-grass" />
        {/* Village Houses */}
        <div className="village-houses">
          {/* House 1 (left) */}
          <div className="farm-house farm-house-left">
            <div className="farm-house-roof" />
            <div className="farm-house-body">
              <div className="farm-house-window" />
              <div className="farm-house-door" />
              <div className="chimney chimney-1" />
              <div className="smoke smoke-1">
                <div className="smoke-puff puff-1" />
                <div className="smoke-puff puff-2" />
                <div className="smoke-puff puff-3" />
              </div>
            </div>
          </div>
          {/* House 2 (center) */}
          <div className="farm-house farm-house-center">
            <div className="farm-house-roof" />
            <div className="farm-house-body">
              <div className="farm-house-window" />
              <div className="farm-house-door" />
              <div className="chimney chimney-2" />
              <div className="smoke smoke-2">
                <div className="smoke-puff puff-1" />
                <div className="smoke-puff puff-2" />
                <div className="smoke-puff puff-3" />
              </div>
            </div>
          </div>
          {/* House 3 (right) */}
          <div className="farm-house farm-house-right">
            <div className="farm-house-roof" />
            <div className="farm-house-body">
              <div className="farm-house-window" />
              <div className="farm-house-door" />
              <div className="chimney chimney-3" />
              <div className="smoke smoke-3">
                <div className="smoke-puff puff-1" />
                <div className="smoke-puff puff-2" />
                <div className="smoke-puff puff-3" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ==================== LAYER 2 — Middle ==================== */}
      <div className="scene-layer layer-middle" aria-hidden="true">
        {/* Windmill */}
        <div className="pixel-windmill">
          <div className="windmill-base" />
          <div className="windmill-tower" />
          <div className="windmill-roof" />
          <div className="windmill-blades" id="windmill-blades">
            <div className="blade blade-1" />
            <div className="blade blade-2" />
            <div className="blade blade-3" />
            <div className="blade blade-4" />
            <div className="blade-hub" />
          </div>
        </div>
        {/* Wheat field */}
        <div className="wheat-field">
          <div className="wheat-row" />
          <div className="wheat-stalks" />
          <div className="wheat-stalks wheat-stalks-2" />
        </div>
      </div>

      {/* ==================== LAYER 3 — Foreground ==================== */}
      <div className="scene-layer layer-foreground">
        {/* Wooden fence */}
        <div className="wooden-fence">
          <div className="fence-post fence-post-1" />
          <div className="fence-rail fence-rail-top" />
          <div className="fence-rail fence-rail-bottom" />
          <div className="fence-post fence-post-2" />
          <div className="fence-post fence-post-3" />
          <div className="fence-post fence-post-4" />
          <div className="fence-post fence-post-5" />
        </div>

        {/* Wooden signpost with two boards */}
        <div className="signpost">
          <div className="signpost-pole" />
          {/* Upper board: LifeQuest (fixed) */}
          <div className="signboard signboard-top">
            <div className="signboard-wood-texture" />
            <h1 className="signboard-title">LifeQuest</h1>
          </div>
          {/* Chains hanging from upper board */}
          <div className="start-chains">
            <div className="start-chain start-chain-left" />
            <div className="start-chain start-chain-right" />
          </div>
          {/* Lower hanging board: Start (swinging, clickable) */}
          <button
            className={cn(
              'signboard signboard-bottom',
              isProcessing && 'start-sign-swing-paused',
            )}
            id="start-button"
            type="button"
            onClick={handleStart}
            disabled={isProcessing}
            aria-label="Start Game"
          >
            <div className="signboard-wood-texture" />
            <span className="signboard-start-text">
              {isProcessing ? '...' : 'Start'}
            </span>
          </button>
        </div>
      </div>

      {/* Ground cover (bottom edge) */}
      <div className="ground-cover" />

      {/* Vignette overlay */}
      <div className="absolute inset-0 pointer-events-none z-10"
        style={{
          background: 'radial-gradient(ellipse at center 40%, transparent 40%, rgba(0,0,0,0.35) 100%)',
        }}
      />
    </div>
  );
}
