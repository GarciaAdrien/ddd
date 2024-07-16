<template>
  <div class="login-page">
    <main>
      <section id="Connexion" class="login-section">
        <h2>Se connecter à votre compte</h2>
        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" required>
          </div>
          <div class="form-group">
            <label for="password">Mot de passe</label>
            <input type="password" id="password" v-model="password" required>
          </div>
          <button v-if="!isLoggedIn" type="submit">Se connecter</button>
          <button v-if="isLoggedIn" class="buttonlogout" @click="logout">Déconnexion</button>
        </form>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      isLoggedIn: localStorage.getItem('isLoggedIn') === 'true' // Check login status from localStorage
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ 
            us_login: this.email,
            password: this.password
          })
        });

        const responseData = await response.json();

        if (response.ok) {
          localStorage.setItem('isLoggedIn', true);
          localStorage.setItem('accessIds', JSON.stringify(responseData.access_ids));
          this.isLoggedIn = true;
          location.reload(); // Refresh to update navigation
        } else {
          alert('Erreur de connexion: ' + responseData.message);
        }
      } catch (error) {
        console.error('Erreur:', error);
        alert('Une erreur est survenue lors de la connexion.');
      }
    },
    logout() {
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('accessIds');
      this.isLoggedIn = false;
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.login-page {
  font-family: Arial, sans-serif;
  background-color: #f7f7f7;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('../assets/pc.jpg');
  background-size:contain; /* Ajuster la taille pour couvrir toute la zone */
  background-position: center; /* Centrer l'image */
}

.login-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: 0 auto; /* Pour centrer horizontalement */
}

.login-section h2 {
  color: #333;
  font-size: 1.8em;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Pour inclure le padding et border dans la largeur */
}

button {
    background: linear-gradient(to right, #ff8a00, #e52e71);
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 1em;
  cursor: pointer;
  width: 100%;
  margin-top: 10px;
}

button:hover {
    transform: scale(1.1);
}
</style>