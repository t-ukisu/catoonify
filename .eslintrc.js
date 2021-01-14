module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/essential',
    '@vue/airbnb',
    "@vue/typescript/recommend"
  ],
  rules: {},
  parserOptions: {
    ecmaVersion: 2020,
  },
  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        "**/tests/unit/**/*.spec.{j,t}s?(x)"
      ],
      env: {
        jest: true,
      },
    },
  ],
};
