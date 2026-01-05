/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./api/templates/**/*.html",
    "./api/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        nord: {
          // Polar Night - Darker shades for text and UI elements
          'gray-1': '#2E3440',
          'gray-2': '#3B4252',
          'gray-3': '#434C5E',
          'gray-4': '#4C566A',

          // Snow Storm - Light backgrounds
          'snow-1': '#D8DEE9',
          'snow-2': '#E5E9F0',
          'snow-3': '#ECEFF4',

          // Frost - Primary accent colors (cool blues)
          'frost-1': '#8FBCBB',
          'frost-2': '#88C0D0',
          'frost-3': '#81A1C1',
          'frost-4': '#5E81AC',

          // Aurora - Highlight colors
          'aurora-red': '#BF616A',
          'aurora-orange': '#D08770',
          'aurora-yellow': '#EBCB8B',
          'aurora-green': '#A3BE8C',
          'aurora-purple': '#B48EAD',
        }
      },
      fontFamily: {
        sans: ['Figtree', 'system-ui', 'sans-serif'],
        mono: ['Roboto Mono', 'monospace'],
      },
      animation: {
        'visited-pulse': 'visitedPulse 0.3s ease-out',
        'path-glow': 'pathGlow 0.5s ease-out',
        'wall-pop': 'wallPop 0.3s ease-out',
      },
      keyframes: {
        visitedPulse: {
          '0%': { transform: 'scale(0.8)', opacity: '0' },
          '50%': { transform: 'scale(1.05)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        pathGlow: {
          '0%': { boxShadow: '0 0 0 0 rgba(94, 129, 172, 0.5)' },
          '50%': { boxShadow: '0 0 15px 5px rgba(94, 129, 172, 0.3)' },
          '100%': { boxShadow: '0 0 5px 2px rgba(94, 129, 172, 0.2)' },
        },
        wallPop: {
          '0%': { transform: 'scale(0)' },
          '50%': { transform: 'scale(1.1)' },
          '100%': { transform: 'scale(1)' },
        },
      },
    },
  },
  plugins: [],
}
