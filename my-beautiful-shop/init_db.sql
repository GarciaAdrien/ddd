-- Assurez-vous de créer les tables seulement si elles n'existent pas déjà
CREATE TABLE IF NOT EXISTS t_access (
    id_access SERIAL PRIMARY KEY,
    nom_access TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS t_users (
    id_user SERIAL PRIMARY KEY,
    us_login TEXT NOT NULL,
    password TEXT NOT NULL,
    id_access INT NOT NULL,
    FOREIGN KEY (id_access) REFERENCES t_access (id_access)
);

-- Créer la table user_access seulement si elle n'existe pas déjà
CREATE TABLE IF NOT EXISTS user_access (
    id_user INT NOT NULL,
    id_access INT NOT NULL,
    PRIMARY KEY (id_user, id_access),
    FOREIGN KEY (id_user) REFERENCES t_users (id_user),
    FOREIGN KEY (id_access) REFERENCES t_access (id_access)
);

-- Insérez les données seulement si les tables existent et sont vides (optionnel)
INSERT INTO t_access (id_access, nom_access) 
    SELECT 1, 'commercial' WHERE NOT EXISTS (SELECT 1 FROM t_access WHERE id_access = 1);
INSERT INTO t_access (id_access, nom_access) 
    SELECT 2, 'comptable' WHERE NOT EXISTS (SELECT 1 FROM t_access WHERE id_access = 2);
INSERT INTO t_access (id_access, nom_access) 
    SELECT 3, 'direction' WHERE NOT EXISTS (SELECT 1 FROM t_access WHERE id_access = 3);

INSERT INTO t_users (us_login, password, id_access)
    SELECT 'commercial@esgi.fr', 'commercial', 1 WHERE NOT EXISTS (SELECT 1 FROM t_users WHERE id_user = 1);
INSERT INTO t_users (us_login, password, id_access)
    SELECT 'comptable@esgi.fr', 'comptable', 2 WHERE NOT EXISTS (SELECT 1 FROM t_users WHERE id_user = 2);
INSERT INTO t_users (us_login, password, id_access)
    SELECT 'direction@esgi.fr', 'direction', 3 WHERE NOT EXISTS (SELECT 1 FROM t_users WHERE id_user = 3);
INSERT INTO t_users (us_login, password, id_access)
    SELECT 'admin@esgi.fr', 'admin', 3 WHERE NOT EXISTS (SELECT 1 FROM t_users WHERE id_user = 4);

-- Insérer des données dans user_access seulement si la table existe et est vide (optionnel)
INSERT INTO user_access (id_user, id_access) VALUES
(1, 1), -- commercial a accès commercial
(2, 2), -- comptable a accès comptable
(3, 3); -- direction a accès direction
(4, 1), -- admin a aussi accès commercial
(4, 2), -- admin a aussi accès comptable
(4, 3), -- admin a aussi accès direction


/*
-- Assurez-vous de créer les tables seulement si elles n'existent pas déjà
CREATE TABLE IF NOT EXISTS orders (
    customer_id TEXT,
    customer_unique_id TEXT,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT,
    order_status TEXT,
    order_purchase_timestamp TEXT,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT,
    order_item_id TEXT,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TEXT,
    price TEXT,
    freight_value TEXT,
    payment_sequential TEXT,
    payment_type TEXT,
    payment_installments TEXT,
    payment_value TEXT,
    review_id TEXT,
    review_score TEXT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TEXT,
    review_answer_timestamp TEXT,
    product_category_name_x TEXT,
    product_name_length TEXT,
    product_description_length TEXT,
    product_photos_qty TEXT,
    product_weight_g TEXT,
    product_length_cm TEXT,
    product_height_cm TEXT,
    product_width_cm TEXT,
    seller_zip_code_prefix TEXT,
    seller_city TEXT,
    seller_state TEXT,
    product_category_name_english TEXT,
    product_category_name_y TEXT,
    min_weight TEXT,
    max_weight TEXT,
    Volume TEXT,
    price_delivery TEXT,
    price_storage_per_day TEXT,
    jours_ecoules_debut_mois TEXT,  -- Assumed to be INT based on previous context
    price_storage_total TEXT,
    price_delivery_direct TEXT,
    PRIMARY KEY (customer_id, order_item_id)  -- Adjust primary key as per your dataset
);
*/
