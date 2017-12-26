const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: path.resolve('assets', 'javascript', 'app.js'),
    output: {
        path: path.resolve('assets', 'dist'),
        filename: 'bundle-[hash:6].js'
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'sass-loader']
                })
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin('site-[hash:6].css'),
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
