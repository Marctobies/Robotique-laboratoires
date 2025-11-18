import torch
import time

def intensive_cuda_test(tensor_size=4096, num_iterations=100):
    """
    Effectue un test de charge intensif sur le GPU avec PyTorch et le compare au CPU.

    :param tensor_size: La taille des matrices carrées à multiplier.
    :param num_iterations: Le nombre de multiplications à effectuer.
    """
    print("--- Test de charge intensif pour CUDA avec PyTorch ---")

    # 1. Vérification de la disponibilité de CUDA
    if not torch.cuda.is_available():
        print("ERREUR : CUDA n'est pas disponible. Impossible de lancer le test intensif sur GPU.")
        return

    # --- Configuration des périphériques ---
    device_gpu = torch.device("cuda:0")
    device_cpu = torch.device("cpu")
    print(f"SUCCÈS : CUDA est disponible ! GPU détecté : {torch.cuda.get_device_name(0)}")

    print(f"\nConfiguration du test :")
    print(f"  - Taille des tenseurs : {tensor_size}x{tensor_size}")
    print(f"  - Nombre d'itérations : {num_iterations}")

    try:
        # --- Test sur CPU ---
        print("\n[1/2] Lancement du test sur CPU...")
        a_cpu = torch.randn(tensor_size, tensor_size, device=device_cpu)
        b_cpu = torch.randn(tensor_size, tensor_size, device=device_cpu)

        start_time_cpu = time.perf_counter()
        for _ in range(num_iterations):
            c_cpu = torch.matmul(a_cpu, b_cpu)
        end_time_cpu = time.perf_counter()
        cpu_time = end_time_cpu - start_time_cpu
        print(f"Temps d'exécution sur CPU : {cpu_time:.4f} secondes.")

        # Libérer la mémoire
        del a_cpu, b_cpu, c_cpu

        # --- Test sur GPU ---
        print("\n[2/2] Lancement du test sur GPU...")
        a_gpu = torch.randn(tensor_size, tensor_size, device=device_gpu)
        b_gpu = torch.randn(tensor_size, tensor_size, device=device_gpu)

        # Opération de chauffe pour s'assurer que le GPU est prêt
        torch.matmul(a_gpu, b_gpu)
        torch.cuda.synchronize() # Attendre la fin de l'opération de chauffe

        start_time_gpu = time.perf_counter()
        for _ in range(num_iterations):
            c_gpu = torch.matmul(a_gpu, b_gpu)
        # IMPORTANT: Attendre que toutes les opérations sur le GPU soient terminées
        torch.cuda.synchronize()
        end_time_gpu = time.perf_counter()
        gpu_time = end_time_gpu - start_time_gpu
        print(f"Temps d'exécution sur GPU : {gpu_time:.4f} secondes.")

        # Afficher l'utilisation de la mémoire VRAM
        vram_allocated = torch.cuda.memory_allocated(device_gpu) / 1024**3 # en Go
        vram_reserved = torch.cuda.memory_reserved(device_gpu) / 1024**3 # en Go
        print(f"Mémoire VRAM allouée : {vram_allocated:.2f} Go")
        print(f"Mémoire VRAM réservée : {vram_reserved:.2f} Go")

        # Libérer la mémoire
        del a_gpu, b_gpu, c_gpu
        torch.cuda.empty_cache()

        # --- Conclusion ---
        print("\n--- Résultats du test ---")
        print(f"Facteur d'accélération (CPU / GPU) : x{cpu_time / gpu_time:.2f}")
        print("Conclusion : Le GPU est nettement plus rapide. Votre configuration CUDA est performante !")

    except Exception as e:
        print("\nERREUR : Une erreur est survenue lors du test intensif :")
        print(e)
        print("\nCela peut être dû à une mémoire VRAM insuffisante ('CUDA out of memory').")
        print("Essayez de réduire le 'tensor_size' dans le script.")

if __name__ == "__main__":
    # Vous pouvez ajuster la taille des tenseurs et le nombre d'itérations ici
    # Attention : une taille trop grande peut causer une erreur "out of memory"
    intensive_cuda_test(tensor_size=4096, num_iterations=100)
