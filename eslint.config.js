const { FlatCompat } = require("@eslint/eslintrc");
const path = require("path");
const nextPlugin = require("@next/eslint-plugin-next");

// __dirname は CJS (module.exports を使う) ファイルでは利用可能です
const compat = new FlatCompat({
  baseDirectory: __dirname,
  resolvePluginsRelativeTo: __dirname,
});

module.exports = [
  // FlatCompatの extends() を使って、以前の .eslintrc.json 相当の設定を読み込みます
  ...compat.extends(
    "plugin:@typescript-eslint/recommended", // TypeScript
    "prettier"                              // Prettier競合回避 (必ず最後)
  ),

  nextPlugin.configs["core-web-vitals"],

  // 無視するディレクトリ
  {
    ignores: [
      "node_modules/",
      ".next/",
      "dist/",
      ".husky/",
    ],
  },
];
