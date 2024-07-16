// webpack.config.js
const webpack = require('webpack');

module.exports = {
  // Configurations spécifiques à Webpack ici
  plugins: [
    new webpack.DefinePlugin({
      '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': false  // ou true selon vos besoins
    })
  ]
};
