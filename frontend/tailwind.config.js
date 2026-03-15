/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'bg-dark': '#0d0d1a',
        'bg-mid': '#12122a',
        'bg-card': '#1a1a35',
        'border': '#3a3a6a',
        'accent-1': '#ff6eb4',
        'accent-2': '#7b61ff',
        'accent-3': '#00e5ff',
        'accent-4': '#ffe066',
        'accent-5': '#4dff91',
        'text-main': '#e8e8ff',
        'text-dim': '#8888bb'
      },
      fontFamily: {
        'pixel': ['"Press Start 2P"', 'cursive'],
        'mono': ['"Share Tech Mono"', 'monospace']
      },
      boxShadow: {
        'pixel': '4px 4px 0 #000',
        'pixel-accent': '4px 4px 0 #7b61ff',
        'pixel-pink': '4px 4px 0 #ff6eb4',
        'pixel-cyan': '4px 4px 0 #00e5ff',
        'pixel-green': '4px 4px 0 #4dff91'
      }
    }
  },
  plugins: []
};
