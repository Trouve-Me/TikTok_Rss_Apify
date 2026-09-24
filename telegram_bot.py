import os
import json
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse

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
            token = config.get("telegram_token")
            chat_id = config.get("telegram_chat_id")
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


def envoyer_message_telegram(token, chat_id, texte):
    """Envoie un message texte simple via l'API Bot Telegram standard."""
    url = f"https://telegram.org{token}/sendMessage"
    donnees = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": texte,
        "parse_mode": "HTML"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=donnees)
        with urllib.request.urlopen(req) as response:
            return response.getcode() == 200
    except Exception as e:
        print(f"❌ Erreur d'envoi Telegram : {e}")
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

    # Parcours de tous les fichiers XML du dossier rss/
    for fichier in os.listdir(DOSSIER_RSS):
        if fichier.endswith(".xml"):
            chemin_xml = os.path.join(DOSSIER_RSS, fichier)
            createur = fichier.replace(".xml", "")

            try:
                tree = ET.parse(chemin_xml)
                root = tree.getroot()
                items = root.findall(".//item")

                # Inversion pour traiter la plus ancienne d'abord
                for item in items[::-1]:
                    lien_video = item.find("link").text
                    titre_video = item.find("title").text

                    # Si le lien n'est pas dans l'historique, c'est une nouveauté !
                    if lien_video not in historique:
                        print(f"✨ Nouvelle vidéo détectée pour @{createur} !")

                        message = (
                            f"🎬 <b>Nouvelle vidéo de @{createur}</b>\n\n"
                            f"📝 {titre_video}\n\n"
                            f"🔗 <a href='{lien_video}'>Regarder sur TikTok</a>"
                        )

                        if envoyer_message_telegram(token, chat_id, message):
                            historique.add(lien_video)
                            nouvelles_videos_detectees = True

            except Exception as e:
                print(f"❌ Erreur lors de la lecture de {fichier} : {e}")

    if nouvelles_videos_detectees:
        sauvegarder_historique(historique)
    else:
        print("😴 Aucune nouvelle vidéo à envoyer sur Telegram.")


if __name__ == "__main__":
    verifier_et_notifier()
