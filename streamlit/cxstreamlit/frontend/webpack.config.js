module.exports = function (webpackEnv) {
    return {
        resolve: {
            fallback: {
                crypto: require.resolve("crypto-browserify"),
                stream: require.resolve("stream-browserify"),
            }
        }
    }
}
