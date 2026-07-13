import { useAuth } from '@/features/auth';

export function useCharacter() {
  const { character, isRegistered } = useAuth();

  return {
    character: character
      ? {
          displayName: character.display_name,
          username: character.username,
          characterClass: character.character_class ?? 'adventurer',
          avatar: character.avatar ?? 'pixel_adventurer',
          level: character.level,
          experience: character.experience,
          coins: character.coins,
        }
      : null,
    isRegistered,
  };
}
