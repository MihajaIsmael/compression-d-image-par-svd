# 📷 Compression d’image par SVD de rang k
<!-- Titre principal du projet -->

## 👥 Contributeurs
- ANDRIANARIVONY Heritsihoarana Kevin
- Mouandhui IBADA
- RANARIMANANA Liana Miotisoa
- RAVALOMANDA Andrianarimihaja Ismael

## 🎯 Objectif du projet
Ce projet applique la **décomposition en valeurs singulières (SVD)** à une image en niveaux de gris pour la **compresser**.

Fonctionnalités :
- Reconstruction de l’image avec différents rangs `k`
- Calcul de l’erreur de compression (MSE)
- Détermination automatique du plus petit `k` conservant un **seuil d’énergie donné** (par défaut : 90 %)
- Animation progressive de la compression
- Interface interactive pour sélectionner l’image à compresser

---

## 🧰 Bibliothèques utilisées
- `numpy` → calcul numérique (SVD, tableaux…)  
- `matplotlib` → affichage des images, courbes, animation  
- `Pillow` → lecture et conversion d’image  
- `tkinter` → sélection interactive de l’image (inclus dans la bibliothèque standard Python, nécessite `python3-tk` sous Linux)

---

## 📁 Structure du projet

```text
racine_du_projet/
│
├── images/
│   └── image.jpg        # Image test à compresser
│
├── src/
│   └── default.py       # Script par défaut pour comparaison
│   └── subject.py       # Script de l'exercice (le code Python du projet)
│
└── README.md            # Ce fichier d'explication

```
## ▶️ Exécution

Installer les dépendances:

```bash
pip install -r requirements.txt
```
Sous Linux, installer également Tkinter si besoin :

```bash
sudo apt-get install python3-tk
```

Puis pour lancer la compression, depuis le dossier `src`, lance le script avec :

```bash
python subject.py
```
Ou simplement depuis la racine du projet avec:

```bash
python src/subject.py
```