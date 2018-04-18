/* global module */
/* global require */
/* global __dirname */

const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
    context: __dirname,
    entry: {
        main: path.resolve('assets', 'javascript', 'app.js'),
        authoring: path.resolve('assets', 'javascript', 'authoring.js')
    },
    output: {
        path: path.resolve('assets', 'dist'),
        filename: '[name]-bundle-[hash:6].js'
    },
    resolve: {
        extensions: ['*', '.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve('assets', 'javascript')
        }
    },
    module: {
        rules: [
            {
                enforce: 'pre',
                test: /\.(js|vue)$/,
                loader: 'eslint-loader',
                exclude: /node_modules/
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {
                        scss: ExtractTextPlugin.extract({
                            use: ['css-loader', 'sass-loader'],
                            fallback: 'vue-style-loader'
                        })
                    }
                }
            },
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    use: ['css-loader', 'sass-loader'],
                    fallback: 'style-loader'
                })
            },
            {
                test: /\.js$/,
                use: ['babel-loader']
            }
        ]
    },
    plugins: [
        new UglifyJsPlugin({
            test: /\.js($|\?)/i,
            sourceMap: true,
            uglifyOptions: {
                warnings: false
            }
        }),
        new ExtractTextPlugin('[name]-[hash:6].css'),
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
