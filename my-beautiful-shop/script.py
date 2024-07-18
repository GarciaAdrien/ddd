import pandas as pd
import psycopg2
import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from io import BytesIO
import matplotlib
import seaborn as sns

matplotlib.use('Agg')  # Utiliser le backend 'Agg' de Matplotlib

import matplotlib.pyplot as plt
import io


app = Flask(__name__)
CORS(app, resources={r"/fetch_csv": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/login": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/execute_script": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_commercial": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_commercial2": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_comptable3": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_comptable2": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_comptable1": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_direction2": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_direction1": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_satisfaction_by_category": {"origins": "http://localhost:8080"}})

db_connection = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='0804',
    host='localhost',
    port='5433'
)

def charger_donnees(lChemin_dossier):
    dfs = []
    for lFichier in os.listdir(lChemin_dossier):
        if lFichier.endswith('.csv'):
            lChemin_fichier = os.path.join(lChemin_dossier, lFichier)
            lNom_dataframe = lFichier.split('.')[0]
            df = pd.read_csv(lChemin_fichier)
            dfs.append((lNom_dataframe, df))
    return dfs
    
def generate_direction_data1(dataframe_final_filtered):
    try:
        # Conversion 'order_purchase_timestamp' en datetime si nécessaire
        dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

        # Grouper par mois et compter le nombre de commandes
        orders_by_month = dataframe_final_filtered.groupby(dataframe_final_filtered['order_purchase_timestamp'].dt.to_period('M')).size()

        # Préparer les données pour Chart.js
        labels = orders_by_month.index.strftime('%Y-%m').tolist()  # Convert Index to list
        data = orders_by_month.values.tolist()  # Valeurs de nombre de commandes

        return {
            'labels': labels,
            'data': data
        }

    except Exception as e:
        print(f"Erreur lors de la génération des données pour Direction 1 : {str(e)}")
        return None

        
@app.route('/get_graph_direction1', methods=['GET'])
def get_direction_data1():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_final_filtered = pd.read_csv(chemin_excel, sep=';')

        data = generate_direction_data1(dataframe_final_filtered)
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Données non disponibles'}), 500

    except Exception as e:
        print(f"Erreur lors de la récupération des données pour Direction 1 : {str(e)}")
        return jsonify({'error': 'Données non disponibles'}), 500

def generate_direction_data2(dataframe_final_filtered):
    try:
        # Conversion 'order_purchase_timestamp' en datetime si nécessaire
        dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

        # Filtrage des données pour le mois de juillet 2018
        data_july_2018 = dataframe_final_filtered[(dataframe_final_filtered['order_purchase_timestamp'].dt.year == 2018) &
                                                  (dataframe_final_filtered['order_purchase_timestamp'].dt.month == 7)]

        # Ajout de la colonne 'jour_du_mois' pour le jour du mois
        data_july_2018['jour_du_mois'] = data_july_2018['order_purchase_timestamp'].dt.day

        # Comptage du nombre de commandes pour chaque jour du mois et catégorie de produits
        orders_by_day_and_category = data_july_2018.groupby(['jour_du_mois', 'product_category_name_english']).size().reset_index(name='nombre_commandes')

        # Création de la pivot table
        pivot_table = orders_by_day_and_category.pivot_table(index='jour_du_mois', columns='product_category_name_english', values='nombre_commandes', aggfunc='sum', fill_value=0)

        # Réindexer pour inclure tous les jours de 1 à 31
        pivot_table = pivot_table.reindex(range(1, 32), fill_value=0)

        # Préparer les données pour Chart.js
        labels = pivot_table.index.tolist()  # Jours du mois
        categories = pivot_table.columns.tolist()  # Catégories de produits
        data = pivot_table.values.tolist()  # Valeurs de nombre de commandes sous forme de liste de listes

        return {
            'labels': labels,
            'datasets': [{
                'label': category,
                'data': [data[i][j] for i in range(len(labels))]  # Récupérer les données par jour
            } for j, category in enumerate(categories)]
        }

    except Exception as e:
        print(f"Erreur lors de la génération des données pour Direction 2 : {str(e)}")
        return None




@app.route('/get_graph_direction2', methods=['GET'])
def get_direction_data2():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_final_filtered = pd.read_csv(chemin_excel, sep=';')

        data = generate_direction_data2(dataframe_final_filtered)
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Données non disponibles'}), 500

    except Exception as e:
        print(f"Erreur lors de la récupération des données pour Direction 2 : {str(e)}")
        return jsonify({'error': 'Données non disponibles'}), 500

def generate_commercial_graph_data():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_fusionne = pd.read_csv(chemin_excel, sep=';')
        
        # Affichage des premières lignes du dataframe pour vérifier le contenu
        print(dataframe_fusionne.head())
        
        if 'product_category_name_english' in dataframe_fusionne.columns:
            top_categories = dataframe_fusionne['product_category_name_english'].value_counts().head(10)
            
            data = {
                'labels': top_categories.index.tolist(),
                'datasets': [{
                    'label': 'Nombre d\'items vendus',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 1,
                    'data': top_categories.values.tolist()
                }]
            }
            return data
        else:
            print("La colonne 'product_category_name_english' n'existe pas dans le dataframe.")
            return None
    except Exception as e:
        print(f"Erreur lors de la génération des graphiques commerciaux : {str(e)}")
        return None

@app.route('/get_graph_commercial', methods=['GET'])
def get_graph_commercial_data():
    data = generate_commercial_graph_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Graphique non disponible'}), 500

def generate_commercial_graph2_data():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_final_filtered = pd.read_csv(chemin_excel, sep=';')

        dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

        def jours_ecoules_debut_mois(date):
            premier_jour_mois = date.replace(day=1)
            return (date - premier_jour_mois).days + 1

        dataframe_final_filtered['jours_ecoules_debut_mois'] = dataframe_final_filtered['order_purchase_timestamp'].apply(jours_ecoules_debut_mois)

        nombre_d_unites_vendues_par_produit = dataframe_final_filtered.groupby('product_id')['order_item_id'].sum().reset_index()

        dataframe_final_filtered['price_storage_total'] = dataframe_final_filtered['price_storage_per_day'] * dataframe_final_filtered['jours_ecoules_debut_mois']
        dataframe_final_filtered['coût_stockage_par_unité'] = dataframe_final_filtered['price_storage_total'] / nombre_d_unites_vendues_par_produit['order_item_id']

        cost_data = dataframe_final_filtered.groupby('product_category_name_english')['coût_stockage_par_unité'].mean().reset_index()

        data = {
            'labels': cost_data['product_category_name_english'].tolist(),
            'datasets': [{
                'label': 'Coût moyen de stockage par unité vendue',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1,
                'data': cost_data['coût_stockage_par_unité'].tolist()
            }]
        }
        return data
    except Exception as e:
        print(f"Erreur lors de la génération du graphique commercial 2 : {str(e)}")
        return None

@app.route('/get_graph_commercial2', methods=['GET'])
def get_graph_commercial2_data():
    data = generate_commercial_graph2_data()
    if data:
        return jsonify(data)
    else:
        return jsonify({'error': 'Graphique non disponible'}), 500

@app.route('/get_satisfaction_by_category', methods=['GET'])
def get_satisfaction_by_category():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_final_filtered = pd.read_csv(chemin_excel, sep=';')

        # Calculer la moyenne de satisfaction par catégorie
        satisfaction_by_category = dataframe_final_filtered.groupby('product_category_name_english')['review_score'].mean().reset_index()

        # Préparer les données pour Vue Chart.js
        labels = satisfaction_by_category['product_category_name_english'].tolist()
        scores = satisfaction_by_category['review_score'].tolist()
        
        # Generate colors dynamically
        num_categories = len(labels)
        colors = generate_chart_colors(num_categories)

        data = {
            'labels': labels,
            'scores': scores,
            'colors': colors  # Include colors in the response
        }

        return jsonify(data)
    
    except Exception as e:
        print(f"Erreur lors de la récupération de la satisfaction par catégorie : {str(e)}")
        return jsonify({'error': 'Données non disponibles'}), 500

def generate_chart_colors(num_colors):
    # Example function to generate random colors or use a predefined color palette
    # This should generate num_colors number of colors
    # You can modify this function based on your color requirements
    import random
    return ['#' + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(num_colors)]

# Route pour le premier graphique
@app.route('/get_graph_comptable1', methods=['GET'])
def get_graph_comptable1():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_final_filtered = pd.read_csv(chemin_excel, sep=';')

        # Manipulation des données et calculs
        dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

        def jours_ecoules_debut_mois(date):
            premier_jour_mois = date.replace(day=1)
            return (date - premier_jour_mois).days + 1

        dataframe_final_filtered['jours_ecoules_debut_mois'] = dataframe_final_filtered['order_purchase_timestamp'].apply(jours_ecoules_debut_mois)

        dataframe_final_filtered['price_storage_total'] = dataframe_final_filtered['price_storage_per_day'] * dataframe_final_filtered['jours_ecoules_debut_mois']
        dataframe_final_filtered['prix_total'] = dataframe_final_filtered['price'] + dataframe_final_filtered['price_storage_total'] + dataframe_final_filtered['price_delivery']
        dataframe_final_filtered['marge_brute'] = dataframe_final_filtered['prix_total'] - (dataframe_final_filtered['price_storage_total'] + dataframe_final_filtered['price_delivery'] + dataframe_final_filtered['price_storage_per_day'])

        top_categories = dataframe_final_filtered['product_category_name_english'].value_counts().head(10).index
        df_top_categories = dataframe_final_filtered[dataframe_final_filtered['product_category_name_english'].isin(top_categories)]
        df_plot_marge_brute = df_top_categories.groupby('product_category_name_english')['marge_brute'].sum().reset_index()
        # Préparation des données pour le graphique
        data = {
            'labels': list(df_plot_marge_brute['product_category_name_english']),
            'values': list(df_plot_marge_brute['marge_brute'])
        }

        return jsonify(data)

    except Exception as e:
        print(f"Erreur lors de la génération du graphique comptable 1 : {str(e)}")
        return jsonify({'error': 'Graphique non disponible'}), 500

# Route pour le deuxième graphique
@app.route('/get_graph_comptable2', methods=['GET'])
def get_graph_comptable2():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_final_filtered = pd.read_csv(chemin_excel, sep=';')

        nombre_d_unites_vendues_par_produit = dataframe_final_filtered.groupby('product_id')['order_item_id'].sum().reset_index()
        dataframe_final_filtered['coût_stockage_par_unité'] = dataframe_final_filtered['price_storage_total'] / nombre_d_unites_vendues_par_produit['order_item_id']

        df_plot_cout_stockage = dataframe_final_filtered.groupby('product_category_name_english')['coût_stockage_par_unité'].mean().reset_index()

        # Préparation des données pour le graphique
        data = {
            'labels': list(df_plot_cout_stockage['product_category_name_english']),
            'values': list(df_plot_cout_stockage['coût_stockage_par_unité'])
        }

        return jsonify(data)

    except Exception as e:
        print(f"Erreur lors de la génération du graphique comptable 2 : {str(e)}")
        return jsonify({'error': 'Graphique non disponible'}), 500

@app.route('/get_graph_comptable3', methods=['GET'])
def get_graph_comptable3():
    try:
        chemin_excel = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        dataframe_final_filtered = pd.read_csv(chemin_excel, sep=';')

        dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])
        dataframe_final_filtered['jours_ecoules_debut_mois'] = dataframe_final_filtered['order_purchase_timestamp'].apply(lambda date: (date - date.replace(day=1)).days + 1)

        dataframe_final_filtered['price_storage_total'] = dataframe_final_filtered['price_storage_per_day'] * dataframe_final_filtered['jours_ecoules_debut_mois']
        dataframe_final_filtered['prix_total'] = dataframe_final_filtered['price'] + dataframe_final_filtered['price_storage_total'] + dataframe_final_filtered['price_delivery']

        dataframe_final_filtered = dataframe_final_filtered.rename(columns={
            'price_storage_total': 'Charges',
            'prix_total': 'Prix total',
            'price': 'Prix du produit'
        })

        # Calcul des gains sur le produit
        dataframe_final_filtered['Gains'] = dataframe_final_filtered['Prix total'] - (dataframe_final_filtered['Charges'] + dataframe_final_filtered['Prix du produit'])

        top_categories = dataframe_final_filtered['product_category_name_english'].value_counts().head(10).index
        dataframe_top_categories = dataframe_final_filtered[dataframe_final_filtered['product_category_name_english'].isin(top_categories)]

        df_plot = dataframe_top_categories.melt(id_vars='product_category_name_english',
                                                value_vars=['Charges', 'Prix total', 'Prix du produit', 'Gains'],  # Ajout de 'Gains'
                                                var_name='cost_type',
                                                value_name='cost_value')

        # Préparation des données pour le graphique
        data = {
            'labels': list(df_plot['product_category_name_english'].unique()),
            'datasets': []
        }
        max_value = 1000
        for cost_type, color in zip(df_plot['cost_type'].unique(), ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)']):  # Ajout de couleur pour 'Gains'
            # Ajout de cette ligne pour définir `dataset_values`
            dataset_values = df_plot[df_plot['cost_type'] == cost_type]['cost_value'].tolist()
            dataset_values = [min(value, max_value) for value in dataset_values]
            data['datasets'].append({
                'label': cost_type,
                'data': dataset_values,
                'backgroundColor': color,
                'borderColor': color.replace('0.2', '1'),
                'borderWidth': 1
            })

        return jsonify(data)

    except Exception as e:
        print(f"Erreur lors de la génération du graphique comptable 3 : {str(e)}")
        return jsonify({'error': 'Graphique non disponible'}), 500



@app.route('/login', methods=['POST'])
def login():
    try:
        # Retrieve login credentials from request
        request_data = request.get_json()
        email = request_data.get('us_login')
        password = request_data.get('password')

        # Example: Querying the database for authentication
        cursor = db_connection.cursor()
        cursor.execute('''
            SELECT u.id_user, u.us_login, u.password, ua.id_access
            FROM t_users u
            JOIN user_access ua ON u.id_user = ua.id_user
            WHERE u.us_login = %s AND u.password = %s
        ''', (email, password))
        
        user_access_list = cursor.fetchall()
        cursor.close()

        if user_access_list:
            user_id, _, _, _ = user_access_list[0]  # Assume the first row for simplicity
            access_ids = [ua[3] for ua in user_access_list]  # Extract all id_access values
            
            return jsonify({'status': 'success', 'message': 'Connexion réussie', 'access_ids': access_ids})
        else:
            # Authentication failed
            return jsonify({'status': 'error', 'message': 'Identifiants Incorrects'}), 401

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/fetch_csv', methods=['GET'])
def fetch_csv():
    try:
        chemin_csv = r'.\Data Centric\\result\\donnees_fusion_result.csv'
        return send_file(chemin_csv, as_attachment=False)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/')
def index():
    return "Le serveur Flask fonctionne!"


@app.route('/execute_script', methods=['POST'])
def execute_script():
    try:
        # Chemins bruts pour éviter les erreurs d'échappement
        lChemin_Dossier = r'.\Data Centric\\archive\\'
        lChemin_Dossier_Result = r'.\Data Centric\\result\\'

        # Charger les données dans un seul dataframe
        donnees = charger_donnees(lChemin_Dossier)

        # Initialiser le premier dataframe
        nom_dataframe, dataframe_fusionne = donnees[0]

        # Fusionner les dataframes en mergeant sur les colonnes communes
        for nom_dataframe, df in donnees[1:]:
            colonnes_communes = [colonne for colonne in dataframe_fusionne.columns if colonne in df.columns]
            if colonnes_communes:
                dataframe_fusionne = pd.merge(dataframe_fusionne, df, on=colonnes_communes, how='left').drop_duplicates()
                chemin_sortie_fusion = os.path.join(lChemin_Dossier_Result, 'donnees_fusion_archive.csv')
                dataframe_fusionne.to_csv(chemin_sortie_fusion, index=False, sep=';')
            else:
                print(f"Aucune colonne commune entre {nom_dataframe} et le dataframe fusionné.")

        # Charger les données depuis le fichier Excel
        chemin_excel = r".\Data Centric\\frais_expedition\\price_logistical.xlsx"
        df_excel = pd.read_excel(chemin_excel)

        # Créer le dataframe final
        dataframe_final = pd.merge(dataframe_fusionne, df_excel, on='product_category_name_english', how='left')

        # Générer le nouveau fichier csv
        chemin_sortie_csv = os.path.join(lChemin_Dossier_Result, 'donnees_fusion_result.csv')

        # Filtrer les données et fusionner sur le poids des produits
        dataframe_final_filtered = dataframe_final[(dataframe_final['product_weight_g'] >= dataframe_final['min_weight'] * 1000) &
                                                   (dataframe_final['product_weight_g'] <= dataframe_final['max_weight'] * 1000)]

        # Convertir order_purchase_timestamp en datetime
        dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

        # Calculer le nombre de jours écoulés depuis le début du mois
        def jours_ecoules_debut_mois(date):
            premier_jour_mois = date.replace(day=1)
            return (date - premier_jour_mois).days + 1

        dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])
        dataframe_final_filtered['jours_ecoules_debut_mois'] = dataframe_final_filtered['order_purchase_timestamp'].apply(jours_ecoules_debut_mois)
        dataframe_final_filtered['price_storage_total'] = dataframe_final_filtered['price_storage_per_day'] * dataframe_final_filtered['jours_ecoules_debut_mois']
        dataframe_final_filtered['price_delivery_direct'] = dataframe_final_filtered['price_storage_total'] + dataframe_final_filtered['price_delivery']
        # Assurer que toutes les valeurs NaN sont converties en None (NULL) pour PostgreSQL
        dataframe_final_filtered = dataframe_final_filtered.where(pd.notnull(dataframe_final_filtered), None)

        # Nettoyage des sauts de ligne dans les cellules
        for col in dataframe_final_filtered.columns:
            if dataframe_final_filtered[col].dtype == 'object':
                dataframe_final_filtered[col] = dataframe_final_filtered[col].str.replace(r'\n', ' ', regex=True)
       
        dataframe_final_filtered.groupby('order_id').first().to_csv(chemin_sortie_csv, index=False, sep=';')
        return jsonify({'status': 'success', 'message': 'Traitement terminé'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
