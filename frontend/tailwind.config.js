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
        background: '#0B0C10',
        surface: 'rgba(31, 40, 51, 0.4)',
        surfaceHighlight: 'rgba(45, 55, 72, 0.6)',
        border: 'rgba(69, 162, 158, 0.2)',
        primary: {
          DEFAULT: '#66FCF1', // Neon Cyan
          hover: '#45A29E',
          light: '#C5C6C7',
        },
        secondary: {
          DEFAULT: '#8B5CF6', // Purple
          light: '#A78BFA',
        },
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
        text: {
          main: '#FFFFFF',
          muted: '#C5C6C7',
        }
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [],
}
