import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-sans)'],
        display: ['var(--font-display)'],
        mono: ['var(--font-mono)'],
      },
      gridTemplateColumns: {
        '13': 'repeat(13, minmax(0, 1fr))',
      },
      colors: {
        ink: '#1d1d1f', // accessible black alternative
        paper: '#f8f7f5', // accessible white alternative
        blue: {
          400: '#2589FE',
          500: '#0070F3',
          600: '#2F6FEB',
        },
        navy: {
          500: '#032059',
          400: '#021A62',
          300: '#072273',
        },
        brown: {
          500: '#29180E',
          400: '#41210D',
          300: '#544132',
          200: '#C3C2C0',
        },
        burgundy: {
          500: '#400909',
          400: '#5B0A09'
        },
        grey: {
          500: '#545559',
          400: '#565759',
          300: '#EAEBED',
          200: '#F2F2F2'
        },
        beige: {
          300: '#D8D0C5',
          200: '#D2CAC7'
        },
      popover: 'oklch(1 0 0)',
      popoverForeground: 'oklch(0.145 0 0)',
      },
    },
    keyframes: {
      shimmer: {
        '100%': {
          transform: 'translateX(100%)',
        },
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};
export default config;
