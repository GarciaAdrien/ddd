<template>
  <div class="app">
    <div class="chart-container2">
      <div class="graph-wrapper3">
        <canvas id="directionChart" ref="directionChart"></canvas>
      </div>
      <div class="graph-wrapper3">
        <canvas id="directionChart2" ref="directionChart2"></canvas>
      </div>
    </div>
    <div v-if="loading" class="loading-spinner">
      <div class="loader"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto'; // Import Chart.js from 'chart.js/auto'

export default {
  data() {
    return {
      loading: false,
      directionChart: null,
      directionChart2: null,
      chartTitle: "Nombre de commandes par catégories sur le mois de Juillet 2018", // Ajout du titre ici
    };
  },
  mounted() {
    this.loading = true; // Set loading to true when component mounts
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:5000/get_graph_direction1')
        .then(response => {
          this.renderDirectionChart(response.data);
        })
        .catch(error => {
          console.error('Error fetching Direction 1 chart:', error);
        });

      axios.get('http://localhost:5000/get_graph_direction2')
        .then(response => {
          this.renderDirectionChart2(response.data);
          this.loading = false; // Set loading to false after rendering Direction 2 chart
        })
        .catch(error => {
          console.error('Error fetching Direction 2 chart:', error);
        });
    },
    renderDirectionChart(data) {
      if (!this.directionChart) {
        this.directionChart = new Chart(this.$refs.directionChart.getContext('2d'), {
          type: 'line',
          data: {
            labels: data.labels,
            datasets: [{
              label: 'Nombre de Commandes par Mois',
              data: data.data,
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: 'Nombre de Commandes par Mois',
                font: {
                  size: 18 // Taille de police pour le titre du premier graphique
                }
              }
            },
            // Autres options Chart.js
          }
        });
      } else {
        this.directionChart.data.labels = data.labels;
        this.directionChart.data.datasets[0].data = data.data;
        this.directionChart.update();
      }
    },
    renderDirectionChart2(data) {
      if (!data || !data.labels || !data.datasets) {
        console.error('Invalid data format or datasets are missing:', data);
        return;
      }

      const labels = data.labels.map(day => `Jour ${day}`);
      const datasets = data.datasets.map(dataset => ({
        label: dataset.label,
        data: dataset.data,
        backgroundColor: this.generateGradient(),
        borderWidth: 1
      }));

      if (!this.directionChart2) {
        this.directionChart2 = new Chart(this.$refs.directionChart2.getContext('2d'), {
          type: 'bar',
          data: {
            labels: labels,
            datasets: datasets
          },
          options: {
            plugins: {
              title: {
                display: true,
                text: this.chartTitle,
                font: {
                  size: 18 // Taille de police pour le titre du deuxième graphique
                }
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      } else {
        this.directionChart2.data.labels = labels;
        this.directionChart2.data.datasets = datasets;
        this.directionChart2.update();
      }
    },
    generateGradient() {
      const ctx = this.$refs.directionChart2.getContext('2d');
      const gradient = ctx.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, 'rgba(75, 192, 192, 0.2)');
      gradient.addColorStop(1, 'rgba(75, 192, 192, 1)');
      return gradient;
    }
  }
};
</script>


<style >
.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 90vh;
  margin-top: 0;
  background-size: cover;
  background-attachment: fixed;
  background-position: center;
  overflow-x: hidden;
  padding-bottom: 50px;
}

.loading-spinner {
  display: flex;
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
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

.chart-container2 {
  text-align: center;
    width: 100%;
    height:100%;
}

.graph-wrapper3 {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 50px;
  width: 100%; /* Ajuster la largeur du wrapper */
}

.graph-wrapper3 img {
  width: 100%; /* Ajuster la taille de l'image pour remplir le wrapper */
  height: auto;
  display: block; /* Assurer que l'image est bien affichée en bloc */
}

.graph-wrapper3 p {
  text-align: center;
  padding: 10px;
  margin: 0;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  font-size: 16px;
  background-color: white;
  color: black;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  border-radius:10px;
  border:2px solid black;
}

button:hover {
  background-color: red;
  color: white;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
