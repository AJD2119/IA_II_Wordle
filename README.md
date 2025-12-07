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
