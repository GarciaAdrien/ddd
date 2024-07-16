<template>
  <div class="app">
    <div v-if="!dataLoaded && processing" class="loading-spinner">
      <div class="loader"></div>
      <p class="white">Chargement en cours...</p>
    </div>
    <div class="chart-container">
      <h2>Graphique Commercial</h2>
      <img :src="commercialGraphUrl" alt="Graphique Commercial">
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      commercialGraphUrl: ''
    };
  },
  created() {
    this.dataLoaded = false;
    // Appel à l'API Flask pour récupérer le graphique commercial
    this.fetchCommercialGraph();
  },
  methods: {
    fetchCommercialGraph() {
      axios.get('http://localhost:5000/get_graph_commercial', {
        responseType: 'arraybuffer'  // Indiquer que la réponse est un tableau d'octets
      })
        .then(response => {
          // Convertir les données reçues en URL d'image pour l'affichage
          const blob = new Blob([response.data], { type: 'image/png' });
          this.commercialGraphUrl = URL.createObjectURL(blob);
          this.dataLoaded = true;
        })

        .catch(error => {
          console.error('Erreur lors de la récupération du graphique commercial:', error);

        });
    }
  }
};
</script>






<style>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
}

.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  margin-top: 0;
  background-image: url('../assets/BeautyShop.png');
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
  overflow-x: hidden;
}

.loading-spinner {
flex-direction: column;
justify-content: center;
align-items: center;
height: 200px;
}

.loader {
border: 4px solid rgba(255, 0, 0, 0.3);
border-radius: 50%;
border-top: 4px solid #fefefe;
width: 50px;
height: 50px;
left:50%;
right:50%;
animation: spin 1s linear infinite;
margin-top: 100px;
justify-content: center;
position: absolute;
margin-left:25px;
}



</style>