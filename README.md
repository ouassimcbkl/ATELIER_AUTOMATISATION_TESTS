# API Testing Project - Frankfurter API

Ce dépôt contient la solution de "Testing as Code" pour l'API publique [Frankfurter](https://api.frankfurter.app).

## Fonctionnalités
- **Application Flask** présentant un dashboard des exécutions (Endpoint `/dashboard`).
- **Endpoint Health** (`/health`) pour surveiller l'état de l'application.
- **Tests robustes** vérifiant le contrat (HTTP 200, Content-Type, Types de données) et gérant les erreurs 404/Timeout.
- **QoS & Métriques** : Calcul de la latence moyenne, du P95 et du taux d'erreur, stockés localement dans une base SQLite.
- **Bouton d'exécution manuelle** via le Dashboard Web ou appel de l'endpoint `/run`.

## Déploiement sur PythonAnywhere

1. **Importer le dépôt** sur PythonAnywhere.
2. **Créer un Web App Flask** :
   - Pointer le `Source code` vers le dossier contenant `flask_app.py`.
   - Modifiez le fichier WSGI (visible dans l'onglet Web) pour instancier l'application Flask :
     ```python
     import sys
     path = '/home/votre_username/chemin_du_projet'
     if path not in sys.path:
         sys.path.append(path)
     from flask_app import app as application
     ```
3. **Installer les dépendances** :
   Ouvrez une console Bash PythonAnywhere et installez les dépendances :
   ```bash
   pip install -r requirements.txt --user
   ```

4. **Automatisation (Scheduled Tasks)** :
   - Rendez-vous dans l'onglet **Tasks**.
   - Créez une tâche (Scheduled Task) pour exécuter les tests régulièrement sans intervention manuelle.
   - Command : `curl -X POST https://VOTRE_URL.pythonanywhere.com/run`
   - Fréquence : Selon vos besoins (ex: daily). Cette commande va déclencher les tests et les résultats seront sauvegardés via l'application Flask dans la base SQLite.

## Lancement Local
Pour tester le projet localement :
```bash
pip install -r requirements.txt
python flask_app.py
```
Ouvrez votre navigateur sur `http://127.0.0.1:5000/`.

## Structure du Code
- `API_CHOICE.md` : Document d'analyse de l'API choisie.
- `flask_app.py` : Entrée principale Flask contenant les endpoints web.
- `tester/` : Module d'automatisation
   - `client.py` : Wrapper HTTP gérant les Timeouts et Retries (robustesse)
   - `tests.py` : Fonctions d'assertions (Testing as Code)
   - `runner.py` : Moteur d'exécution, compilation des résultats et métriques QoS.
- `storage.py` : Gestion DB SQLite locale.
- `templates/` : Dashboard Web HTML.
