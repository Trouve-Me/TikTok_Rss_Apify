# 📱 TikTok RSS Apify & Telegram Bot

<p align="center">
  <b>Surveillez automatiquement vos créateurs TikTok préférés, générez des flux RSS locaux et recevez des notifications enrichies directement sur Telegram.</b>
</p>

<p align="center">
  <a href="https://t.me/+8F_mqcAGerwxNWY0">
    <img src="https://img.shields.io/badge/Rejoindre-Canal%20Telegram-blue?style=for-the-badge&logo=telegram" alt="Rejoindre le canal Telegram">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Apify-API-orange?style=flat-square" alt="Apify">
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=flat-square&logo=telegram" alt="Telegram">
  <img src="https://img.shields.io/badge/RSS-XML-orange?style=flat-square" alt="RSS">
</p>

---

## 🚀 Présentation

**TikTok RSS Apify** est un projet Python modulaire permettant de transformer le suivi de comptes TikTok en un système automatisé de veille.

Le projet s'appuie sur **Apify** pour récupérer les dernières publications des créateurs surveillés, génère des **flux RSS XML locaux**, puis utilise un **bot Telegram** pour détecter les nouvelles vidéos et envoyer automatiquement des notifications enrichies.

L'objectif est de disposer d'une solution simple permettant de :

* 👤 surveiller plusieurs comptes TikTok ;
* 🔄 récupérer automatiquement leurs dernières publications ;
* 📡 générer un flux RSS indépendant pour chaque créateur ;
* 📌 ignorer les vidéos épinglées si nécessaire ;
* 🖼️ récupérer et afficher les miniatures ;
* 📝 conserver les descriptions complètes ;
* 🕐 afficher les dates de publication ;
* 🔔 envoyer les nouvelles vidéos sur Telegram ;
* 🛡️ éviter les notifications en double ;
* 🔑 utiliser plusieurs clés Apify avec basculement automatique ;
* 💾 conserver localement les flux et l'historique des notifications.

---

# ✨ Fonctionnalités

## 📡 Scraping TikTok via Apify

Le script de récupération interroge Apify afin d'obtenir les dernières publications des comptes configurés.

Pour chaque créateur, le système peut notamment récupérer :

* le nom d'utilisateur ;
* l'URL de la vidéo ;
* la description ;
* la date de publication ;
* la miniature ;
* les informations disponibles sur la vidéo ;
* les métadonnées nécessaires à la génération du flux RSS.

---

## 📰 Génération de flux RSS

Chaque compte TikTok surveillé dispose de son propre fichier RSS.

Exemple :

```text
rss/
├── creator_1.xml
├── creator_2.xml
├── creator_3.xml
└── creator_4.xml
```

Ces fichiers peuvent ensuite être utilisés avec n'importe quel lecteur RSS compatible.

Exemple :

```text
rss/@createur.xml
```

Le flux contient les dernières publications détectées pour le compte correspondant.

---

## 📌 Gestion des vidéos épinglées

Les vidéos épinglées peuvent être ignorées afin d'éviter qu'elles soient considérées comme de nouvelles publications.

Cela permet notamment d'éviter le problème suivant :

```text
Compte TikTok
│
├── 📌 Ancienne vidéo épinglée
├── 📌 Ancienne vidéo épinglée
├── 🎬 Nouvelle vidéo
└── 🎬 Nouvelle vidéo
```

Le système se concentre alors sur les publications réellement récentes.

---

## 🔔 Notifications Telegram

Le bot surveille les flux RSS générés localement et détecte les nouvelles entrées.

Lorsqu'une nouvelle vidéo est détectée, il peut envoyer une notification contenant :

```text
🎬 Nouveau TikTok !

👤 @createur

📝 Description de la vidéo...

📅 24 septembre 2026

🔗 Voir la vidéo
```

Lorsque la miniature est disponible, elle est également utilisée afin de rendre la notification plus visuelle.

---

## 🛡️ Système anti-doublons

Le fichier :

```text
envoyees.json
```

permet de conserver l'historique des vidéos déjà envoyées.

Exemple :

```json
{
  "creator_1": [
    "https://www.tiktok.com/@creator_1/video/123456789",
    "https://www.tiktok.com/@creator_1/video/987654321"
  ]
}
```

Avant d'envoyer une notification, le bot vérifie si la vidéo est déjà présente dans cet historique.

Cela évite les notifications répétées après :

* un redémarrage du bot ;
* une nouvelle exécution du script ;
* une mise à jour du flux RSS ;
* une erreur temporaire ;
* une modification du fichier RSS.

---

# 📁 Structure du projet

```text
TikTokRss/
│
├── 📁 rss/
│   ├── creator_1.xml
│   ├── creator_2.xml
│   └── ...
│
├── 📄 abonnements.csv
├── 🔐 cles_apify.json
├── 🔐 config_telegram.json
├── 💾 envoyees.json
│
├── 🐍 main_test.py
├── 🐍 bot_telegram.py
│
└── 📄 README.md
```

### Description des fichiers

| Fichier                | Rôle                                    |
| ---------------------- | --------------------------------------- |
| `rss/`                 | Contient les flux RSS générés           |
| `abonnements.csv`      | Liste des créateurs TikTok à surveiller |
| `cles_apify.json`      | Clés API Apify utilisées par le scraper |
| `config_telegram.json` | Configuration du bot Telegram           |
| `envoyees.json`        | Historique anti-doublons                |
| `main_test.py`         | Récupération TikTok + génération RSS    |
| `bot_telegram.py`      | Analyse RSS + notifications Telegram    |
| `README.md`            | Documentation du projet                 |

---

# ⚙️ Installation

## 1. Prérequis

Le projet nécessite :

* Python **3.10 ou supérieur** ;
* un compte **Apify** ;
* un ou plusieurs tokens API Apify ;
* un bot Telegram ;
* un environnement capable d'exécuter les scripts Python régulièrement.

Vérifier la version de Python :

```bash
python --version
```

ou :

```bash
python3 --version
```

---

## 2. Cloner le projet

```bash
git clone https://github.com/VOTRE_UTILISATEUR/TikTokRss.git
cd TikTokRss
```

> Remplacez l'URL par celle de votre dépôt.

---

## 3. Créer un environnement virtuel

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 4. Installer les dépendances

Si un fichier `requirements.txt` est présent :

```bash
pip install -r requirements.txt
```

Sinon, installez les dépendances utilisées par votre version du projet.

Exemple :

```bash
pip install requests feedparser python-telegram-bot
```

---

# 👤 Configuration des abonnements

Le fichier :

```text
abonnements.csv
```

contient les comptes TikTok à surveiller.

Exemple :

```csv
username
tiktok
createur1
createur2
createur3
```

Selon l'implémentation du scraper, le fichier peut également utiliser une structure plus simple :

```csv
tiktok
createur1
createur2
createur3
```

### Recommandation

Utilisez de préférence les pseudos **sans `@`** :

```text
createur1
createur2
createur3
```

Le programme pourra ensuite construire automatiquement les URLs correspondantes.

---

# 🔑 Configuration Apify

Le fichier :

```text
cles_apify.json
```

permet de stocker plusieurs clés API.

Exemple :

```json
{
  "cles": [
    "APIFY_API_TOKEN_1",
    "APIFY_API_TOKEN_2",
    "APIFY_API_TOKEN_3"
  ]
}
```

Le système peut ainsi passer automatiquement à une autre clé lorsqu'une clé rencontre une limite, une erreur ou devient temporairement indisponible.

### ⚠️ Important

Ne publiez **jamais** vos clés API dans un dépôt Git public.

Ajoutez notamment les fichiers sensibles à `.gitignore` :

```gitignore
cles_apify.json
config_telegram.json
envoyees.json
.venv/
__pycache__/
*.pyc
```

---

# 🤖 Configuration du bot Telegram

Créez un bot Telegram via **BotFather**, puis récupérez son token.

Le fichier :

```text
config_telegram.json
```

peut par exemple contenir :

```json
{
  "bot_token": "123456789:ABCDEF_VOTRE_TOKEN",
  "chat_id": "-1001234567890"
}
```

Selon votre implémentation, vous pouvez également prévoir plusieurs destinations :

```json
{
  "bot_token": "123456789:ABCDEF_VOTRE_TOKEN",
  "chat_ids": [
    "-1001234567890",
    "-1009876543210"
  ]
}
```

Le bot doit avoir les permissions nécessaires dans le groupe ou canal auquel les notifications doivent être envoyées.

---

# ▶️ Utilisation

Le fonctionnement général est divisé en deux étapes.

```text
                ┌─────────────────────┐
                │ abonnements.csv     │
                │ Comptes TikTok      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Apify Scraper    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Génération des RSS  │
                │     /rss/*.xml      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Bot Telegram        │
                │ Analyse des RSS     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ envoyees.json       │
                │ Anti-doublons       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ 🔔 Telegram         │
                │ Notification        │
                └─────────────────────┘
```

---

## 1. Générer les flux RSS

Lancer :

```bash
python main_test.py
```

Le programme récupère les publications des comptes configurés puis génère les fichiers XML dans :

```text
rss/
```

Exemple :

```text
rss/
├── createur1.xml
├── createur2.xml
└── createur3.xml
```

---

## 2. Lancer le bot Telegram

Dans un second terminal :

```bash
python bot_telegram.py
```

Le bot analyse les flux RSS et détecte les nouvelles publications.

Lorsqu'une vidéo n'a pas encore été envoyée, elle est transmise à Telegram.

---

# 🔄 Automatisation

Pour utiliser le projet comme véritable système de veille, il est recommandé d'exécuter automatiquement le scraper à intervalle régulier.

Par exemple :

```text
Toutes les 10 minutes
       │
       ▼
main_test.py
       │
       ▼
Mise à jour des RSS
       │
       ▼
bot_telegram.py
       │
       ▼
Notification Telegram
```

---

## Linux — Cron

Exemple avec une exécution toutes les 10 minutes :

```cron
*/10 * * * * cd /chemin/vers/TikTokRss && /chemin/vers/.venv/bin/python main_test.py >> scraper.log 2>&1
```

Le bot Telegram peut être exécuté séparément comme processus permanent :

```bash
python bot_telegram.py
```

Pour un serveur Linux, l'utilisation d'un service `systemd`, Docker ou d'un gestionnaire de processus est recommandée.

---

# 🐳 Docker

Une future évolution du projet peut permettre de lancer l'ensemble du système avec Docker :

```text
docker-compose.yml
│
├── scraper
│   └── main_test.py
│
└── telegram-bot
    └── bot_telegram.py
```

L'objectif serait de pouvoir démarrer le projet avec :

```bash
docker compose up -d
```

et consulter les logs avec :

```bash
docker compose logs -f
```

---

# 🧠 Gestion du failover Apify

Lorsque plusieurs clés Apify sont configurées, le scraper peut utiliser une stratégie de basculement.

Exemple :

```text
Clé #1
 │
 ├── OK ───────────────► Continuer
 │
 └── Erreur / limite
          │
          ▼
       Clé #2
          │
          ├── OK ──────► Continuer
          │
          └── Erreur
                 │
                 ▼
              Clé #3
```

Cela permet d'améliorer la continuité du service lorsque plusieurs tokens sont disponibles.

> Il est recommandé de journaliser les erreurs plutôt que de masquer silencieusement les échecs.

---

# 📰 Format RSS

Chaque flux XML suit la structure RSS standard.

Exemple simplifié :

```xml
<?xml version="1.0" encoding="UTF-8"?>

<rss version="2.0">
  <channel>

    <title>TikTok - @createur</title>

    <link>https://www.tiktok.com/@createur</link>

    <description>Flux RSS de @createur</description>

    <item>
      <title>Nouvelle vidéo TikTok</title>

      <link>https://www.tiktok.com/@createur/video/123456789</link>

      <description>Description de la vidéo</description>

      <pubDate>Thu, 24 Sep 2026 20:00:00 GMT</pubDate>
    </item>

  </channel>
</rss>
```

---

# 🔔 Exemple de notification Telegram

Une notification peut être présentée de la manière suivante :

```text
🎬 Nouvelle vidéo TikTok

👤 @createur

📝 Une nouvelle vidéo vient d'être publiée !

📅 24 septembre 2026 à 20:00

🔗 Voir sur TikTok
```

Avec la miniature, le message peut être envoyé sous forme de média accompagné de sa légende.

---

# 🛡️ Gestion des erreurs

Le projet devrait idéalement gérer les erreurs suivantes :

### Apify

* token invalide ;
* quota atteint ;
* acteur indisponible ;
* timeout ;
* erreur réseau ;
* réponse inattendue.

### RSS

* fichier XML invalide ;
* flux inaccessible ;
* entrée malformée ;
* date absente ou invalide.

### Telegram

* token invalide ;
* chat inexistant ;
* permissions insuffisantes ;
* erreur réseau ;
* limite d'envoi atteinte.

Chaque erreur devrait être enregistrée dans les logs afin de faciliter le diagnostic.

---

# 📋 Logs

Pour faciliter la maintenance, il est recommandé d'utiliser le module `logging` de Python plutôt que de simples `print()`.

Exemple :

```text
2026-09-24 20:00:01 [INFO] Démarrage du scraper
2026-09-24 20:00:02 [INFO] Récupération de @createur1
2026-09-24 20:00:05 [INFO] 5 vidéos récupérées
2026-09-24 20:00:05 [INFO] Flux RSS mis à jour
2026-09-24 20:00:06 [INFO] Scraping terminé
```

En cas d'erreur :

```text
2026-09-24 20:05:01 [ERROR] Token Apify #1 indisponible
2026-09-24 20:05:01 [INFO] Passage au token #2
```

---

# 🔒 Sécurité

Ne versionnez jamais les informations sensibles.

Votre dépôt Git ne devrait notamment pas contenir :

```text
cles_apify.json
config_telegram.json
```

Vous pouvez utiliser :

```text
config_telegram.example.json
cles_apify.example.json
```

pour documenter la structure attendue.

Exemple :

```json
{
  "bot_token": "VOTRE_TOKEN_TELEGRAM",
  "chat_id": "VOTRE_CHAT_ID"
}
```

Puis créer localement le véritable fichier de configuration.

---

# 🧹 Fichiers recommandés dans `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# IDE
.vscode/
.idea/

# Secrets
cles_apify.json
config_telegram.json

# Runtime
envoyees.json
*.log

# Generated RSS
rss/*.xml
```

Si les flux RSS doivent être distribués ou versionnés, retirez évidemment `rss/*.xml` du `.gitignore`.

---

# 🛠️ Dépannage

## Le bot n'envoie aucune notification

Vérifiez :

1. que `main_test.py` fonctionne correctement ;
2. que des fichiers XML sont générés dans `rss/` ;
3. que `bot_telegram.py` lit bien le dossier `rss/` ;
4. que le token Telegram est valide ;
5. que le `chat_id` est correct ;
6. que le bot possède les permissions nécessaires ;
7. que la vidéo n'est pas déjà enregistrée dans `envoyees.json`.

---

## Les notifications sont envoyées plusieurs fois

Vérifiez le fichier :

```text
envoyees.json
```

et assurez-vous que l'identifiant utilisé pour reconnaître une vidéo est stable.

Il est préférable d'utiliser l'**ID unique de la vidéo TikTok** plutôt que sa description ou son titre.

---

## Une vidéo ancienne est envoyée comme nouvelle

Cela peut arriver après :

* la suppression de `envoyees.json` ;
* une réinitialisation de l'historique ;
* un changement de logique d'identification ;
* une première installation du bot.

Une stratégie de première initialisation peut consister à enregistrer les vidéos existantes sans les notifier, puis à ne notifier que les publications apparues après cette initialisation.

---

# 🚧 Améliorations possibles

Plusieurs fonctionnalités peuvent être ajoutées au projet.

### 📊 Statistiques

Ajouter des statistiques telles que :

```text
👤 42 créateurs surveillés
🎬 1 284 vidéos détectées
🔔 937 notifications envoyées
⏱️ Dernière mise à jour : il y a 3 minutes
```

### 🗂️ Plusieurs catégories

Organiser les créateurs par groupe :

```text
Gaming
├── creator1
├── creator2

Tech
├── creator3
├── creator4

Actualité
├── creator5
└── creator6
```

### 🎯 Filtres

Permettre de filtrer les publications selon :

* mots-clés ;
* hashtags ;
* longueur de description ;
* date ;
* créateur.

### 📱 Plusieurs canaux Telegram

Associer certains créateurs à certains canaux :

```text
@creator1 ──► Canal Gaming
@creator2 ──► Canal Tech
@creator3 ──► Canal News
```

### 🌐 Interface Web

Une interface web pourrait permettre de :

* ajouter/supprimer un créateur ;
* consulter les flux ;
* voir les dernières vidéos ;
* gérer les clés Apify ;
* modifier la fréquence de scraping ;
* consulter les logs ;
* gérer les destinations Telegram.

---

# 🗺️ Roadmap

* [x] Récupération des créateurs TikTok
* [x] Génération des flux RSS
* [x] Filtrage des vidéos épinglées
* [x] Notifications Telegram
* [x] Système anti-doublons
* [x] Gestion de plusieurs clés Apify
* [ ] Configuration via variables d'environnement
* [ ] Système de logs avancé
* [ ] Dockerisation
* [ ] Interface Web
* [ ] Gestion de plusieurs canaux Telegram
* [ ] Statistiques
* [ ] Filtres avancés
* [ ] Tests automatisés
* [ ] CI/CD

---

# 🤝 Contribution

Les contributions sont les bienvenues.

Pour proposer une modification :

```bash
git checkout -b feature/ma-fonctionnalite
```

Effectuez vos modifications puis :

```bash
git add .
git commit -m "Ajout de ma fonctionnalité"
git push origin feature/ma-fonctionnalite
```

Ouvrez ensuite une Pull Request.

---

# ⚠️ Limites et bonnes pratiques

Ce projet dépend de services externes et leur comportement peut évoluer.

En particulier :

* les données accessibles via TikTok peuvent changer ;
* les acteurs Apify peuvent évoluer ;
* les limites API peuvent être modifiées ;
* Telegram applique ses propres limites d'envoi ;
* certaines informations peuvent être absentes selon la publication.

Le projet doit donc prévoir une gestion robuste des erreurs et éviter de supposer que toutes les métadonnées seront toujours disponibles.

Utilisez les services concernés conformément à leurs conditions d'utilisation et aux règles applicables.

---

# 📄 Licence

Ajoutez ici la licence choisie pour le projet.

Exemple :

```text
MIT License
```

Si aucune licence n'est encore définie, indiquez clairement que le projet est actuellement distribué sans licence explicite.

---

# ❤️ Remerciements

Merci aux projets et services qui rendent cette automatisation possible :

* **Apify** pour l'infrastructure de collecte ;
* **Telegram** pour la plateforme de notification ;
* **Python** pour l'écosystème et les bibliothèques utilisées ;
* les développeurs et contributeurs du projet.

---

<p align="center">
  <b>📱 TikTok → 📡 RSS → 🔔 Telegram</b>
</p>

<p align="center">
  Automatisez votre veille TikTok simplement.
</p>
