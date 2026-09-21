import time
import math
import multiprocessing


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


def contar_primos(inicio, fim, contador_compartilhado, lock):
    tempo_inicio = time.perf_counter()

    contador_local = 0

    for numero in range(inicio, fim + 1):
        if eh_primo(numero):
            contador_local += 1

    tempo_fim = time.perf_counter()

    print(
        f"Intervalo {inicio} até {fim}: "
        f"{contador_local} primos em "
        f"{tempo_fim - tempo_inicio:.2f} segundos"
    )

    with lock:
        contador_compartilhado.value += contador_local


def dividir_intervalo(inicio, fim, quantidade_processos):
    total_numeros = fim - inicio + 1
    tamanho_base = total_numeros // quantidade_processos
    resto = total_numeros % quantidade_processos

    intervalos = []
    inicio_atual = inicio

    for i in range(quantidade_processos):
        tamanho = tamanho_base

        #distribuição dos números entre os primeiros processos
        if i < resto:
            tamanho += 1

        fim_atual = inicio_atual + tamanho - 1

        intervalos.append((inicio_atual, fim_atual))

        inicio_atual = fim_atual + 1

    return intervalos


if __name__ == "__main__":

    inicio = 1
    fim = 50_000_000

    quantidade_processos = 4

    print(f"Procurando números primos de {inicio} até {fim}...")
    print(f"Processos utilizados: {quantidade_processos}")

    #estado compartilhado entre todos os processos
    contador_compartilhado = multiprocessing.Value("i", 0)

    #sincronização
    lock = multiprocessing.Lock()

    #divide o trabalho entre os processos
    intervalos = dividir_intervalo(
        inicio,
        fim,
        quantidade_processos
    )

    print("\nIntervalos atribuídos:")

    for i, intervalo in enumerate(intervalos):
        print(
            f"Processo-{i + 1}: "
            f"{intervalo[0]} até {intervalo[1]}"
        )

    processos = []

    tempo_inicio = time.perf_counter()

    #cria os processos
    for intervalo in intervalos:

        processo = multiprocessing.Process(
            target=contar_primos,
            args=(
                intervalo[0],
                intervalo[1],
                contador_compartilhado,
                lock
            )
        )

        processos.append(processo)
        processo.start()

    #aguarda pelos processos terminarem
    for processo in processos:
        processo.join()

    tempo_fim = time.perf_counter()

    print("\nResultado:")
    print(
        f"Quantidade de primos: "
        f"{contador_compartilhado.value}"
    )

    print(
        f"Tempo: "
        f"{tempo_fim - tempo_inicio:.2f} segundos"
    )

