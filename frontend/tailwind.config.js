/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        background: '#09090b',
        surface: '#18181b',
        border: '#27272a',
        primary: {
          DEFAULT: '#8b5cf6', // Violet
          hover: '#7c3aed',
          light: '#a78bfa',
        },
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        text: {
          main: '#fafafa',
          muted: '#a1a1aa',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
