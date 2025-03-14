const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: config => {
    config.plugin('define').tap(definitions => {
      Object.assign(definitions[0].__VUE_OPTIONS_API__ ? definitions[0] : definitions[0]['process.env'], {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'true'
      })
      return definitions
    })
  },
  // Define the page title
  pages: {
    index: {
      entry: 'src/main.js',
      title: 'Advanced User Management Portal',
    },
  }
})
