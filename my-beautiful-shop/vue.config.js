// vue.config.js
const webpack = require('webpack'); // Assurez-vous d'importer webpack

module.exports = {
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': false  // ou true selon vos besoins
      })
    ]
  }
};
