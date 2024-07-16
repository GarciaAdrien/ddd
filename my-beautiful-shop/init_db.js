const { Client } = require('pg');
const fs = require('fs');
const path = require('path');

// Configuration de connexion à PostgreSQL
const config = {
    user: 'postgres',
    host: 'localhost',
    password: '0804', // Remplacez par votre mot de passe PostgreSQL
    port: 5433, // Port de votre PostgreSQL
    database: 'postgres' // Remplacez par le nom de votre base de données
};

// Chemin vers le fichier SQL d'initialisation
const initSqlPath = path.join(__dirname, 'init_db.sql');

// Fonction pour lire et exécuter le script SQL
async function executeSqlScript() {
    const client = new Client(config);

    try {
        await client.connect(); // Se connecter à PostgreSQL
        console.log('Connexion à PostgreSQL réussie.');

        // Lire le contenu du fichier SQL d'initialisation
        const initSql = fs.readFileSync(initSqlPath, 'utf8');

        // Démarrer une transaction
        await client.query('BEGIN');

        // Exécuter chaque partie du script SQL séparément
        await client.query(initSql);

        // Valider la transaction
        await client.query('COMMIT');
        console.log('Script SQL exécuté avec succès.');

    } catch (err) {
        // En cas d'erreur, annuler la transaction
        await client.query('ROLLBACK');
        console.error('Erreur lors de l\'exécution du script SQL :', err);
    } finally {
        await client.end(); // Toujours fermer la connexion, même en cas d'erreur
        console.log('Connexion PostgreSQL fermée.');
    }
}

// Appeler la fonction pour exécuter le script SQL
executeSqlScript();
