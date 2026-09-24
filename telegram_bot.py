import os
import json
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse

# 1. Configuration (Utilise les variables d'environnement sur GitHub)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "VOTRE_TOKEN_TELEGRAM_LOCAL")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "VOTRE_CHAT_ID_LOCAL")
DOSSIER_RSS = "rss"
FICHIER_MEMOIRE = "envoyees.json"


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


def envoyer_message_telegram(texte):
    """Envoie un message texte simple via l'API Bot Telegram standard."""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    donnees = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
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

                # On récupère les <item> du flux XML (du plus ancien au plus récent si possible)
                items = root.findall(".//item")

                # On les inverse [::-1] pour envoyer la plus ancienne d'abord s'il y en a 2 nouvelles
                for item in items[::-1]:
                    lien_video = item.find("link").text
                    titre_video = item.find("title").text
                    description = item.find("description").text

                    # Si le lien n'est pas dans l'historique, c'est une nouveauté !
                    if lien_video not in historique:
                        print(f"✨ Nouvelle vidéo détectée pour @{createur} !")

                        # Formatage du message Telegram
                        message = (
                            f"🎬 <b>Nouvelle vidéo de @{createur}</b>\n\n"
                            f"📝 {titre_video}\n\n"
                            f"🔗 <a href='{lien_video}'>Regarder sur TikTok</a>"
                        )

                        if envoyer_message_telegram(message):
                            historique.add(lien_video)
                            nouvelles_videos_detectees = True

            except Exception as e:
                print(f"❌ Erreur lors de la lecture de {fichier} : {e}")

    if nouvelles_videos_detectees:
        sauvegarder_historique(historique)
    else:
        print("😴 Aucune nouvelle vidéo à envoyer sur Telegram.")


if __name__ == "__main__":
    if TELEGRAM_TOKEN == "VOTRE_TOKEN_TELEGRAM_LOCAL" or TELEGRAM_CHAT_ID == "VOTRE_CHAT_ID_LOCAL":
        print("⚠️ Mode local : Pensez à configurer vos accès Telegram pour tester.")
    verifier_et_notifier()
