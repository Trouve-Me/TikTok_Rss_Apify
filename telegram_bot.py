import os
import json
import re
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

# Configuration des fichiers
CHEMIN_CONFIG = "config_telegram.json"
DOSSIER_RSS = "rss"
FICHIER_MEMOIRE = "envoyees.json"


def charger_config_telegram():
    """Charge les identifiants Telegram depuis le fichier JSON."""
    if not os.path.exists(CHEMIN_CONFIG):
        print(f"❌ ERREUR : Le fichier {CHEMIN_CONFIG} est introuvable.")
        return None, None
    try:
        with open(CHEMIN_CONFIG, "r", encoding="utf-8") as f:
            config = json.load(f)
            token = str(config.get("telegram_token")).strip()
            chat_id = str(config.get("telegram_chat_id")).strip()
            return token, chat_id
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de la config Telegram : {e}")
        return None, None


def charger_historique():
    """Charge la liste des vidéos déjà envoyées pour éviter les doublons."""
    if os.path.exists(FICHIER_MEMOIRE):
        try:
            with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def sauvegarder_historique(historique):
    """Sauvegarde la liste mise à jour."""
    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as f:
        json.dump(list(historique), f, ensure_ascii=False, indent=2)


def envoyer_notification_telegram(token, chat_id, image_url, legende):
    """Envoie la miniature de la vidéo en photo, ou bascule sur un message texte en cas d'échec."""
    token_propre = str(token).strip()
    chat_id_propre = str(chat_id).strip()

    # Tentative d'envoi de la photo (miniature) avec la légende
    if image_url:
        url = f"https://api.telegram.org/bot{token_propre}/sendPhoto"
        payload = {
            "chat_id": chat_id_propre,
            "photo": image_url,
            "caption": legende,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload, timeout=20)
            if response.status_code == 200:
                return True
            else:
                print(f"⚠️ Échec sendPhoto ({response.status_code}), bascule sur sendMessage : {response.text}")
        except Exception as e:
            print(f"⚠️ Erreur réseau sendPhoto : {e}")

    # Repli : Envoi d'un message texte classique si pas d'image ou échec
    url = f"https://api.telegram.org/bot{token_propre}/sendMessage"
    payload = {
        "chat_id": chat_id_propre,
        "text": legende,
        "parse_mode": "HTML",
        "link_preview_options": {"is_disabled": False}
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"⚠️ Échec Telegram (Code {response.status_code}) : {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'appel API Telegram : {e}")
        return False


def verifier_et_notifier():
    token, chat_id = charger_config_telegram()
    if not token or not chat_id:
        print("🚨 Configuration Telegram incomplète. Annulation de l'envoi.")
        return

    if not os.path.exists(DOSSIER_RSS):
        print("📂 Aucun dossier RSS trouvé.")
        return

    historique = charger_historique()
    nouvelles_videos_detectees = False

    for fichier in os.listdir(DOSSIER_RSS):
        if fichier.endswith(".xml"):
            chemin_xml = os.path.join(DOSSIER_RSS, fichier)
            createur = fichier.replace(".xml", "")

            try:
                tree = ET.parse(chemin_xml)
                root = tree.getroot()
                items = root.findall(".//item")

                for item in items[::-1]:
                    lien_video = item.find("link").text

                    # Récupération de la description complète et nettoyage du compteur de vues
                    description_brute = item.find("description").text if item.find("description") is not None else ""
                    description_nette = re.sub(r'\s*\(Vues:\s*\d+\)', '', description_brute).strip()

                    # Récupération et formatage de la date de publication (<pubDate>)
                    pub_date_str = item.find("pubDate").text if item.find("pubDate") is not None else ""
                    try:
                        # Conversion du format RSS "Thu, 24 Sep 2026 09:14:39 GMT" en format lisible
                        dt = datetime.strptime(pub_date_str.replace(" GMT", ""), "%a, %d %b %Y %H:%M:%S")
                        date_formatee = dt.strftime("%d/%m/%Y à %H:%M")
                    except Exception:
                        date_formatee = pub_date_str  # Repli sur la chaîne brute si le parse échoue

                    # Récupération de l'URL de la miniature depuis l'enclosure
                    image_url = None
                    enclosure = item.find("enclosure")
                    if enclosure is not None:
                        image_url = enclosure.get("url")

                    if lien_video not in historique:
                        print(f"✨ Notification (avec miniature et date) pour la nouvelle vidéo de @{createur}...")

                        legende = (
                            f"🎬 <b>Nouvelle vidéo de @{createur}</b>\n\n"
                            f"📝 {description_nette}\n\n"
                            f"📅 {date_formatee}\n\n"
                            f"🔗 <a href='{lien_video}'>Regarder sur TikTok</a>"
                        )

                        if envoyer_notification_telegram(token, chat_id, image_url, legende):
                            historique.add(lien_video)
                            nouvelles_videos_detectees = True

            except Exception as e:
                print(f"❌ Erreur lors de la lecture du fichier XML {fichier} : {e}")

    if nouvelles_videos_detectees:
        sauvegarder_historique(historique)
        print("✅ Historique mis à jour.")
    else:
        print("😴 Toutes les vidéos sont déjà synchronisées sur Telegram.")


if __name__ == "__main__":
    verifier_et_notifier()