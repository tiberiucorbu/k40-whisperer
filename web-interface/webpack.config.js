const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
const SpriteLoaderPlugin = require('svg-sprite-loader/plugin');


const cert = fs.readFileSync('./cert/server.crt');
const key = fs.readFileSync('./cert/server.key');
module.exports = {
    devtool: 'inline-source-map',
    entry: {
        'k40-web-interface': [
            './src/main.js'
        ],
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].js',
    },

    resolve: {
        extensions: ['.ts', '.js', '.scss', '.svg', '.pug']
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                loader: 'ts-loader'
            },
            {
                test: /\.scss/,
                use: [
                    // 'stylesheet-loader',
                    'css-loader',
                    {
                        loader: 'sass-loader', options: {
                            includePaths: ['./node_modules']
                        }
                    },
                    // 'resolve-url-loader'
                ]
            },
            {
                test: /\.html$/,
                use: [
                    {
                        loader: "html-loader"
                    }
                ]
            },
            {
                test: /\.md$/,
                use: [
                    {
                        loader: "html-loader"
                    },
                    {
                        loader: "markdown-loader",
                        options: {
                            /* your options here */
                        }
                    }
                ]
            },
            {
                test: /\.pug/,
                use: {
                    loader: "pug-loader",
                    options: {}
                }
            }, {
                test: /\.svg$/,
                use: [
                    {
                        loader: 'svg-sprite-loader',
                        /*options: { ... }*/
                    },
                    //'svg-fill-loader',
                    //'svgo-loader'
                ]
            }
        ]
    },
    devServer: {
        https: true,
        cert: cert,
        key: key,
        before: function (app) {
            app.use(function (req, res, next) {
                console.log(req.path) // populated!
                next();
            });
        },
        port: 58081,
        hot: false,
        inline: false
    },
    plugins: [
        // new UglifyJSPlugin(),
        new HtmlWebpackPlugin({
            title: 'WebComponents example',
            template: './src/main.html',
            inject: false,
            filename: 'main.html',
        }),
        new SpriteLoaderPlugin()
    ]
};