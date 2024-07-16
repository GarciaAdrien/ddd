<template>
    <div class="login-page">
      <header>
        <nav>
          <ul>
            <li><a href="#Connexion">Se connecter</a></li>
            <li><a href="#Inscription">S'inscrire</a></li>
            <li><a href="#ForgotPassword">Mot de passe oublié</a></li>
          </ul>
        </nav>
      </header>
  
      <main>

        <!-- Section de Mot de passe oublié -->
        <section id="ForgotPassword" class="forgot-password-section">
          <h2>Mot de passe oublié ?</h2>
          <p>Entrez votre adresse email pour réinitialiser votre mot de passe.</p>
          <form @submit.prevent="resetPassword">
            <div class="form-group">
              <label for="reset-email">Email</label>
              <input type="email" id="reset-email" v-model="resetEmail" required>
            </div>
            <button type="submit">Réinitialiser</button>
          </form>
        </section>
      </main>
    </div>
  </template>
  
  
  <script>
  export default {
    name: 'forgot-password'
  }
  </script>
  
  <style scoped>
  /* Styles spécifiques à cette page */
  .login-page {
    font-family: Arial, sans-serif;
    background-color: #f7f7f7;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  header {
    width: 100%;
    background-color: #fff;
    padding: 10px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    text-align: center;
  }
  
  nav ul li {
    display: inline;
    margin-right: 10px;
  }
  
  nav ul li a {
    color: #333;
    text-decoration: none;
    font-weight: bold;
    font-size: 1.1em;
  }
  
  nav ul li a:hover {
    color: #6b4eff;
  }
  
  main {
    max-width: 600px;
    margin-top: 20px;
  }
  
  .login-section, .signup-section, .forgot-password-section {
    background-color: #fff;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .login-section h2, .signup-section h2, .forgot-password-section h2 {
    color: #333;
    font-size: 1.8em;
    margin-bottom: 10px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    color: #555;
  }
  
  input[type="email"], input[type="password"] {
    width: 100%;
    padding: 10px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    background-color: #6b4eff;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    font-size: 1em;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #5c3db7;
  }
  </style>
   
