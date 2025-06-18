# 📷 Compression d’image par SVD de rang k
<!-- Titre principal du projet -->

## 👥 Contributeurs
- ANDRIANARIVONY Heritsihoarana Kevin  sds
- Mouandhui IBADA
- RANARIMANANA Liana Miotisoa
- RAVALOMANDA Ismael

## 🎯 Objectif du projet
Ce projet applique la **décomposition en valeurs singulières (SVD)** à une image en niveaux de gris pour la **compresser**.

Il permet :
- de reconstruire l’image pour différents rangs `k`
- de calculer l’erreur de compression (MSE)
- de déterminer automatiquement le plus petit `k` conservant par exemple **90 % de l’énergie** de l’image

---

## 🧰 Bibliothèques utilisées
- `numpy` → calcul numérique (SVD, tableaux…)
- `matplotlib` → affichage des images et courbes
- `Pillow` → lecture et conversion d’image

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

Puis, depuis le dossier `src`, lance le script avec :

```bash
python subject.py
```
Ou simplement depuis la racine du projet avec:

```bash
python src/subject.py