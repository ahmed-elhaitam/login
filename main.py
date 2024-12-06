import streamlit as st
import mysql.connector

# Fonction pour se connecter à la base de données
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="34.163.145.6",  # Adresse IP publique de votre instance Cloud SQL
            port=3306,            # Port par défaut pour MySQL
            user="root",          # Utilisateur MySQL
            password="12345",  # Remplacez par votre mot de passe MySQL
            database="CNC-BD"     # Nom de la base de données
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Erreur de connexion à la base de données : {err}")
        return None

# Fonction pour insérer un utilisateur
def insert_user(connection, nom, prenom, gmail, password):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO utilisateurs (nom, prenom, gmail, password)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nom, prenom, gmail, password))
        connection.commit()
        cursor.close()
        st.success("Utilisateur ajouté avec succès !")
    except mysql.connector.Error as err:
        st.error(f"Erreur lors de l'insertion : {err}")

# Fonction pour récupérer les utilisateurs
def fetch_users(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT nom, prenom, gmail FROM utilisateurs"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error as err:
        st.error(f"Erreur lors de la récupération des utilisateurs : {err}")
        return []

# Interface Streamlit
st.title("Gestion des utilisateurs")

# Formulaire pour ajouter un utilisateur
with st.form("Ajouter un utilisateur"):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    gmail = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    submitted = st.form_submit_button("Ajouter")

    if submitted:
        if nom and prenom and gmail and password:
            connection = connect_to_database()
            if connection:
                insert_user(connection, nom, prenom, gmail, password)
                connection.close()
        else:
            st.error("Tous les champs sont obligatoires.")

# Afficher la liste des utilisateurs
st.subheader("Liste des utilisateurs")
connection = connect_to_database()
if connection:
    users = fetch_users(connection)
    connection.close()

    if users:
        st.table(users)
    else:
        st.write("Aucun utilisateur trouvé.")
