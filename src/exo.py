# === Importation des bibliothèques nécessaires ===
import numpy as np                    # Pour les calculs matriciels et SVD
import matplotlib.pyplot as plt      # Pour afficher les images
from PIL import Image                # Pour charger et convertir l'image

# === Chargement de l'image et conversion en niveaux de gris ===
image_path = 'vw.jpg'                # Nom du fichier image
img        = Image.open(image_path).convert('L')  # 'L' = niveaux de gris (luminance)
A          = np.asarray(img, dtype=np.float64)    # Conversion en matrice NumPy

# === Décomposition SVD de la matrice A ===
# A ≈ U × S × Vt (où S est un vecteur des valeurs singulières)
U, S, Vt = np.linalg.svd(A, full_matrices=False)

# === Fonction de compression d'image par approximation SVD de rang k ===
def compress_image(U, S, Vt, k):
    U_k  = U[:, :k]                  # Prendre les k premières colonnes de U
    S_k  = np.diag(S[:k])            # Transformer les k premières valeurs singulières en matrice diagonale
    Vt_k = Vt[:k, :]                 # Prendre les k premières lignes de Vt
    return np.dot(U_k, np.dot(S_k, Vt_k))  # Reconstitution de l'image compressée Ak

# === Liste des valeurs de k à tester (différents niveaux de compression) ===
ks = [5, 20, 50, 100, 200]

# === Création d'une figure avec plusieurs sous-figures (originale + compressées) ===
fig, axes = plt.subplots(1, len(ks) + 1, figsize=(15, 5))  # Une ligne, plusieurs colonnes

# === Affichage de l'image originale ===
axes[0].imshow(A, cmap='gray')       # Affiche l'image originale en niveaux de gris
axes[0].set_title('Original')        # Titre de l'image
axes[0].axis('off')                  # Masque les axes (x, y)

# === Affichage des images compressées avec différentes valeurs de k ===
for i, k in enumerate(ks):
    Ak = compress_image(U, S, Vt, k)              # Image compressée avec rang k
    axes[i + 1].imshow(Ak, cmap='gray')           # Affichage en niveaux de gris
    axes[i + 1].set_title(f'k={k}')               # Titre indiquant la valeur de k
    axes[i + 1].axis('off')                       # Masque les axes

# === Ajustement de la disposition et affichage final ===
plt.tight_layout()                   # Évite les chevauchements
plt.show()                           # Affiche la figure finale
