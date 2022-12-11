/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");

module.exports = {
  content: ["./src/**/*.{html,js,ts,tsx,jsx}"],
  theme: {
    extend: {
      scale: {
        102: "102%",
      },
      colors: {
        primary: colors.indigo,
        accent: colors.lime,
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
