# my-beautiful-shop

![image](https://github.com/user-attachments/assets/49098bd5-54b5-454b-a1fd-6a7e12fd07fd)
![image](https://github.com/user-attachments/assets/31f98df4-9042-483e-b767-7839f213bc61)



## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Modification de la base de données Postgres 
```
Edition init_db config
```

### Création de la base de données
```
node init_db.js   
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# ESGI - Dashboard DDD |M2 AL
Adrien Garcia / Clément Deborde

## Description

Ce projet est une application web permettant de gérer des tableaux de bord spécifiques pour différents rôles d'utilisateur : commerce, direction, comptable et administrateur. L'objectif est de visualiser l'impact économique du stockage et/ou de l'expédition en direct pour divers produits d'une plateforme commerciale.
## Technologies Utilisées

- **Backend** : Python
- **Frontend** : VueJS
- **Base de Données** : PostgreSQL

## Fonctionnement

### Étape 1 : Création et Insertion des Données
- Créer une base postgres et modifiez init_db selon les informations de votre BDD précédemment créer
- Exemple :
    user: 'postgres',
    host: 'localhost',
    password: '0804', // Remplacez par votre mot de passe PostgreSQL
    port: 5433, // Port de votre PostgreSQL
    database: 'postgres' // Remplacez par le nom de votre base de données 
- Exécutez le script SQL pour créer et insérer les données dans une table `t_users`. Cette table permettra la connexion des utilisateurs sur le frontend.
- t_access permet de creer des accès spécifiques pour chaque dashboard
- t_user_acces permet aux users d'avoir accès a ces dashboards

### Étape 2 : Lancement du back
- Telecharger toutes les bibliothèques python utiles au projet : 
Exemple : cd C:\Users\Adrien\Desktop\ddd\my-beautiful-shop
  pip install -r requirements.txt

- Executer script.py via l'invité de commandes cmd 
Exemple : cd C:\Users\Adrien\Desktop\ddd\my-beautiful-shop
          python script.py 

### Étape 3 : Lancement de l'Application

- **Démarrer le Frontend** : Lancez l'application VueJS, qui s'occupera d'éxécuter une instance du backend. Le backend permet la récuperation des données CSV utilisés par les graphiques.

### Étape 4 : Connexion des Utilisateurs

Depuis le front, on se connecte avec l'un des 4 utilisateurs suivants :

- **Commerce**
  - Login: `commerce@esgi.fr`
  - Mot de passe: `commerce`

- **Direction**
  - Login: `direction@esgi.fr`
  - Mot de passe: `direction`

- **Comptable**
  - Login: `comptable@esgi.fr`
  - Mot de passe: `comptable`

- **Super Admin**
  - Login: `admin@esgi.fr`
  - Mot de passe: `admin`

  chaque utilisateur peut acceder a son propre tableau de bord, propre a sa section, excepté `admin`, qui a acces a tout les dashboards.

### Étape 5 : Utilisation de l'Application

1. **Tableaux de Bord Spécifiques** : Chaque compte accède à ses propres tableaux de bord, qu'il peut alors explorer et exploiter au travers de diférents graphiques.
2. **Page de Récupération des Données** : ommun a tous les compte, il permet d'avoir le CSV renvoyer par le backend, mais aussi de rappeler le backend pour mettre à jour les données ou de les télécharger.
