# EPF Min2 - IA Exploratoire et Symbolique

Anaïs DEWEVER - Edwige LEBLANC - Marianne LEPERE

---

## Sujets détaillés pour le projet

### 9. Solveur de Wordle par CSP (et LLM)

**Description du problème et contexte**
Wordle est un jeu de mots dans lequel à chaque tentative de mot, on obtient des indications de lettres bien placées, mal placées ou absentes. Ces indices se traduisent par des contraintes sur le mot secret : certaines positions doivent contenir certaines lettres, d'autres non, etc. Un programme peut appliquer ces contraintes à un dictionnaire pour filtrer les mots possibles. Par exemple, une approche par contraintes définit des variables pour chaque lettre du mot secret et impose les retours (vert, jaune, gris) comme contraintes logiques sur ces variables.

**Références multiples**

- **Approche CSP** : [Beating Wordle: Constraint Programming](https://medium.com/better-programming/beating-wordle-constraint-programming-ef0b0b6897fe) - Utilisation d'un solver de contraintes sur un dataset de mots
- **Implémentation** : hakank.org - Implémentation d'un solveur Wordle en OR-Tools CP-SAT
- **Function calling** : [OpenAI Function calling documentation](https://platform.openai.com/docs/guides/function-calling) - Appel de fonctions pour déléguer des tâches (ex. solveur externe)
- **Intégration LLM** : On peut intégrer un LLM en function-calling pour qu'il exploite un solveur CSP sous-jacent et propose des coups optimisés

**Approches suggérées**

- Définir des variables pour chaque lettre du mot secret et imposer les contraintes de retour (vert/jaune/gris)
- Utiliser un solveur de contraintes pour réduire l'espace des solutions à chaque coup
- Intégrer un LLM via function calling pour déduire les contraintes linguistiques
- Développer une stratégie d'optimisation pour minimiser le nombre de tentatives

**Technologies pertinentes**

- Python avec python-constraint ou OR-Tools CP-SAT pour la résolution
- Dictionnaires de mots français/anglais pour les domaines de variables
- API OpenAI ou modèles locaux pour l'intégration LLM
- Interface web avec React/Vue pour une expérience interactive

---

# Projet Wordle Solver

Ce projet est un **solveur et visualiseur Wordle** avec un backend FastAPI et un frontend simple en HTML/JS.  
Il permet de :

- Jouer au **Wordle quotidien (Daily Wordle)**
- Jouer au **Wordle aléatoire (Random Wordle)**
- Voir le solveur résoudre automatiquement le mot étape par étape avec un retour visuel

## 📂 Structure du projet

project-root/
│
├─ Api_wordle/
│ ├─ main.py
│ ├─ utils.py
│
├─ Solveur_wordle/
│ └─ Solveur_Wordle.py
│
├─ frontend/
│ └─ index.html
│
├─ word_list.txt
├─ requirements.txt
├─ README.md
└─ launch.py # Script pour lancer le projet

## 🚀 Lancer le projet localement

Le projet inclut un seul script `launch.py` qui :

1. Installe les dépendances Python depuis `requirements.txt`
2. Démarre le **backend FastAPI** (port par défaut 5000)
3. Démarre le **serveur HTTP du frontend** (port par défaut 8080)
4. Ouvre automatiquement le frontend dans votre navigateur par défaut à : `http://127.0.0.1:8080/` (sert `index.html` par défaut)

Exécutez depuis le dossier racine du projet :
python launch.py

Pour utiliser l'intégration LLM :
1. Créer un fichier config.py dans la base du projet
2. Générer une clé (https://ai.google.dev/gemini-api/docs/api-key?hl=fr)
3. Mettre dans config.py : GEMINI_API_KEY = "votre clé"
4. Lancer le projet comme indiqué plus haut

## 🔧 Configuration des ports

En haut de launch.py, vous pouvez modifier les ports si nécessaire :

API_PORT = 5000       # Port du backend FastAPI
FRONTEND_PORT = 8080  # Port du serveur HTTP du frontend

Si un port est déjà utilisé, changez-le et relancez le script.

## 🔹 Utilisation du frontend
Si le frontend ne s’ouvre pas automatiquement, ouvrez :
http://127.0.0.1:8080/

Cliquez sur :

- 🟦 Daily Wordle – sélectionne le mot du jour

- 🟩 Random Wordle – génère un mot aléatoire

- ▶ Solve – lance le solveur et affiche chaque étape avec retour coloré (vert, jaune, gris)

---