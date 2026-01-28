import os
import requests
import time
import random
from duckduckgo_search import DDGS
from urllib.parse import urlparse
import re

# ==========================================
# DICTIONNAIRE DES RECHERCHES
dictionnaire = {
    # --- CHASSEURS AMÉRICAINS ---
    "Chat": [
        "Chat", "Chaton"],
    "Chien": [
        "Chien", "Chiot"],
    "Poule": [
        "Poule", "Poussin"]
}
# ==========================================


def get_last_index(folder, prefix):
    files = [f for f in os.listdir(folder) if f.startswith(prefix) and "_" in f]
    if not files:
        return 0
    indices = []
    for f in files:
        try:
            match = re.search(r'_(\d+)\.', f)
            if match:
                indices.append(int(match.group(1)))
        except ValueError:
            continue
    return max(indices) if indices else 0


def telecharger_images(query, nom, nb_a_prendre):
    output_folder = os.path.join("data", "train", nom)
    os.makedirs(output_folder, exist_ok=True)

    current_idx = get_last_index(output_folder, nom) + 1

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."}
    count_success = 0

    try:
        with DDGS() as ddgs:
            results = ddgs.images(keywords=query, region="wt-wt", max_results=nb_a_prendre * 3)

            for r in results:
                if count_success >= nb_a_prendre:
                    break

                url = r.get("image")
                try:
                    res = requests.get(url, headers=headers, timeout=5)
                    if res.status_code == 200:
                        ext = os.path.splitext(urlparse(url).path)[1].lower()
                        if ext not in ['.jpg', '.jpeg', '.png']: ext = ".jpg"

                        filename = f"{nom}_{current_idx}{ext}"
                        full_path = os.path.join(output_folder, filename)

                        with open(full_path, "wb") as f:
                            f.write(res.content)

                        print(f"   [OK] {nom} : image {current_idx} ajoutée.")
                        current_idx += 1
                        count_success += 1
                        time.sleep(random.uniform(0.1, 0.3))
                except:
                    continue
    except Exception as e:
        print(f"⚠️ Erreur recherche : {e}")

    return count_success


if __name__ == "__main__":
    QUOTA_PAR_IMAGE = 1500

    for dictio, recherches in dictionnaire.items():
        output_folder = os.path.join("data", "train", dictio)
        os.makedirs(output_folder, exist_ok=True)

        print(f"\n🎯 ANALYSE : {dictio}")

        idx_rech = 0
        while True:
            images_actuelles = len(os.listdir(output_folder))
            besoin = QUOTA_PAR_IMAGE - images_actuelles

            if besoin <= 0:
                print(f"✅ Quota atteint ou dépassé pour {dictio} ({images_actuelles} images).")
                break

            query = recherches[idx_rech % len(recherches)]
            print(f"🔍 Dossier à {images_actuelles}/{QUOTA_PAR_IMAGE}. Lancement : {query}")

            telecharger_images(query, dictio, besoin)

            # Sécurité pour éviter la boucle infinie
            idx_rech += 1
            if idx_rech > len(recherches) * 2:
                print(f"🛑 Plus de résultats disponibles pour {dictio}.")
                break

            time.sleep(2)

    print("\n🏁 Recherche terminée.")