import os
import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone
from apify_client import ApifyClient
from apify_client.errors import ApifyApiError

# Configuration des fichiers
CHEMIN_CSV = "abonnements.csv"
CHEMIN_JSON = "cles_apify.json"


def charger_cles_api():
    """Charge la liste des clés API depuis le fichier JSON."""
    if not os.path.exists(CHEMIN_JSON):
        print(f"❌ ERREUR : Le fichier {CHEMIN_JSON} est introuvable.")
        return []
    try:
        with open(CHEMIN_JSON, "r", encoding="utf-8") as f:
            cles = json.load(f)
            if isinstance(cles, list) and len(cles) > 0:
                return cles
            print("⚠️ Le fichier JSON est vide ou n'est pas une liste.")
            return []
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier JSON : {e}")
        return []


def executer_avec_failover(username, liste_cles):
    """Tente d'exécuter le scraper. En cas de panne de crédit, bascule sur la clé suivante."""
    while len(liste_cles) > 0:
        cle_actuelle = liste_cles[0]
        print(f"🔑 Utilisation de la clé : ...{cle_actuelle[-6:]}")

        try:
            client = ApifyClient(cle_actuelle)
            run_input = {
                "profiles": [username],
                "resultsPerPage": 5,
                "shouldDownloadVideos": False,
            }

            run = client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
            dataset_id = run.default_dataset_id
            return client.dataset(dataset_id).iterate_items()

        except ApifyApiError as e:
            if e.status_code in [401, 402] or "credit" in str(e).lower():
                print(f"⚠️ Clé épuisée ou invalide (...{cle_actuelle[-6:]}). Bascule sur la suivante...")
                liste_cles.pop(0)
            else:
                raise e
        except Exception as e:
            print(f"❌ Erreur réseau ou inconnue avec cette clé : {e}")
            liste_cles.pop(0)

    print("🚨 BLOCAGE : Toutes les clés API du fichier JSON ont été épuisées !")
    return None


def generer_rss_pour_createur(username, liste_cles):
    print(f"\n🚀 [TikTok-RSS] Traitement du créateur : @{username}")

    items = executer_avec_failover(username, liste_cles)
    if items is None:
        return

    try:
        videos_valides = []
        for item in items:
            # Gestion des messages d'erreur renvoyés par l'acteur (profil privé, supprimé, etc.)
            if "errorCode" in item:
                print(f"⚠️ Erreur détectée pour @{username} : {item.get('error')} ({item.get('errorCode')})")
                continue

            is_pinned = (
                item.get("isPinned") is True or
                item.get("isTop") is True or
                item.get("pinType") is not None
            )

            if is_pinned:
                print(f"📌 Vidéo épinglée ignorée pour @{username}")
                continue

            videos_valides.append(item)
            if len(videos_valides) == 2:
                break

        if not videos_valides:
            print(f"⚠️ Aucune vidéo récente trouvée pour @{username}")
            return

        # Construction du XML RSS
        ET.register_namespace("media", "http://search.yahoo.com/mrss/")
        
        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = f"TikTok RSS - {username}"
        ET.SubElement(channel, "link").text = f"https://tiktok.com/@{username}"
        ET.SubElement(channel, "description").text = f"Les 2 dernières vidéos non épinglées de {username}"
        ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

        for video in videos_valides:
            item = ET.SubElement(channel, "item")
            texte = video.get("text", "Vidéo TikTok")
            titre = texte[:50] + "..." if len(texte) > 50 else texte

            ET.SubElement(item, "title").text = titre
            lien = video.get("webVideoUrl", f"https://tiktok.com/@{username}")
            ET.SubElement(item, "link").text = lien
            ET.SubElement(item, "guid").text = lien
            ET.SubElement(item, "description").text = f"{texte} (Vues: {video.get('playCount', 0)})"

            # 🖼️ Extraction de la miniature via videoMeta (selon la documentation)
            video_meta = video.get("videoMeta", {})
            url_miniature = (
                video_meta.get("coverUrl") or
                video_meta.get("originalCoverUrl")
            )

            if url_miniature:
                ET.SubElement(item, "enclosure", {"url": url_miniature, "type": "image/jpeg"})
                ET.SubElement(item, "{http://search.yahoo.com/mrss/}content", {"url": url_miniature, "medium": "image", "type": "image/jpeg"})
            else:
                print(f"⚠️ Miniature introuvable dans videoMeta pour la vidéo.")

            date_iso = video.get("createTimeISO")
            if date_iso:
                date_iso = date_iso.replace("Z", "+00:00")
                dt = datetime.fromisoformat(date_iso)
                ET.SubElement(item, "pubDate").text = dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

        os.makedirs("rss", exist_ok=True)
        xml_string = ET.tostring(rss, encoding="utf-8")
        xml_pretty = minidom.parseString(xml_string).toprettyxml(indent="  ", encoding="utf-8")

        chemin_fichier = os.path.join("rss", f"{username}.xml")
        with open(chemin_fichier, "wb") as f:
            f.write(xml_pretty)

        print(f"✅ Fichier créé avec succès : {chemin_fichier}")

    except Exception as e:
        print(f"❌ Erreur lors de la génération du XML pour @{username} : {e}")


if __name__ == "__main__":
    if not os.path.exists(CHEMIN_CSV):
        print(f"❌ Fichier {CHEMIN_CSV} introuvable.")
        exit(1)

    cles_disponibles = charger_cles_api()
    if not cles_disponibles:
        exit(1)

    with open(CHEMIN_CSV, mode="r", encoding="utf-8") as f:
        lecteur = csv.reader(f)
        for ligne in lecteur:
            if ligne and ligne[0].strip():
                createur = ligne[0].strip().replace(",", "")
                if not cles_disponibles:
                    print("🚨 Arrêt du script : Plus aucune clé API valide disponible.")
                    break
                generer_rss_pour_createur(createur, cles_disponibles)