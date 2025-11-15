const { FlatCompat } = require("@eslint/eslintrc");
const path = require("path");
const nextPlugin = require("@next/eslint-plugin-next");

const compat = new FlatCompat({
  baseDirectory: __dirname,
  resolvePluginsRelativeTo: __dirname,
});

module.exports = [
  ...compat.extends(
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ),

  {
    plugins: {
      '@next/next': nextPlugin,
    },
  },

  // next/core-web-vitals はFlatCompatでは読み込めない
  // nextPlugin.configs["core-web-vitals"],

  {
    ignores: [
      "node_modules/",
      ".next/",
      ".husky/",
    ],
  },
];
