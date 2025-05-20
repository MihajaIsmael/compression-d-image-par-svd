import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# === 1. Charger et convertir l'image en niveaux de gris ===
image_path = '../images/image.jpg'                               # Mettre le nom exact de l’image
img        = Image.open(image_path).convert('L')              # Conversion en niveaux de gris
A          = np.asarray(img, dtype = np.float64)                # Matrice de l’image

# === 2. Calcul de la SVD de l’image ===
U, S, Vt = np.linalg.svd(A, full_matrices = False)

# === 3. Fonction de reconstruction par somme de matrices de rang 1 ===
def approx_rang_k(U, S, Vt, k):
    """
    Recompose l'image avec une approximation de rang k
    A_k = somme des k premières matrices de rang 1
    """
    m, n  = U.shape[0], Vt.shape[1]
    A_k   = np.zeros((m, n))
    for i in range(k):
        A_k += S[i] * np.outer(U[:, i], Vt[i, :])
    return A_k

# === 4. Fonction pour calculer l'erreur quadratique moyenne (MSE) ===
def erreur_mse(original, approx):
    return np.mean((original - approx) ** 2)

# === 5. Tester plusieurs valeurs de k ===
ks = [5, 20, 50, 100, 200]
fig, axes = plt.subplots(2, len(ks), figsize = (15, 6))

for i, k in enumerate(ks):
    Ak  = approx_rang_k(U, S, Vt, k)                       # Image approximée
    mse = erreur_mse(A, Ak)                                # Erreur de reconstruction

    # Affichage image
    axes[0, i].imshow(Ak, cmap = 'gray')
    axes[0, i].set_title(f'k={k}')
    axes[0, i].axis('off')

    # Affichage de l'erreur
    axes[1, i].text(0.5, 0.5, f"MSE:\n{mse:.2f}", fontsize = 12,
                ha = 'center', va = 'center')
    axes[1, i].set_xticks([])
    axes[1, i].set_yticks([])
    axes[1, i].set_title(f'Erreur pour k={k}')

plt.suptitle('Compression d’image par SVD de rang k', fontsize = 16)
plt.tight_layout()
plt.show()

# === 6. Tâche avancée : Choix automatique de k pour un pourcentage d’énergie donné ===
def choisir_k_pour_energie(S, seuil = 0.90):
    """
    Calcule le plus petit k tel que la somme des S[:k]² >= seuil * somme totale
    """
    energie_totale  = np.sum(S ** 2)
    energie_cumulee = np.cumsum(S ** 2)
    k               = np.searchsorted(energie_cumulee, seuil * energie_totale) + 1
    return k

# === Exemple : choisir k pour 90% d’énergie conservée ===
seuil  = 0.90
k_auto = choisir_k_pour_energie(S, seuil)

print(f"Pour conserver {int(seuil * 100)}% de l'énergie, il faut k = {k_auto}")

# === Reconstruction avec ce k optimal ===
A_k_auto = approx_rang_k(U, S, Vt, k_auto)

# === Affichage image et erreur ===
plt.figure(figsize = (6, 5))
plt.imshow(A_k_auto, cmap = 'gray')
plt.title(f'Compression auto : k={k_auto} (90% énergie)')
plt.axis('off')
plt.show()

# Affichage de l'erreur
mse_auto = erreur_mse(A, A_k_auto)
print(f"Erreur MSE avec k={k_auto} : {mse_auto:.2f}")
