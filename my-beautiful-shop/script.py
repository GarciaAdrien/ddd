import pandas as pd
import psycopg2
import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
CORS(app, resources={r"/fetch_csv": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/login": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/execute_script": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/get_graph_commercial": {"origins": "http://localhost:8080"}})

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

def generate_commercial_graphs():
    try:
        # Chargement des données commerciales spécifiques
        lChemin_Dossier = r'.\Data Centric\\archive\\'  # Adapter ce chemin selon vos données
        donnees = charger_donnees(lChemin_Dossier)

        # Exemple de traitement pour générer des graphiques (à adapter selon vos besoins)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot([1, 2, 3, 4], [10, 20, 25, 30], label='Ventes mensuelles')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Ventes')
        ax.set_title('Ventes Mensuelles par Mois')
        ax.legend()

        # Conversion du graphique en image
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        return buf

    except Exception as e:
        print(f"Erreur lors de la génération des graphiques commerciaux : {str(e)}")
        return None

@app.route('/get_graph_commercial', methods=['GET'])
def get_graph_commercial():
    try:
        # Générer les graphiques commerciaux
        graph_buffer = generate_commercial_graphs()

        if graph_buffer:
            return send_file(graph_buffer, mimetype='image/png')
        else:
            return jsonify({'status': 'error', 'message': 'Impossible de générer les graphiques commerciaux'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


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
