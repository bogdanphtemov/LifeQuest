import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { useAuth, useAuthStore, apiClient } from '@/features/auth';
import type { AppearanceOptions } from '@/features/character/types/character.types';

const CLASSES: { value: AppearanceOptions['characterClass']; label: string; emoji: string; desc: string }[] = [
  { value: 'adventurer', label: 'Adventurer', emoji: '🧭', desc: 'A balanced all-rounder' },
  { value: 'warrior', label: 'Warrior', emoji: '⚔️', desc: 'Strong melee fighter' },
  { value: 'mage', label: 'Mage', emoji: '🔮', desc: 'Powerful spellcaster' },
  { value: 'archer', label: 'Archer', emoji: '🏹', desc: 'Ranged precision striker' },
  { value: 'rogue', label: 'Rogue', emoji: '🗡️', desc: 'Stealthy and swift' },
];

const SKIN_TONES: { value: string; label: string; color: string }[] = [
  { value: 'light', label: 'Light', color: '#f5d0a9' },
  { value: 'tan', label: 'Tan', color: '#d4a574' },
  { value: 'dark', label: 'Dark', color: '#8b5e3c' },
  { value: 'pale', label: 'Pale', color: '#f0e6d3' },
];

const HAIR_STYLES: { value: string; label: string }[] = [
  { value: 'short', label: 'Short' },
  { value: 'long', label: 'Long' },
  { value: 'spiky', label: 'Spiky' },
  { value: 'bald', label: 'Bald' },
  { value: 'ponytail', label: 'Ponytail' },
];

const HAIR_COLORS: { value: string; label: string; color: string }[] = [
  { value: 'brown', label: 'Brown', color: '#6b3a2a' },
  { value: 'blonde', label: 'Blonde', color: '#e8c840' },
  { value: 'black', label: 'Black', color: '#2a2a2a' },
  { value: 'red', label: 'Red', color: '#c04020' },
  { value: 'white', label: 'White', color: '#d0d0d0' },
];

const OUTFIT_COLORS: { value: string; label: string; color: string }[] = [
  { value: 'blue', label: 'Blue', color: '#4060c0' },
  { value: 'red', label: 'Red', color: '#c04040' },
  { value: 'green', label: 'Green', color: '#40a040' },
  { value: 'black', label: 'Black', color: '#404040' },
  { value: 'white', label: 'White', color: '#d0d0d0' },
];

export function CharacterCreationPage() {
  const navigate = useNavigate();
  const { isNoTelegramContext, isLoading } = useAuth();
  const initData = useAuthStore((s) => s.initData);

  const [step, setStep] = useState<1 | 2>(1);
  const [form, setForm] = useState<AppearanceOptions>({
    name: '',
    characterClass: 'adventurer',
    skinTone: 'light',
    hairStyle: 'short',
    hairColor: 'brown',
    outfitColor: 'blue',
  });

  const createMutation = useMutation({
    mutationFn: () => {
      if (!initData) throw new Error('No Telegram session');

      // Build sprite_data JSON from appearance options
      const spriteData = JSON.stringify({
        skinTone: form.skinTone,
        hairStyle: form.hairStyle,
        hairColor: form.hairColor,
        outfitColor: form.outfitColor,
      });

      return apiClient.registerCharacter(initData, {
        display_name: form.name || undefined,
        character_class: form.characterClass,
        sprite_data: spriteData,
      });
    },
    onSuccess: (data) => {
      if (data.user) {
        // Update the auth store with the new session data
        useAuthStore.getState().setSession({
          status: 'success',
          registered: true,
          user: data.user,
        });
      }
      navigate('/game-dashboard', { replace: true });
    },
  });

  const updateField = useCallback(<K extends keyof AppearanceOptions>(
    key: K,
    value: AppearanceOptions[K],
  ) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  }, []);

  const handleSubmit = useCallback(() => {
    createMutation.mutate();
  }, [createMutation]);

  // ── Error / missing Telegram context ──
  if (isNoTelegramContext) {
    return (
      <div
        className="screen-container pixel-art flex flex-col items-center justify-center gap-4"
        style={{ background: '#1a0a2e' }}
      >
        <p className="font-pixel text-[10px] text-[#e8d8b8] text-center max-w-[280px]">
          Open this app from the Telegram bot to create your character.
        </p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div
        className="screen-container pixel-art flex items-center justify-center"
        style={{ background: '#1a0a2e' }}
      >
        <p className="font-pixel text-[10px] text-[#e8d8b8] animate-pulse">
          Loading...
        </p>
      </div>
    );
  }

  return (
    <div
      className="screen-container pixel-art flex flex-col items-center overflow-y-auto"
      style={{ background: '#1a0a2e' }}
    >
      {/* ── Title ── */}
      <div className="w-full px-4 py-3 text-center border-b border-[#4a2a6a]">
        <h1 className="font-pixel text-[12px] text-[#e8d8b8] tracking-wider">
          ✦ CREATE YOUR CHARACTER ✦
        </h1>
      </div>

      {/* ── Step indicator ── */}
      <div className="flex items-center gap-2 my-3">
        <div
          className={`w-6 h-6 rounded-full flex items-center justify-center font-pixel text-[8px] ${
            step === 1 ? 'bg-[#e8d8b8] text-[#1a0a2e]' : 'bg-[#4a2a6a] text-[#e8d8b8]'
          }`}
        >
          1
        </div>
        <div className="w-12 h-[2px] bg-[#4a2a6a]" />
        <div
          className={`w-6 h-6 rounded-full flex items-center justify-center font-pixel text-[8px] ${
            step === 2 ? 'bg-[#e8d8b8] text-[#1a0a2e]' : 'bg-[#4a2a6a] text-[#e8d8b8]'
          }`}
        >
          2
        </div>
      </div>

      {/* ── Error message ── */}
      {createMutation.isError && (
        <p className="font-pixel text-[8px] text-[#ff6060] px-4 text-center mb-2">
          {createMutation.error instanceof Error
            ? createMutation.error.message
            : 'Failed to create character'}
        </p>
      )}

      {/* ── STEP 1: Name & Class ── */}
      {step === 1 && (
        <div className="w-full px-4 flex flex-col gap-3">
          {/* Character Name */}
          <div>
            <label className="font-pixel text-[8px] text-[#a080c0] block mb-1">
              CHARACTER NAME
            </label>
            <input
              type="text"
              maxLength={20}
              value={form.name}
              onChange={(e) => updateField('name', e.target.value)}
              placeholder="Enter your name..."
              className="w-full bg-[#2a1040] border border-[#4a2a6a] rounded px-3 py-2 font-pixel text-[10px] text-[#e8d8b8] placeholder:text-[#6a4a8a] outline-none focus:border-[#e8d8b8]"
            />
          </div>

          {/* Class Selection */}
          <div>
            <label className="font-pixel text-[8px] text-[#a080c0] block mb-1">
              CHARACTER CLASS
            </label>
            <div className="grid grid-cols-2 gap-2">
              {CLASSES.map((cls) => (
                <button
                  key={cls.value}
                  onClick={() => updateField('characterClass', cls.value)}
                  className={`p-2 rounded border text-left transition-colors ${
                    form.characterClass === cls.value
                      ? 'border-[#e8d8b8] bg-[#3a1a5a]'
                      : 'border-[#4a2a6a] bg-[#2a1040] hover:bg-[#3a1a5a]'
                  }`}
                >
                  <span className="font-pixel text-[14px]">{cls.emoji}</span>
                  <p className="font-pixel text-[9px] text-[#e8d8b8] mt-1">
                    {cls.label}
                  </p>
                  <p className="font-pixel text-[7px] text-[#8060a0]">
                    {cls.desc}
                  </p>
                </button>
              ))}
            </div>
          </div>

          {/* Next button */}
          <button
            onClick={() => setStep(2)}
            className="mt-2 w-full py-3 rounded font-pixel text-[10px] text-[#1a0a2e] bg-[#e8d8b8] hover:bg-[#d0c0a0] transition-colors"
          >
            NEXT: APPEARANCE ▶
          </button>
        </div>
      )}

      {/* ── STEP 2: Appearance ── */}
      {step === 2 && (
        <div className="w-full px-4 flex flex-col gap-3">
          {/* Preview */}
          <div
            className="w-full h-20 rounded border border-[#4a2a6a] bg-[#2a1040] flex items-center justify-center"
          >
            <span className="font-pixel text-[24px]">
              {form.characterClass === 'mage' ? '🧙' :
               form.characterClass === 'warrior' ? '⚔️' :
               form.characterClass === 'archer' ? '🏹' :
               form.characterClass === 'rogue' ? '🗡️' : '🧭'}
            </span>
          </div>

          {/* Skin Tone */}
          <div>
            <label className="font-pixel text-[8px] text-[#a080c0] block mb-1">
              SKIN TONE
            </label>
            <div className="flex gap-2">
              {SKIN_TONES.map((tone) => (
                <button
                  key={tone.value}
                  onClick={() => updateField('skinTone', tone.value as AppearanceOptions['skinTone'])}
                  className={`flex-1 h-10 rounded border flex items-center justify-center ${
                    form.skinTone === tone.value
                      ? 'border-[#e8d8b8] scale-105'
                      : 'border-[#4a2a6a]'
                  }`}
                  style={{ backgroundColor: tone.color }}
                >
                  <span className="font-pixel text-[7px] text-[#1a0a2e] font-bold">
                    {tone.label}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Hair Style */}
          <div>
            <label className="font-pixel text-[8px] text-[#a080c0] block mb-1">
              HAIR STYLE
            </label>
            <div className="flex gap-1 flex-wrap">
              {HAIR_STYLES.map((style) => (
                <button
                  key={style.value}
                  onClick={() => updateField('hairStyle', style.value as AppearanceOptions['hairStyle'])}
                  className={`px-3 py-1 rounded border font-pixel text-[8px] transition-colors ${
                    form.hairStyle === style.value
                      ? 'border-[#e8d8b8] bg-[#3a1a5a] text-[#e8d8b8]'
                      : 'border-[#4a2a6a] bg-[#2a1040] text-[#a080c0] hover:bg-[#3a1a5a]'
                  }`}
                >
                  {style.label}
                </button>
              ))}
            </div>
          </div>

          {/* Hair Color */}
          <div>
            <label className="font-pixel text-[8px] text-[#a080c0] block mb-1">
              HAIR COLOR
            </label>
            <div className="flex gap-2">
              {HAIR_COLORS.map((color) => (
                <button
                  key={color.value}
                  onClick={() => updateField('hairColor', color.value as AppearanceOptions['hairColor'])}
                  className={`flex-1 h-10 rounded border flex items-center justify-center ${
                    form.hairColor === color.value
                      ? 'border-[#e8d8b8] scale-105'
                      : 'border-[#4a2a6a]'
                  }`}
                  style={{ backgroundColor: color.color }}
                >
                  <span className="font-pixel text-[7px] text-white font-bold drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
                    {color.label}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Outfit Color */}
          <div>
            <label className="font-pixel text-[8px] text-[#a080c0] block mb-1">
              OUTFIT COLOR
            </label>
            <div className="flex gap-2">
              {OUTFIT_COLORS.map((color) => (
                <button
                  key={color.value}
                  onClick={() => updateField('outfitColor', color.value as AppearanceOptions['outfitColor'])}
                  className={`flex-1 h-10 rounded border flex items-center justify-center ${
                    form.outfitColor === color.value
                      ? 'border-[#e8d8b8] scale-105'
                      : 'border-[#4a2a6a]'
                  }`}
                  style={{ backgroundColor: color.color }}
                >
                  <span className="font-pixel text-[7px] text-white font-bold drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
                    {color.label}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex gap-2 mt-2">
            <button
              onClick={() => setStep(1)}
              className="flex-1 py-3 rounded font-pixel text-[10px] text-[#e8d8b8] border border-[#4a2a6a] bg-[#2a1040] hover:bg-[#3a1a5a] transition-colors"
            >
              ◀ BACK
            </button>
            <button
              onClick={handleSubmit}
              disabled={createMutation.isPending}
              className="flex-1 py-3 rounded font-pixel text-[10px] text-[#1a0a2e] bg-[#e8d8b8] hover:bg-[#d0c0a0] disabled:opacity-50 transition-colors"
            >
              {createMutation.isPending ? 'CREATING...' : '✨ CREATE!'}
            </button>
          </div>
        </div>
      )}

      <div className="h-6" />
    </div>
  );
}
