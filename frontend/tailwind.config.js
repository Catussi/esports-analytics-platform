/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#12151a',
          panel: '#1a1f26',
          raised: '#222831',
        },
        border: {
          DEFAULT: '#2a313c',
          strong: '#3d4654',
        },
        text: {
          DEFAULT: '#e8eaed',
          muted: '#8b939e',
          dim: '#5c6370',
        },
        ct: '#5d79ae',
        tside: '#c4872e',
        accent: '#7eb8da',
        positive: '#6abf8a',
        negative: '#d4736e',
      },
      fontFamily: {
        sans: ['"Chakra Petch"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
      },
      fontSize: {
        '2xs': '0.65rem',
      },
      borderRadius: {
        sm: '2px',
        DEFAULT: '3px',
        md: '4px',
      },
      boxShadow: {
        panel: 'inset 0 1px 0 rgba(255,255,255,0.04)',
      },
    },
  },
  plugins: [],
};
