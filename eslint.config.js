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

  {
    ignores: [
      "node_modules/",
      ".next/",
      ".husky/",
    ],
  },
];
