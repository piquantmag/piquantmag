module.exports = {
    "env": {
        "browser": true,
        "es6": true
    },
    "extends": [
        "eslint:recommended",
        "plugin:vue/strongly-recommended"
    ],
    "parserOptions": {
        "sourceType": "module"
    },
    "rules": {
        "vue/html-indent": [
            "error",
            4
        ],
        "no-console": 0,
        "indent": [
            "error",
            4
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "error",
            "single"
        ]
    },
    plugins: [
        'vue'
    ]
};
