import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          dark: '#0a0e27',
          DEFAULT: '#16213e',
          light: '#1a1a2e',
        },
        accent: {
          red: '#e94560',
          gold: '#d4af37',
        },
        text: {
          primary: '#c0c0c0',
          secondary: '#808080',
        },
        success: '#4caf50',
        error: '#f44336',
        border: '#404854',
        sky: {
          top: '#5b3a8c',
          mid: '#c45a28',
          low: '#f0a830',
          glow: '#ffe566',
        },
        hill: {
          far: '#3d2860',
          near: '#2d6b35',
        },
        wheat: {
          light: '#e8c547',
          mid: '#c9a030',
          dark: '#8b6914',
        },
        path: {
          DEFAULT: '#c4a060',
          dark: '#8b7040',
        },
        wood: {
          light: '#c8956c',
          mid: '#a06840',
          dark: '#6b4423',
          edge: '#4a2e18',
        },
        roof: {
          red: '#8b3030',
          dark: '#5c2020',
        },
        wall: {
          cream: '#d4b896',
          shadow: '#a08060',
        },
        chain: {
          metal: '#8a8a9a',
          shadow: '#4a4a58',
        },
      },
      fontFamily: {
        pixel: ['"Courier New"', 'Consolas', 'Monaco', 'monospace'],
        mono: ['"Courier New"', 'Consolas', 'monospace'],
        ui: ['Arial', 'sans-serif'],
      },
      animation: {
        'pulse-text': 'pulse-text 1.5s ease-in-out infinite',
        'sun-pulse': 'sun-pulse 6s ease-in-out infinite',
        'cloud-drift': 'cloud-drift 40s linear infinite',
        'cloud-drift-reverse': 'cloud-drift 55s linear infinite reverse',
        'blade-spin': 'blades-spin 8s linear infinite',
        'window-glow': 'window-glow 3s ease-in-out infinite',
        'wheat-sway': 'wheat-sway 4s ease-in-out infinite',
        'walker-bob': 'walker-bob 0.4s ease-in-out infinite',
        'walk-right': 'walk-right 18s linear infinite',
        'walk-left': 'walk-left 22s linear infinite',
        'sign-sway': 'sign-sway 5s ease-in-out infinite',
      },
      keyframes: {
        'pulse-text': {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '1' },
        },
        'sun-pulse': {
          '0%, 100%': { transform: 'scale(1)', opacity: '1' },
          '50%': { transform: 'scale(1.05)', opacity: '0.92' },
        },
        'cloud-drift': {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(60px)' },
        },
        'blades-spin': {
          from: { transform: 'translateX(-50%) rotate(0deg)' },
          to: { transform: 'translateX(-50%) rotate(360deg)' },
        },
        'window-glow': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        'wheat-sway': {
          '0%, 100%': { transform: 'skewX(0deg)' },
          '50%': { transform: 'skewX(1.5deg)' },
        },
        'walker-bob': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-2px)' },
        },
        'walk-right': {
          '0%': { left: '-3%', opacity: '0' },
          '5%': { opacity: '1' },
          '95%': { opacity: '1' },
          '100%': { left: '103%', opacity: '0' },
        },
        'walk-left': {
          '0%': { right: '-3%', opacity: '0' },
          '5%': { opacity: '1' },
          '95%': { opacity: '1' },
          '100%': { right: '103%', opacity: '0' },
        },
        'sign-sway': {
          '0%, 100%': { transform: 'rotate(-0.6deg)' },
          '50%': { transform: 'rotate(0.6deg)' },
        },
      },
      boxShadow: {
        'inner-glow': 'inset 0 2px 0 rgba(255,255,255,0.15), inset 0 -4px 0 rgba(0,0,0,0.2)',
        'wood-sign': '0 8px 0 #4a2e18, 0 12px 24px rgba(0,0,0,0.45)',
      },
    },
  },
  plugins: [],
} satisfies Config;
