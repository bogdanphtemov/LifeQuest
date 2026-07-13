export interface CharacterData {
  displayName?: string;
  username?: string;
  characterClass?: string;
  avatar?: string;
  level?: number;
  experience?: number;
  coins?: number;
  texturePath?: string | null;
  spriteData?: string | null;
}

/** Character customization options for the creation form */
export interface AppearanceOptions {
  /** Character name to display */
  name: string;
  /** RPG class */
  characterClass: 'adventurer' | 'warrior' | 'mage' | 'archer' | 'rogue';
  /** Skin tone */
  skinTone: 'light' | 'tan' | 'dark' | 'pale';
  /** Hair style */
  hairStyle: 'short' | 'long' | 'spiky' | 'bald' | 'ponytail';
  /** Hair color */
  hairColor: 'brown' | 'blonde' | 'black' | 'red' | 'white';
  /** Outfit color */
  outfitColor: 'blue' | 'red' | 'green' | 'black' | 'white';
}
