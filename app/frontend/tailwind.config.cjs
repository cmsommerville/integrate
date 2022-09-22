/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,ts,tsx,jsx}"],
  theme: {
    extend: {
      colors: {
        "primary-50": "rgb(255 241 242)",
        "primary-100": "rgb(255 228 230)",
        "primary-200": "rgb(254 205 211)",
        "primary-300": "rgb(253 164 175)",
        "primary-400": "rgb(251 113 133)",
        "primary-500": "rgb(244 63 94)",
        "primary-600": "rgb(225 29 72)",
        "primary-700": "rgb(190 18 60)",
        "primary-800": "rgb(159 18 57)",
        "primary-900": "rgb(136 19 55)",
      },
    },
  },
  plugins: [],
};
