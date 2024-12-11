// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Usa la clase "dark" para habilitar el modo oscuro
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './comisarias/templates/**/*.html',
    './divisioncomunicaciones/templates/**/*.html',
    './divisioncomunicaciones/**/*.html',
    './comisarias/**/*.html',
    './static/**/*.css',
  ],
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      'xs': {'min': '440px', 'max': '640px'}, // Breakpoint personalizado
    },
    extend: {
      colors: {
        prueba: '#48556a', // Nuevo color personalizado
      },
    },
  },
  plugins: [],
}
