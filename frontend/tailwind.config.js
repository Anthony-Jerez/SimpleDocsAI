/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6', // primary accent (vivid purple)
          600: '#7c3aed', // deeper
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
        },
        bg: '#0b0f1a', // deep navy background
        panel: '#0f1422', // left/right cards
        panelElev: '#141a2a',
        text: '#e6e6f0',
        sub: '#a1a1b5',
      },
      boxShadow: {
        soft: '0 8px 30px rgba(0,0,0,0.25)',
      },
      borderRadius: {
        xl2: '1.25rem',
      }
    },
  },
  plugins: [],
}