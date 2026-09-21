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


def primeiro_impar(inicio):
    """Retorna o primeiro número ímpar >= inicio e >= 3."""
    inicio = max(inicio, 3)
    return inicio if inicio % 2 == 1 else inicio + 1


def contar_primos_distribuidos(
    primeiro_numero,
    fim,
    passo,
    contador_compartilhado,
    lock,
    numero_processo,
):
    """
    Cada processo percorre números ímpares intercalados ao longo de todo
    o intervalo. Assim, todos recebem números pequenos e grandes, evitando
    que um único processo fique responsável apenas pela parte mais cara.
    """
    tempo_inicio = time.perf_counter()
    contador_local = 0

    for numero in range(primeiro_numero, fim + 1, passo):
        if eh_primo(numero):
            contador_local += 1

    tempo_fim = time.perf_counter()
    tempo_local = tempo_fim - tempo_inicio

    print(
        f"Processo-{numero_processo}: "
        f"{contador_local} primos em {tempo_local:.2f} segundos"
    )

    # Seção crítica: todos os processos escrevem no mesmo contador.
    # O lock protege somente a soma final de cada trabalhador.
    with lock:
        contador_compartilhado.value += contador_local


if __name__ == "__main__":
    inicio = 1
    fim = 50_000_000

    # A EC2 t3.micro utilizada no projeto possui 2 vCPUs.
    quantidade_processos = 2

    print(f"Procurando números primos de {inicio} até {fim}...")
    print(f"Processos utilizados: {quantidade_processos}")
    print("Estratégia: distribuição intercalada dos números ímpares")

    # O número 2 é tratado separadamente, pois os trabalhadores recebem
    # apenas ímpares. Usa 64 bits para suportar intervalos maiores.
    contador_inicial = 1 if inicio <= 2 <= fim else 0
    contador_compartilhado = multiprocessing.Value("q", contador_inicial)

    lock = multiprocessing.Lock()

    primeiro = primeiro_impar(inicio)
    passo = 2 * quantidade_processos

    processos = []

    print("\nTrabalho atribuído:")
    for i in range(quantidade_processos):
        inicio_processo = primeiro + (2 * i)
        print(
            f"Processo-{i + 1}: começa em {inicio_processo}, "
            f"passo {passo}, até {fim}"
        )

    tempo_inicio = time.perf_counter()

    for i in range(quantidade_processos):
        inicio_processo = primeiro + (2 * i)

        processo = multiprocessing.Process(
            target=contar_primos_distribuidos,
            args=(
                inicio_processo,
                fim,
                passo,
                contador_compartilhado,
                lock,
                i + 1,
            ),
        )

        processos.append(processo)
        processo.start()

    for processo in processos:
        processo.join()

    tempo_fim = time.perf_counter()

    print("\nResultado:")
    print(f"Quantidade de primos: {contador_compartilhado.value}")
    print(f"Tempo: {tempo_fim - tempo_inicio:.2f} segundos")
