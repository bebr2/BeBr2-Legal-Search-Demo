module.exports = {
  assetsDir: 'static',
  devServer: {
    proxy: {
      '/search': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
      },
      '/match': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
      },
      '/show': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
      },
      '/recommend': {
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
      },
    }
  },
  publicPath: "/",
  chainWebpack: config => {
    config.module.rule('md')
      .test(/\.md/)
      .use('vue-loader')
      .loader('vue-loader')
      .end()
      .use('vue-markdown-loader')
      .loader('vue-markdown-loader/lib/markdown-compiler')
      .options({
        raw: true
      })
  }
}
