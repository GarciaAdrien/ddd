import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

# Simuler le chargement des données depuis vos DataFrames
# Remplacer par les DataFrames réels
dataframe_fusionne = pd.DataFrame({
    'product_category_name_english': ['mesa_banho', 'beleza_saude', 'esporte_lazer', 'casa_decoracao', 'informatica_acessorios', 'moveis_decoracao', 'papelaria', 'telefonia', 'construcao_ferramentas_seguranca', 'automotivo'],
    'customer_state': ['SP', 'RJ', 'MG', 'ES', 'PR', 'SC', 'RS', 'DF', 'BA', 'PE'],
    'order_purchase_timestamp': pd.date_range(start='1/1/2023', periods=10, freq='M'),
    'order_id': range(10)
})

# Préparer les données pour les catégories de produits les plus commandées
top_categories = dataframe_fusionne['product_category_name_english'].value_counts().head(10)

# Préparer les données pour les commandes par état
orders_by_state = dataframe_fusionne['customer_state'].value_counts()

# Préparer les données pour l'évolution temporelle des commandes
dataframe_fusionne['order_purchase_timestamp'] = pd.to_datetime(dataframe_fusionne['order_purchase_timestamp'])
orders_by_month = dataframe_fusionne.groupby(dataframe_fusionne['order_purchase_timestamp'].dt.to_period('M')).size()

@app.route('/api/top-categories', methods=['GET'])
def get_top_categories():
    top_categories_data = {
        'labels': top_categories.index.tolist(),
        'datasets': [{
            'label': 'Nombre de produits Commandés',
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'data': top_categories.values.tolist()
        }]
    }
    return jsonify(top_categories_data)

@app.route('/api/orders-by-state', methods=['GET'])
def get_orders_by_state():
    orders_by_state_data = {
        'labels': orders_by_state.index.tolist(),
        'datasets': [{
            'label': 'Nombre de commandes',
            'backgroundColor': 'rgba(153, 102, 255, 0.2)',
            'borderColor': 'rgba(153, 102, 255, 1)',
            'borderWidth': 1,
            'data': orders_by_state.values.tolist()
        }]
    }
    return jsonify(orders_by_state_data)

@app.route('/api/orders-by-month', methods=['GET'])
def get_orders_by_month():
    orders_by_month_data = {
        'labels': orders_by_month.index.astype(str).tolist(),
        'datasets': [{
            'label': 'Nombre de commandes',
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgba(54, 162, 235, 1)',
            'borderWidth': 1,
            'fill': False,
            'data': orders_by_month.values.tolist()
        }]
    }
    return jsonify(orders_by_month_data)

if __name__ == '__main__':
    app.run(debug=True)