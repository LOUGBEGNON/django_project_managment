# restaurant_app_django

## Description
Brève description de ce que fait le projet.

## Prérequis
Assurez-vous d'avoir installé Python 3.9 et pip sur votre machine.

## Installation

### Clonage du projet
Pour obtenir le projet, clonez le dépôt GitHub :
```bash
git clone https://github.com/LOUGBEGNON/django_project_managment.git
cd restaurant_app_django
```

### Configuration de l'environnement
Créez un environnement virtuel pour installer les dépendances :
```bash
python3.9 -m venv env
```

Activez l'environnement virtuel :
- Sur Windows :
  ```bash
  .\env\Scripts\activate
  ```
- Sur Unix ou MacOS :
  ```bash
  source env/bin/activate
  ```

### Installation des dépendances
Installez les dépendances du projet avec pip :
```bash
pip install -r requirements.txt
```

### Configuration des variables d'environnement
Créez un fichier `.env` dans le répertoire racine du projet et ajoutez-y les variables nécessaires. Exemple :
```plaintext
DEBUG=True
```

### Démarrage du serveur
Effectuez les migrations de votre base de données :
```bash
python manage.py migrate
```

Enfin, démarrez le serveur de développement :
```bash
python manage.py runserver
```

## Utilisation
Vous pouvez maintenant accéder à l'application via `http://127.0.0.1:8000` dans votre navigateur web.

## Contribution
Les contributions à ce projet sont les bienvenues. Veuillez suivre les bonnes pratiques de développement et maintenir la qualité du code.

