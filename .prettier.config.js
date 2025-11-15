module.exports = {
  // --- .prettierrc.json からの内容 ---
  tabWidth: 2,
  printWidth: 100,
  trailingComma: "es5",
  semi: true,
  singleQuote: false,

  // --- 元の prettier.config.js の内容 ---
  plugins: [require("prettier-plugin-tailwindcss")],
};
