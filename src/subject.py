import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import Tk, filedialog
import os

def calculate_svd(A):
    """
    Calcul manuel de la SVD d'une matrice A.
    Utilise les valeurs propres de A.T @ A et A @ A.T
    """
    AtA = A.T @ A
    AAt = A @ A.T

    eigvals_V, V = np.linalg.eigh(AtA)
    eigvals_U, U = np.linalg.eigh(AAt)

    # Tri décroissant des valeurs propres
    idx            = np.argsort(eigvals_V)[::-1]
    eigvals_sorted = eigvals_V[idx]
    V              = V[:, idx]

    # Valeurs singulières
    singular_values = np.sqrt(np.clip(eigvals_sorted, 0, None))

    # Suppression des valeurs singulières nulles ou très faibles
    nonzero_mask = singular_values > 1e-10
    Sigma        = singular_values[nonzero_mask]
    V            = V[:, nonzero_mask]
    U            = A @ V / Sigma

    return U, Sigma, V.T

def compress_image(U, S, Vt, k):
    """
    Recompose une approximation de l’image avec les k premiers vecteurs.
    """
    U_k  = U[:, :k]
    S_k  = np.diag(S[:k])
    Vt_k = Vt[:k, :]
    return U_k @ S_k @ Vt_k

def erreur_mse(original, approx):
    """
    Calcule l’erreur quadratique moyenne (MSE).
    """
    return np.mean((original - approx) ** 2)

def choisir_k_pour_energie(S, seuil=0.90):
    """
    Choisit le plus petit k tel que l'énergie cumulée atteint le seuil.
    """
    energie_totale  = np.sum(S ** 2)
    energie_cumulee = np.cumsum(S ** 2)
    k               = np.searchsorted(energie_cumulee, seuil * energie_totale) + 1
    return k

# === Main ===

#Sélection interactive de l'image ===

# Ouvre une boîte de dialogue pour choisir un fichier image
Tk().withdraw()  # Cache la fenêtre principale de Tkinter
image_path = filedialog.askopenfilename(
    title="Choisir une image",
    filetypes=[("Fichiers image", "*.jpg *.jpeg *.png *.bmp *.tiff")]
)

if not image_path:
    raise Exception("Aucune image sélectionnée.")


# Chargement de l’image en niveaux de gris
image = Image.open(image_path).convert('L')
A     = np.asarray(image, dtype = np.float64)

# Calcul SVD
U, S, Vt = calculate_svd(A)

# Test avec plusieurs valeurs de k
ks        = [5, 20, 50, 100]
fig, axes = plt.subplots(2, len(ks), figsize = (15, 6))

for i, k in enumerate(ks):
    Ak  = compress_image(U, S, Vt, k)
    mse = erreur_mse(A, Ak)

    axes[0, i].imshow(Ak, cmap = 'gray')
    axes[0, i].set_title(f'k = {k}')
    axes[0, i].axis('off')

    axes[1, i].text(0.5, 0.5, f"MSE:\n{mse:.2f}", ha = 'center', va = 'center')
    axes[1, i].set_xticks([])
    axes[1, i].set_yticks([])
    axes[1, i].set_title(f'Erreur pour k = {k}')

plt.suptitle("Compression d'image par SVD manuelle", fontsize = 16)
plt.tight_layout()
plt.show()

# Compression automatique pour un seuil d’énergie
seuil    = 0.90
k_auto   = choisir_k_pour_energie(S, seuil)
A_auto   = compress_image(U, S, Vt, k_auto)
mse_auto = erreur_mse(A, A_auto)

plt.figure(figsize = (6, 5))
plt.imshow(A_auto, cmap = 'gray')
plt.title(f'Compression auto : k={k_auto} (90% énergie)')
plt.axis('off')
plt.show()

print(f"Pour conserver {int(seuil * 100)}% de l’énergie → k = {k_auto}")
print(f"Erreur MSE avec k = {k_auto} : {mse_auto:.2f}")
