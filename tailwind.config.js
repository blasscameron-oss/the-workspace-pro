/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './content/**/*.html', './static/**/*.html'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'primary': '#2a6b7e',
        'primary-light': '#4a8fa3',
        'secondary': '#c86b4a',
        'secondary-light': '#e48c6d',
        'surface': '#fefcf8',
        'card': '#ffffff',
        'border': '#e8e3da',
        'text': '#1f2937',
        'text-light': '#6b7280',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'serif': ['Playfair Display', 'serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 3s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    }
  },
  plugins: [],
}
