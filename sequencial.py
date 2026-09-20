import time
import math


def eh_primo(n):
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    limite = int(math.sqrt(n))

    for divisor in range(3, limite + 1, 2):
        if n % divisor == 0:
            return False

    return True


def contar_primos(inicio, fim):
    contador = 0

    for numero in range(inicio, fim + 1):
        if eh_primo(numero):
            contador += 1

    return contador


if __name__ == "__main__":
    inicio = 1
    fim = 50_000_000

    print(f"Procurando números primos de {inicio} até {fim}...")

    tempo_inicio = time.perf_counter()

    quantidade = contar_primos(inicio, fim)

    tempo_fim = time.perf_counter()

    print(f"\nQuantidade de primos: {quantidade}")
    print(f"Tempo: {tempo_fim - tempo_inicio:.2f} segundos")