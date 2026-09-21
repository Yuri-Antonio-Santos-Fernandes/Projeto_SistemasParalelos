import argparse
import math
import time


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


def ler_argumentos():
    parser = argparse.ArgumentParser(
        description="Conta números primos em um intervalo usando execução sequencial."
    )
    parser.add_argument(
        "inicio",
        type=int,
        help="limite inferior do intervalo (inclusivo)",
    )
    parser.add_argument(
        "fim",
        type=int,
        help="limite superior do intervalo (inclusivo)",
    )

    args = parser.parse_args()

    if args.inicio > args.fim:
        parser.error("o valor de inicio deve ser menor ou igual ao valor de fim")

    return args.inicio, args.fim


if __name__ == "__main__":
    inicio, fim = ler_argumentos()

    print(f"Procurando números primos de {inicio} até {fim}...")

    tempo_inicio = time.perf_counter()

    quantidade = contar_primos(inicio, fim)

    tempo_fim = time.perf_counter()

    print(f"\nQuantidade de primos: {quantidade}")
    print(f"Tempo: {tempo_fim - tempo_inicio:.2f} segundos")
