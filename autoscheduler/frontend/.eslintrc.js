// We're using a Javascript file rather than JSON, as it allows us to comment stuff in here
module.exports = {
    parser: "@typescript-eslint/parser",
    extends: [
        'plugin:react/recommended', // Uses the recommended rules from @eslint-plugin-react
        'plugin:@typescript-eslint/recommended', // Uses the recommended rules from @typescript-eslint/eslint-plugin
    ],
    parserOptions: {
        ecmaVersion: 2018,
        sourceType: 'module',
        ecmaFeatures: {
            jsx: true, // Allows for parsing of JSX/TSX(React's javascript superscript)
        },
    },
    rules: {
        // Anything here specifies ESLint rules
    },
    settings: {
        react: {
            version: 'detect', // Tells eslint-plugin-react to automatically detect the version of React to use
        }
    }
}