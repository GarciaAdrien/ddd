<template>
  <div id="app">

    <nav class="navbar">
      <div class="navbar-brand">
        <h1>
          <span class="breathing-letter">B</span>
          <router-link to="/" class="title no-underline">eautyShop</router-link>
        </h1>
      </div>
      <div class="navbar-menu">
        <div class="navbar-start">
          <router-link v-if="isLoggedIn && canAccess(1)" to="/DashboardCommercial" class="navbar-item" style="margin-left: 20px;">Dashboard Commercial</router-link>
          <router-link v-if="isLoggedIn && canAccess(2)" to="/DashboardComptable" class="navbar-item" style="margin-left: 20px;">Dashboard Comptable</router-link>
          <router-link v-if="isLoggedIn && canAccess(3)" to="/DashboardDirection" class="navbar-item dashboard-direction" style="margin-left: 20px;">Dashboard Direction</router-link>
          <router-link v-if="isLoggedIn" to="/RecuperationData" class="navbar-item" style="margin-left: 20px;">Récupération des données</router-link>
          <router-link to="/" class="navbar-item" style="margin-left: 20px;">Accueil</router-link>          
          <div class="profile-menu">
            <router-link v-if="isLoggedIn" @click="logout" to="/" class="profil-item navbar-item">Déconnexion</router-link>
            <router-link v-else to="/Connexion" class="profil-item">Se connecter</router-link>
          </div>
        </div>
      </div>
    </nav>

    <router-view />

    <div class="mask"></div>
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 BeautyShop. Tous droits réservés.</p>
      </div>

    </footer>

  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: localStorage.getItem('isLoggedIn') === 'true',
      accessIds: JSON.parse(localStorage.getItem('accessIds')) || []
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('accessIds');
      this.isLoggedIn = false;
      this.accessIds = [];
      this.$router.push('/');
    },
    canAccess(accessId) {
      return this.accessIds.includes(accessId);
    }
  }
};
</script>

<style scoped>
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
}
.mask {
  position: fixed;


  background-color: rgba(0, 0, 0, 0.5); /* Opacité grise */
  width: 100%; /* Largeur maximale */
  max-width: 100%;
  height: 100%; /* Hauteur de 300px */

  z-index: 999; /* Au-dessus de tout le contenu */
  opacity: 0.3;
  animation: fadeIn 1s forwards;
  backdrop-filter: blur(100px); /* Effet de flou */
}

.footer {
  background: linear-gradient(to right, #ff8a00, #e52e71);
  height: 30px;
  width: 100%;
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 1000;
  border-radius:8px;
}

.footer-content {
  max-width: 1200px; /* Par exemple, pour limiter la largeur du contenu */
  margin: 0 auto;
  padding: 5px 20px; /* Ajustez le padding selon vos besoins */
  color: white;
  text-align: center;
}

/* Styles pour le texte du footer */
.footer p {
  margin: 0;
}
.navbar {
  background: linear-gradient(to right, #ff8a00, #e52e71);
  width: 97.8%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  position: fixed;
  top: 0;
  height:20px;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.navbar-brand h1 {
  display: flex;
  align-items: center;
}

.title {
  color: white;
}

.navbar-start {
  display: flex;
  align-items: center;
}

.navbar-item {
  color: #fff;
  padding: 15px 20px;
  text-decoration: none;
  border-radius: 6px;
  box-shadow: 0 2px 2px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.2s ease;
}
.profil-item {
  color:white;
  padding: 15px 20px;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}
button {

  color:white;
  padding: 15px 20px;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.3s ease, transform 0.2s ease;

}
.profil-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: scale(1.1);
}
.navbar-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: scale(1.1);
}

.dashboard-direction {
  margin-left: 20px; /* Espacement à gauche */
  margin-right: 20px; /* Espacement à droite */
}

.profile-menu {
  display: flex;
  align-items: center;
  position: relative;
  margin-right: 50px;
  color: white;
  border-radius: 8px;
  font-size: 16px;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin-left: 20px; 
}








@media (max-width: 768px) {
  .navbar-menu {
    display: none;
  }

  .navbar-start {
    flex-direction: column;
    position: absolute;
    top: 40px;
    width: 100%;
    background: linear-gradient(to right, #ff8a00, #e52e71);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    transform-origin: top;
    transform: scaleY(0);
    transition: transform 0.3s ease;
    z-index: 999;
  }

  .navbar-start {
    transform: scaleY(1);
  }

  .navbar-item {
    padding: 12px 40px;
    margin-left: 0; /* Réinitialiser la marge à gauche */
  }

  .profile-options {
    top: 100%;
    right: 0;
  }
}

@keyframes breathe {
  0%, 100% {
    font-size: 20px;
  }

  50% {
    font-size: 24px;
  }
}

.breathing-letter {
  animation: breathe 3s infinite;
  color: white;
}

.no-underline {
  text-decoration: none; /* Enlève le soulignement */
}
</style>
