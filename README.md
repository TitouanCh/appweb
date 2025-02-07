# 🧬 Projet Web – M2 AMI2B 2024-2025


## 🚀 Conception d’une application web pour l’annotation et l’analyse fonctionnelle de génomes bactériens

### 📖 Description du projet
Ce projet vise à développer une **application web** permettant de réaliser l’**annotation** et l’**analyse fonctionnelle** de **génomes bactériens**. L'application offre une gestion des utilisateurs avec différents rôles, un moteur de recherche pour explorer les séquences génomiques, ainsi que des outils pour l'annotation et la validation des génomes.

## 🛠️ Fonctionnalités principales

### 🔹 Gestion des utilisateurs et des rôles
- Authentification et gestion des utilisateurs
- Rôles disponibles : **Lecteur**, **Annotateur**, **Validateur**, **Administrateur**
- Gestion des comptes et des permissions

### 🔹 Recherche de génomes et de séquences
- Recherche par **génome** et **séquence**
- Affichage détaillé des séquences génomiques
- Hyperliens permettant d’accéder aux informations détaillées

### 🔹 Annotation et validation
- Annotation des **séquences non annotées**
- Assignation des séquences aux annotateurs
- Validation ou refus des annotations par les validateurs
- Suivi des annotations en attente

### 🔹 Visualisation et extraction
- Visualisation graphique des génomes
- Extraction des données sous format **.txt**
- Accès à des bases de données externes (ex: **NCBI Blast API**)

## 🏗️ Technologies utilisées

| Technologie      | Usage |
|-----------------|------------------------------------------------|
| Django (Python) | Backend et gestion des utilisateurs           |
| PostgreSQL      | Base de données relationnelle                 |
| HTML / CSS      | Interface utilisateur                         |
| JavaScript      | Amélioration de l’expérience utilisateur      |
| Git & GitHub    | Gestion de version et collaboration          |

## 🚀 Installation et exécution

### 📥 Prérequis
- **Python 3.x**
- **pip** (gestionnaire de paquets Python)
- **PostgreSQL** (ou SQLite pour le développement local)

### 🏗️ Installation
```bash
# 1. Cloner le dépôt
git clone <https://github.com/TitouanCh/appweb>
cd appweb

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la base de données
python manage.py migrate

# 4. Importer les données initiales
python manage.py import_sequences
python manage.py import_databases

# 5. Lancer le serveur Django
python manage.py runserver
```

### 🔗 Accéder à l’application
- **Interface utilisateur** : [localhost:8000](http://127.0.0.1:8000/)
- **Interface d’administration** : [localhost:8000/admin/](http://127.0.0.1:8000/admin/)

## 📌 Améliorations futures
- ✅ Interface améliorée avec **Bootstrap/Tailwind CSS**
- ✅ Système de messagerie interne pour les annotateurs
- ✅ Meilleure intégration avec **des bases de données externes**

## 👥 Équipe du projet
- **Encadrants** : Bryan Brancotte, Olivier Lespinet
- **Étudiants** : Titouan CHAMBE, Maxime PARIZOT, Nathan CARRE, Kubilay MEYDAN

## 📜 Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---



