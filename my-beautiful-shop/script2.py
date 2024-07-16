import pandas as pd
import os
from functools import reduce
import seaborn as sns
import matplotlib.pyplot as plt 



#Récupération du dataframe 
def charger_dataframe(lChemin_fichier):
    return pd.read_csv(lChemin_fichier)

#Récupération des données depuis une liste de csv dans le répertoire
def charger_donnees(lChemin_dossier):
    dfs = []
    for lFichier in os.listdir(lChemin_dossier):
        if lFichier.endswith('.csv'):
            lChemin_fichier = os.path.join(lChemin_dossier, lFichier)
            lNom_dataframe = lFichier.split('.')[0]
            df= pd.read_csv(lChemin_fichier)
            dfs.append((lNom_dataframe, df))
    return dfs
    
if __name__ == "__main__":
    # Chemin du dossier contenant les fichiers CSV
    lChemin_Dossier = 'C:\\Users\\Adrien\\Desktop\\Jupyter\\Data Centric\\archive\\'
    lChemin_Dossier_Result = 'C:\\Users\\Adrien\\Desktop\\Jupyter\\Data Centric\\result\\'    
    
    # Recupération des données dans un seul dataframe
    donnees = charger_donnees(lChemin_Dossier)
    #print(donnees)        

    # Initialiser les csv
    nom_dataframe, dataframe_fusionne = donnees[0]
    
    # fusion des data frame en mergeant sur les colonnes communes
    for nom_dataframe, df in donnees[1:]:
        colonnes_communes = [colonne for colonne in dataframe_fusionne.columns if colonne in df.columns]
        if colonnes_communes:
            dataframe_fusionne = pd.merge(dataframe_fusionne, df, on=colonnes_communes, how='left').drop_duplicates()
            chemin_sortie_fusion = os.path.join(lChemin_Dossier_Result, 'donnees_fusion_archive.csv')
            dataframe_fusionne.to_csv(chemin_sortie_fusion, index=False, sep=';')       
        else: 
            print(f"Aucune colonne commune entre {nom_dataframe} et le dataframe fusionné.")
            
    # Chargement des données depuis le fichier Excel
    chemin_excel = "C:\\Users\\Adrien\\Desktop\\Jupyter\\Data Centric\\frais_expedition\\price_logistical.xlsx"
    df_excel = pd.read_excel(chemin_excel)    

    # Création du dataframe final
    dataframe_final = pd.merge(dataframe_fusionne, df_excel, on='product_category_name_english', how='left')
    # Génération du nouveau fichier csv
    chemin_sortie_csv = os.path.join(lChemin_Dossier_Result, 'donnees_fusion_result.csv')
    
    #Récupération des données filtrées  et merge sur le poid des produits
    dataframe_final_filtered = dataframe_final[(dataframe_final['product_weight_g'] >= dataframe_final['min_weight'] * 1000) & 
                                            (dataframe_final['product_weight_g'] <= dataframe_final['max_weight'] * 1000)]   
    #Conversion order purchase timestamp en datetime
    dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

    #Calcul du nombre de jours écoulés depuis le début du mois
    def jours_ecoules_debut_mois(date):
        premier_jour_mois = date.replace(day=1)
        return (date - premier_jour_mois).days + 1
    print(dataframe_final_filtered)

    dataframe_final_filtered['jours_ecoules_debut_mois'] = dataframe_final_filtered['order_purchase_timestamp'].apply(jours_ecoules_debut_mois)
    
    # Calcul price_storage_total en multipliant jours_ecoules_debut_mois par price_storage_per_day
    dataframe_final_filtered['price_storage_total'] = dataframe_final_filtered['price_storage_per_day'] * dataframe_final_filtered['jours_ecoules_debut_mois']
    dataframe_final_filtered['price_delivery_direct'] = dataframe_final_filtered['price_storage_total'] + dataframe_final_filtered['price_delivery']         
    dataframe_final_filtered.groupby('order_id').first().to_csv(chemin_sortie_csv, index=False, sep=';')


    # calcul du nombre de résultats uniques par colonne
    resultats = {}
    for colonne in dataframe_fusionne.columns:
        resultats[colonne] = dataframe_fusionne[colonne].value_counts()
    
    # TRI des résultats par ordre décroissant
    resultats_tries = {colonne: valeurs.sort_values(ascending=False) for colonne, valeurs in resultats.items()}
    
#Ce graph represente l'Estimation des catégories de produits les plus commandés


#Crée un graph blanc
sns.set(style="whitegrid")
# On récupère le nombre de produits les plus commandés 
colonne = "product_category_name"  
#On tri les résultats
valeurs = resultats_tries[colonne]  

#On se base sur les 10 plus grands nombres d'items vendu dans les différentes catégories
valeurs_top = valeurs.head(10)  
top_categories = dataframe_fusionne['product_category_name_english'].value_counts().head(10)


# Création d'un graphique en barres basé sur les items les plus vendus
plt.figure(figsize=(10, 6))  
barplot = sns.barplot(x=valeurs_top.index, y=valeurs_top.values, palette='viridis')  # Crée un barplot avec axes échangés
plt.title(f'Distribution des 10 catégories de produits les plus commandés')  # Titre du graphique
plt.xlabel('Catégories') 
plt.ylabel('Nombre de produits Commandés')  
plt.xticks(rotation=45) 
plt.show()  

# Récupération  des commandes par état
plt.figure(figsize=(12, 6))
sns.countplot(data=dataframe_fusionne, x='customer_state', palette='viridis')
plt.title('Répartition des commandes par région (état)')
plt.xlabel('Etat')
plt.ylabel('Nombre de commandes')
plt.xticks(rotation=45)
plt.show()


# Conversion la colonne 'order_purchase_timestamp' en datetime 
dataframe_fusionne['order_purchase_timestamp'] = pd.to_datetime(dataframe_fusionne['order_purchase_timestamp'])

# Grouper par mois et compter le nombre de commandes
orders_by_month = dataframe_fusionne.groupby(dataframe_fusionne['order_purchase_timestamp'].dt.to_period('M')).size()

# Graph évolution temporelle des commandes
plt.figure(figsize=(12, 6))
orders_by_month.plot(marker='o', linestyle='-', color='b')
plt.title('Evolution temporelle des commandes')
plt.xlabel('Mois')
plt.ylabel('Nombre de commandes')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

#Ce graph represente l'Estimation des catégories de produits les plus commandés


#Crée un graph blanc
sns.set(style="whitegrid")
# On récupère le nombre de produits les plus commandés 
colonne = "product_category_name"  
#On tri les résultats
valeurs = resultats_tries[colonne]  

#On se base sur les 10 plus grands nombres d'items vendu dans les différentes catégories
valeurs_top = valeurs.head(10)  
top_categories = dataframe_fusionne['product_category_name_english'].value_counts().head(10)


# Création d'un graphique en barres basé sur les items les plus vendus
plt.figure(figsize=(10, 6))  
barplot = sns.barplot(x=valeurs_top.index, y=valeurs_top.values, palette='viridis')  # Crée un barplot avec axes échangés
plt.title(f'Distribution des 10 catégories de produits les plus commandés')  # Titre du graphique
plt.xlabel('Catégories') 
plt.ylabel('Nombre de produits Commandés')  
plt.xticks(rotation=45) 
plt.show()  

# Récupération  des commandes par état
plt.figure(figsize=(12, 6))
sns.countplot(data=dataframe_fusionne, x='customer_state', palette='viridis')
plt.title('Répartition des commandes par région (état)')
plt.xlabel('Etat')
plt.ylabel('Nombre de commandes')
plt.xticks(rotation=45)
plt.show()


# Conversion la colonne 'order_purchase_timestamp' en datetime 
dataframe_fusionne['order_purchase_timestamp'] = pd.to_datetime(dataframe_fusionne['order_purchase_timestamp'])

# Grouper par mois et compter le nombre de commandes
orders_by_month = dataframe_fusionne.groupby(dataframe_fusionne['order_purchase_timestamp'].dt.to_period('M')).size()

# Graph évolution temporelle des commandes
plt.figure(figsize=(12, 6))
orders_by_month.plot(marker='o', linestyle='-', color='b')
plt.title('Evolution temporelle des commandes')
plt.xlabel('Mois')
plt.ylabel('Nombre de commandes')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

#Récupération des prix de stockages journaliers en moyenne pour chaque type de produit


import matplotlib.pyplot as plt
import numpy as np


# On récupère les catégories
categories = dataframe_final_filtered['product_category_name_english'].unique()

# une couleur par catégorie
colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))

# ON map chaque catégorie à une couleur
category_color_map = {category: color for category, color in zip(categories, colors)}

# On assigne une couleur a une catégorie spécifique
dataframe_final_filtered.loc[:, 'category_color'] = dataframe_final_filtered['product_category_name_english'].map(category_color_map)

# On Trace le graphique avec le volume sur l'axe des x, le prix de stockage par jour sur l'axe des y et la couleur selon la catégorie
plt.scatter(dataframe_final_filtered['Volume'], dataframe_final_filtered['price_storage_per_day'], c=dataframe_final_filtered['category_color'], alpha=0.5)

# On add  une légende pour les catégories
for category, color in category_color_map.items():
    plt.scatter([], [], color=[color], label=category)  # Utilisation de color=[] au lieu de c=[]

# Ajoute les labels et le titre
plt.title('Relation entre le Volume d un article, le prix de stockage par jour en fonction des catégories de produits')
plt.xlabel('Volume')
plt.ylabel('Prix de stockage par jour')
plt.legend(title='Catégories')

plt.show()




#dans ce graph , on affiche les catégories de produits avec  des couts  de charges totaux et le prix total et le prix du produit
#On peut voir  que pour certain produit , il serait interessant d'arreter d'en vendre comme pour  "gargen tools" qui n'est pas rentable
#au détriment de catégories comme  "auto" ou "computer_accessories"

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# conversion 'order_purchase_timestamp' en datetime
dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

# Fonction pour calculer les jours écoulés depuis le début du mois
def jours_ecoules_debut_mois(date):
    premier_jour_mois = date.replace(day=1)
    return (date - premier_jour_mois).days + 1

# On applique la fonction pour créer la colonne 'jours_ecoules_debut_mois'
dataframe_final_filtered['jours_ecoules_debut_mois'] = dataframe_final_filtered['order_purchase_timestamp'].apply(jours_ecoules_debut_mois)

# On calcule le coût total de stockage et le prix total
dataframe_final_filtered['price_storage_total'] = dataframe_final_filtered['price_storage_per_day'] * dataframe_final_filtered['jours_ecoules_debut_mois']
dataframe_final_filtered['prix_total'] = dataframe_final_filtered['price'] + dataframe_final_filtered['price_storage_total'] + dataframe_final_filtered['price_delivery']

# On renomme les colonnes pour un affichage correct dans la légende
dataframe_final_filtered = dataframe_final_filtered.rename(columns={
    'price_storage_total': 'Charges',
    'prix_total': 'Prix total',
    'price': 'Prix du produit'
})

# On calcule les 10 catégories de produits les plus commandées
top_categories = dataframe_final_filtered['product_category_name_english'].value_counts().head(10).index

# On filtre le DataFrame pour inclure seulement les top 10 catégories
dataframe_top_categories = dataframe_final_filtered[dataframe_final_filtered['product_category_name_english'].isin(top_categories)]

# On construit les data 
df_plot = dataframe_top_categories.melt(id_vars='product_category_name_english', 
                                        value_vars=['Charges', 'Prix total', 'Prix du produit'], 
                                        var_name='cost_type', 
                                        value_name='cost_value')

# On trace le graphique avec Seaborn
plt.figure(figsize=(12, 8))
sns.barplot(data=df_plot, x='product_category_name_english', y='cost_value', hue='cost_type', alpha=0.9)
plt.title('Comparaison des coûts de stockage, de livraison et prix total pour les 10 catégories de produits les plus commandées')
plt.xlabel('Catégories de produits')
plt.ylabel('Coût')
plt.xticks(rotation=45)
plt.legend(title='Type de coût')
plt.show()


import pandas as pd

# Calcul du nombre total d'unités vendues par produit
nombre_d_unites_vendues_par_produit = dataframe_final_filtered.groupby('product_id')['order_item_id'].sum().reset_index()
dataframe_final_filtered['jours_ecoules_debut_mois'] = dataframe_final_filtered['order_purchase_timestamp'].apply(jours_ecoules_debut_mois)

# On calcule le coût total de stockage et le prix total
dataframe_final_filtered['price_storage_total'] = dataframe_final_filtered['price_storage_per_day'] * dataframe_final_filtered['jours_ecoules_debut_mois']
# Calcul du coût moyen de stockage par unité vendue
dataframe_final_filtered['coût_stockage_par_unité'] = dataframe_final_filtered['price_storage_total'] / nombre_d_unites_vendues_par_produit['order_item_id']

import matplotlib.pyplot as plt
import seaborn as sns

# graph
plt.figure(figsize=(12, 8))
sns.barplot(data=dataframe_final_filtered, x='product_category_name_english', y='coût_stockage_par_unité', palette='rocket')
plt.title('Coût moyen de stockage par unité vendue par catégorie de produits')
plt.xlabel('Catégorie de produits')
plt.ylabel('Coût moyen de stockage par unité vendue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Calcul de la marge brute
dataframe_final_filtered['marge_brute'] = dataframe_final_filtered['Prix total'] - (dataframe_final_filtered['Charges'] + dataframe_final_filtered['price_delivery'] + dataframe_final_filtered['price_storage_per_day'])

# Récup des top catégories
df_top_categories = dataframe_final_filtered[dataframe_final_filtered['product_category_name_english'].isin(top_categories)]

# construction des données pour le graphique
df_plot_marge_brute = df_top_categories.groupby('product_category_name_english')['marge_brute'].sum().reset_index()

# graph
plt.figure(figsize=(12, 8))
sns.barplot(data=df_plot_marge_brute, x='product_category_name_english', y='marge_brute', palette='viridis')
plt.title('Marge Brute par Catégorie de Produits')
plt.xlabel('Catégories de produits')
plt.ylabel('Marge Brute')
plt.xticks(rotation=45)
plt.show()



# dans ce graph , on montre  l'impact du nombre de produits vendus et la rentabilité  par catégories de produits  on distingue donc que watches_gift n'est pas rentable du tout 
# en revanche heal_beauty est très interessant car peu de vente mais CA enorme
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Calcul du nombre de produits vendus par catégorie
df_products_per_category = dataframe_final_filtered.groupby('product_category_name_english')['product_id'].nunique().reset_index()
df_products_per_category = df_products_per_category.rename(columns={'product_id': 'Nombre de Produits Vendus'})

# Calcul du chiffre d'affaires total par catégorie
df_sales_per_category = dataframe_final_filtered.groupby('product_category_name_english')['Prix total'].sum().reset_index()

# Fusion des deux DataFrames pour avoir une vue complète
df_analysis = pd.merge(df_products_per_category, df_sales_per_category, on='product_category_name_english')

# graph
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df_analysis, x='Nombre de Produits Vendus', y='Prix total', hue='product_category_name_english', palette='viridis', s=100)
plt.title('Diversification des Produits et Impact sur la Rentabilité')
plt.xlabel('Nombre de Produits Vendus dans la Catégorie')
plt.ylabel('Chiffre d\'Affaires Total (Prix total)')
plt.legend(title='Catégorie de Produits', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Conversion de 'order_purchase_timestamp' en datetime si ce n'est pas déjà fait
dataframe_final_filtered['order_purchase_timestamp'] = pd.to_datetime(dataframe_final_filtered['order_purchase_timestamp'])

# Filtrage des données pour le mois de juillet 2018
data_july_2018 = dataframe_final_filtered[(dataframe_final_filtered['order_purchase_timestamp'].dt.year == 2018) & 
                                          (dataframe_final_filtered['order_purchase_timestamp'].dt.month == 7)]

# récup du jour du mois à partir de 'order_purchase_timestamp'
data_july_2018['jour_du_mois'] = data_july_2018['order_purchase_timestamp'].dt.day

# Liste des catégories de produits uniques
categories_produits = data_july_2018['product_category_name_english'].unique()

# Comptage du nombre de commandes pour chaque jour du mois et catégorie de produits
orders_by_day_and_category = data_july_2018.groupby(['jour_du_mois', 'product_category_name_english']).size().reset_index(name='nombre_commandes')

# création de la pivot table avec pivot_table
pivot_table = orders_by_day_and_category.pivot_table(index='jour_du_mois', columns='product_category_name_english', values='nombre_commandes', aggfunc='sum', fill_value=0)

# graph
plt.figure(figsize=(14, 10))
sns.heatmap(pivot_table, cmap='viridis', annot=True, fmt='.0f', cbar=True)
plt.title('Somme des Commandes par Jour du Mois et Catégorie de Produits - Juillet 2018')
plt.xlabel('Catégorie de Produits')
plt.ylabel('Jour du Mois')
plt.yticks(rotation=0)
plt.show()

