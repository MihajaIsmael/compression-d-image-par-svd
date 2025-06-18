import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import time

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

def taux_compression(m, n, k):
    original = m * n
    compresse = k * (m + n + 1)
    return 1 - (compresse / original)

def choisir_k_pour_energie(S, seuil=0.90):
    """
    Choisit le plus petit k tel que l'énergie cumulée atteint le seuil.
    """
    energie_totale  = np.sum(S ** 2)
    energie_cumulee = np.cumsum(S ** 2)
    k               = np.searchsorted(energie_cumulee, seuil * energie_totale) + 1
    return k

# === Main ===

# Chemin vers l’image
base_dir    = os.path.dirname(os.path.abspath(__file__))
image_path  = os.path.join(base_dir, '..', 'images', 'image.jpg')

# Chargement de l’image en niveaux de gris
image = Image.open(image_path).convert('L')
A     = np.asarray(image, dtype = np.float64)

# Calcul SVD
U, S, Vt = calculate_svd(A)

# === Tracé de l'énergie cumulée ===
energie = np.cumsum(S**2) / np.sum(S**2)
plt.figure(figsize=(8, 4))
plt.plot(range(1, len(S) + 1), energie, label="Énergie cumulée")
plt.axhline(y=0.90, color='red', linestyle='--', label='Seuil 90%')
plt.xlabel('k')
plt.ylabel('Énergie')
plt.title("Énergie cumulée en fonction de k")
plt.legend()
plt.grid(True)
plt.show()

# Test avec plusieurs valeurs de k
ks        = [5, 20, 50, 100]
fig, axes = plt.subplots(2, len(ks), figsize = (15, 6))

for i, k in enumerate(ks):
    Ak  = compress_image(U, S, Vt, k)
    mse = erreur_mse(A, Ak)
    tc = taux_compression(*A.shape, k)

    axes[0, i].imshow(Ak, cmap = 'gray')
    axes[0, i].set_title(f'k = {k}')
    axes[0, i].axis('off')

    #axes[1, i].text(0.5, 0.5, f"MSE:\n{mse:.2f}", ha = 'center', va = 'center')
    axes[1, i].text(0.5, 0.6, f"MSE:\n{mse:.2f}", ha = 'center', va = 'center')
    axes[1, i].text(0.5, 0.3, f"Compression:\n{tc:.2%}", ha = 'center', va = 'center')

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

choix = input("Choisissez le mode :\n1 → k manuel\n2 → seuil d’énergie (%)\n> ")

if choix == "1":
    k_user = int(input("Entrez la valeur de k : "))
    A_user = compress_image(U, S, Vt, k_user)
    mse_user = erreur_mse(A, A_user)
    tc_user = taux_compression(*A.shape, k_user)
    plt.figure(figsize=(6, 5))
    plt.imshow(A_user, cmap='gray')
    plt.title(f'k = {k_user} | MSE = {mse_user:.2f} | TC = {tc_user:.2%}')
    plt.axis('off')
    plt.show()
elif choix == "2":
    seuil_user = float(input("Entrez le seuil (ex: 0.9 pour 90%) : "))
    k_user = choisir_k_pour_energie(S, seuil_user)
    A_user = compress_image(U, S, Vt, k_user)
    mse_user = erreur_mse(A, A_user)
    tc_user = taux_compression(*A.shape, k_user)
    plt.figure(figsize=(6, 5))
    plt.imshow(A_user, cmap='gray')
    plt.title(f'k = {k_user} | MSE = {mse_user:.2f} | TC = {tc_user:.2%}')
    plt.axis('off')
    plt.show()


# === Animation de la compression de l’image ===

plt.figure(figsize=(6, 5))
plt.title("Animation de la compression (k croissant)")
for k in range(1, min(100, len(S)), 5):  # toutes les 5 valeurs pour aller vite
    Ak = compress_image(U, S, Vt, k)
    plt.imshow(Ak, cmap='gray')
    plt.title(f"Compression avec k = {k}")
    plt.axis('off')
    plt.pause(0.1)  # pause de 100 ms
plt.show()

print(f"Pour conserver {int(seuil * 100)}% de l’énergie → k = {k_auto}")
print(f"Erreur MSE avec k = {k_auto} : {mse_auto:.2f}")
