<template>
  <div class="app">
    <div class="chart-container">
      <div class="graph-wrapper">
        <canvas id="commercialChart" ref="commercialChart"></canvas>
      </div>
      <div class="graph-wrapper">
        <canvas id="commercialChart2" ref="commercialChart2"></canvas>
      </div>

    </div>
    <div class="graph-wrapper2">
        <canvas id="satisfactionChart" ref="satisfactionChart"></canvas>
      </div>
    <div v-if="loading" class="loading-spinner">
      <div class="loader"></div>
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
    };
  },
  mounted() {
    this.fetchCommercialChart();
    this.fetchCommercialChart2();
    this.fetchSatisfactionChart();
  },
  methods: {
    fetchCommercialChart() {
      axios.get('http://localhost:5000/get_graph_commercial')
        .then(response => {
          this.renderCommercialChart(response.data);
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching commercial chart:', error);
          this.loading = false;
        });
    },
    fetchCommercialChart2() {
      axios.get('http://localhost:5000/get_graph_commercial2')
        .then(response => {
          this.renderCommercialChart2(response.data);
          this.loading = false;
        })
        .catch(error => {
          console.error('Error fetching second commercial chart:', error);
          this.loading = false;
        });
    },
    fetchSatisfactionChart() {
      axios.get('http://localhost:5000/get_satisfaction_by_category')
        .then(response => {
          this.renderSatisfactionChart(response.data);
        })
        .catch(error => {
          console.error('Error fetching satisfaction chart:', error);
          this.loading = false;
        });
    },
    renderCommercialChart(data) {
      const ctx = this.$refs.commercialChart.getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: data.datasets[0].label,
            backgroundColor: data.datasets[0].backgroundColor,
            borderColor: data.datasets[0].borderColor,
            borderWidth: data.datasets[0].borderWidth,
            data: data.datasets[0].data,
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Nombre d\'items vendus par catégorie',
              font: {
                size: 18
              }
            }
          }
        }
      });
    },
    renderCommercialChart2(data) {
      const ctx = this.$refs.commercialChart2.getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: data.datasets[0].label,
            backgroundColor: data.datasets[0].backgroundColor,
            borderColor: data.datasets[0].borderColor,
            borderWidth: data.datasets[0].borderWidth,
            data: data.datasets[0].data,
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Coût moyen de stockage par unité vendue',
              font: {
                size: 18
              }
            }
          }
        }
      });
    },
    renderSatisfactionChart(data) {
    const ctx = this.$refs.satisfactionChart.getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Satisfaction Scores',
                backgroundColor: data.colors,  // Use colors from API response
                data: data.scores,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Score de satisfaction par catégorie',
                    font: {
                size: 18
              }
                }
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        let label = data.labels[tooltipItem.index] || '';
                        if (label) {
                            label += ': ';
                        }
                        const score = data.datasets[0].data[tooltipItem.index];
                        if (score >= 4.0) {
                            label += 'Bon';
                        } else if (score >= 3.0) {
                            label += 'Moyen';
                        } else {
                            label += 'Mauvais';
                        }
                        return label;
                    }
                }
            }
        }
    });
}
  }
}
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

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.chart-container {
  text-align: center;
  width: 100%;
  display: -webkit-inline-box;
  margin-top:50px;
}

.graph-wrapper {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
  width: 100%;
  max-width: 800px; /* Example max-width to control width based on your layout */
  margin-left: auto;
  margin-right: auto;
  height:100%
}
.graph-wrapper {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
  width: 100%;
  max-width: 800px; /* Example max-width to control width based on your layout */
  margin-left: auto;
  margin-right: auto;
  height:100%
}
.graph-wrapper2 {
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  height:100%;
  margin-left: auto;
  margin-right: auto;

}

canvas {
  width: 100%;
}

.graph-wrapper p {
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
}

button:hover {
  transform: scale(1.1);
}
#satisfactionChart {
  display: flex;
    left: 44%;
    justify-content: center;
    position: relative;


}
</style>
