<template>
  <div class="app">
    <div v-if="loading" class="loading-spinner">
      <div class="loader"></div>
      <p>Loading graphs...</p>
    </div>

    <div class="chart-container">
      <div class="chart-row">
        <!-- Chart 1 -->
        <div class="graph-wrapper">
          <canvas id="chart-1" ref="chart1"></canvas>
        </div>

        <!-- Chart 2 -->
        <div class="graph-wrapper">
          <canvas id="chart-2" ref="chart2"></canvas>
        </div>
      </div>

      <!-- Chart 3 (Full width) -->
      <div class="chart-row full-width">
        <div class="graph-wrapper full-width">
          <canvas id="chart-3" ref="chart3"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      loading: true,
      chartsData: {}
    };
  },
  mounted() {
    this.fetchChartData();
  },
  methods: {
    async fetchChartData() {
      try {
        const response1 = await axios.get('http://localhost:5000/get_graph_comptable1');
        const response2 = await axios.get('http://localhost:5000/get_graph_comptable2');
        const response3 = await axios.get('http://localhost:5000/get_graph_comptable3');

        // Assuming your API returns data in the format you expect
        this.chartsData = {
          chart1Data: response1.data,
          chart2Data: response2.data,
          chart3Data: response3.data
        };

        this.renderCharts();
        this.loading = false;
      } catch (error) {
        console.error('Error fetching data:', error);
        this.loading = false;
      }
    },
    renderCharts() {
      // Chart 1
      const ctx1 = this.$refs.chart1.getContext('2d');
      new Chart(ctx1, {
        type: 'bar', // Adjust based on your chart type (e.g., bar, line, pie)
        data: {
          labels: this.chartsData.chart1Data.labels,
          datasets: [{
            label: 'Marge Brute',
            data: this.chartsData.chart1Data.values,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }]
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Marge Brute',
              font: {
                size: 18
              }
            }
          }
        }
      });

      // Chart 2
      const ctx2 = this.$refs.chart2.getContext('2d');
      new Chart(ctx2, {
        type: 'bar', // Adjust based on your chart type
        data: {
          labels: this.chartsData.chart2Data.labels,
          datasets: [{
            label: 'Coût de Stockage par Unité',
            data: this.chartsData.chart2Data.values,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Coût de Stockage par Unité',
              font: {
                size: 18
              }
            }
          }
        }
      });

      // Chart 3
      const ctx3 = this.$refs.chart3.getContext('2d');
      new Chart(ctx3, {
        type: 'bar', // Adjust based on your chart type
        data: {
          labels: this.chartsData.chart3Data.labels,
          datasets: this.chartsData.chart3Data.datasets.map(dataset => ({
            label: dataset.label,
            data: dataset.data,
            backgroundColor: dataset.backgroundColor,
            borderColor: dataset.borderColor,
            borderWidth: dataset.borderWidth
          }))
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Moyenne des profits nets par vente et par catégorie de produit',
              font: {
                size: 18
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
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
  position: absolute;
  top: 50%;
  left: 45%;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loader {
  border: 4px solid rgba(255, 0, 0, 0.3);
  border-radius: 50%;
  border-top: 4px solid #fefefe;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  top: -120px;
}

.chart-container {
  text-align: center;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top:50px;
}

.chart-row {
  display: flex;
  justify-content: space-around;
  width: 100%;
  max-width: 1600px;
}

.graph-wrapper {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
  width: 48%; /* Adjust width for better spacing */
}

.graph-wrapper.full-width {
  width: 100%; /* Full width for the last chart */
}

canvas {
  width: 100%;
  height: auto;
}

.graph-wrapper p {
  text-align: center;
  padding: 10px;
  margin: 0;
}

</style>
