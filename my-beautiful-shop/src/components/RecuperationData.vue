<template>
  <div :class="{ 'recuperation-data': true, 'data-not-loaded': !dataLoaded }">
    <!-- Bouton pour recharger les données -->
    <div class="reload-button-wrapper">
      <button @click="reloadData">Recharger les données</button>
    </div>

    <div v-if="!dataLoaded && processing" class="loading-spinner">
      <div class="loader"></div>
      <p class="white">Chargement en cours...</p>
    </div>
    
    <!-- Data table -->
    <div class="table-wrapper" v-if="dataLoaded">
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="(column, index) in columns" :key="index">{{ column }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="paginatedData.length === 0">
            <td :colspan="columns.length">Aucune donnée disponible.</td>
          </tr>
          <tr v-else v-for="(row, rowIndex) in paginatedData" :key="rowIndex">
            <td v-for="(value, colIndex) in row" :key="colIndex">{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Pagination -->
    <div class="pagination" v-if="totalPages > 1">
      <button v-for="pageNumber in displayedPages" :key="pageNumber" @click="changePage(pageNumber)">
        {{ pageNumber }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecuperationData',
  data() {
    return {
      dataLoaded: false,
      processing: false,
      data: [],
      columns: [],
      currentPage: 1,
      itemsPerPage: 10,
      maxDisplayedPages: 10
    };
  },
  computed: {
    paginatedData() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return this.data.slice(startIndex, startIndex + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.data.length / this.itemsPerPage);
    },
    displayedPages() {
      const totalPages = this.totalPages;
      const currentPage = this.currentPage;
      const maxDisplayedPages = this.maxDisplayedPages;

      let startPage = 1;
      let endPage = totalPages;

      if (totalPages > maxDisplayedPages) {
        const halfMaxDisplayedPages = Math.floor(maxDisplayedPages / 2);
        startPage = currentPage - halfMaxDisplayedPages;
        endPage = currentPage + halfMaxDisplayedPages;

        if (startPage < 1) {
          startPage = 1;
          endPage = maxDisplayedPages;
        }

        if (endPage > totalPages) {
          endPage = totalPages;
          startPage = totalPages - maxDisplayedPages + 1;
        }
      }

      return Array.from({ length: endPage - startPage + 1 }, (_, index) => startPage + index);
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.processing = true;
      fetch('http://localhost:5000/fetch_csv', {
        method: 'GET',
        headers: {
          'Content-Type': 'text/csv',
        },
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('La réponse du réseau n\'est pas valide');
        }
        return response.text();
      })
      .then(csv => {
        const rows = csv.split('\n').map(line => line.split(';'));
        this.columns = rows[0].slice(0, 10);
        this.data = rows.slice(1).map(row => row.slice(0, 10));
        this.$nextTick(() => {
          this.dataLoaded = true;
          this.processing = false;
        });
      })
      .catch(error => {
        console.error('Erreur lors de la récupération des données:', error);
        this.processing = false;
      });
    },
    changePage(pageNumber) {
      this.currentPage = pageNumber;
    },
    reloadData() {
      this.dataLoaded = false;
      this.processing = true;
      this.data = [];
      this.columns = [];
      this.currentPage = 1;
      fetch('http://localhost:5000/execute_script', {
        method: 'POST',
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          this.fetchData();
          this.$router.push('/RecuperationData');
        } else {
          throw new Error(data.message);
        }
      })
      .catch(error => {
        console.error('Erreur lors du rechargement des données:', error);
        this.processing = false;
      });
    }
  }
};
</script>


<style>
/* Styles pour le composant */
.recuperation-data {
  color: #333; /* Couleur du texte principale */
  background-color: #f9f9f9; /* Fond légèrement teinté */
  padding: 20px; /* Espacement intérieur */
  border-radius: 8px; /* Bordures arrondies */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Ombre légère */
}

.data-not-loaded {
  background-color: #f9f9f9; /* Fond légèrement teinté lorsque les données ne sont pas chargées */
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.data-table th, .data-table td {
  border: 1px solid #ddd;
  padding: 12px; /* Espacement uniforme */
  min-width: 100px; /* Ajustez selon vos besoins */
  white-space: nowrap; /* Empêche le texte de se couper */
  text-align: left;
}

.data-table th {
  background-color: #f2f2f2;
  font-size: 16px;
  font-weight: bold; /* Texte en gras pour les entêtes */
  padding: 14px; /* Espacement ajusté */
}

.no-data {
  text-align: center;
  margin-top: 20px;
  font-style: italic; /* Style italique pour le message "Aucune donnée disponible." */
  color: #888; /* Couleur de texte plus légère */
}

.pagination {
  text-align: center;
  margin-top: 20px; /* Espacement entre le tableau et la pagination */
}

.pagination button {
  margin: 0 5px; /* Espacement des boutons */
  padding: 8px 16px; /* Espacement intérieur des boutons */
  cursor: pointer;
  background-color: #f2f2f2;
  border: 1px solid #ddd;
  border-radius: 4px; /* Bordures arrondies pour les boutons */
  transition: background-color 0.3s ease; /* Transition douce pour le changement de couleur au survol */
}

.pagination button:hover {
  background-color: #ddd; /* Couleur de fond au survol */
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

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.white {
  color: white;
  font-size: 20px;
}

.table-wrapper {
  width: 100%;
  overflow-x: auto;
  padding: 20px; /* Espacement intérieur ajusté */
  border-radius: 8px; /* Bordures arrondies */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Légère ombre pour un effet flottant */
  margin-top: 80px;
}

.reload-button-wrapper {
  position: absolute;
  left: 50%;
  right: 50%;
  top: 60px;

  justify-content: center;
}

.reload-button-wrapper button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: rgb(244, 146, 146);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.reload-button-wrapper button:hover {
  background-color: white;
}
</style>
