# IMG-Dataset-Creator

Script Python permettant de télécharger automatiquement des images depuis DuckDuckGo Images afin de constituer un **dataset d’entraînement pour le Machine Learning / Deep Learning**.

---

## 📁 Structure générée

```bash
data/
└── train/
    ├── Chat/
    │   ├── Chat_1.jpg
    │   ├── Chat_2.jpg
    │   └── ...
    ├── Chien/
    └── Poule/
```

Chaque dossier correspond à une classe.  
Les images sont numérotées automatiquement sans écrasement.

---

## ⚙️ Prérequis

- Python **3.10+**
- Connexion internet

### Dépendances

```bash
pip install requests duckduckgo-search
```

---

## 🧠 Configuration des classes

Les catégories et leurs variantes sont définies dans un dictionnaire :

```python
dictionnaire = {
    "Chat": ["Chat", "Chaton"],
    "Chien": ["Chien", "Chiot"],
    "Poule": ["Poule", "Poussin"]
}
```

La qualité du dataset dépend directement de la pertinence des mots-clés utilisés.  
Des mots-clés médiocres produisent un dataset médiocre.

---

## 🎯 Quota d’images

```python
QUOTA_PAR_IMAGE = 1500
```

Le script :
- détecte les images déjà présentes
- télécharge uniquement celles manquantes
- s’arrête automatiquement lorsque le quota est atteint

---

## 🚀 Lancement

```bash
python dataset_scraper.py
```

Fonctionnement :
- alternance automatique des mots-clés
- téléchargement des images valides (`.jpg`, `.jpeg`, `.png`)
- gestion silencieuse des erreurs réseau
- délais aléatoires pour éviter les abus

---

## 🛡️ Limites et avertissements

- DuckDuckGo n’est pas une API officielle
- les images peuvent être bruitées ou mal labellisées

---
