# Projeto de Sistemas Distribuídos e Paralelos

Contagem de números primos em um intervalo, nas versões sequencial e paralela.

## Uso

### Sequencial

```bash
python3 sequencial.py <inicio> <fim>
```

Exemplo da medição oficial:

```bash
python3 sequencial.py 1 50000000
```

### Paralelo

```bash
python3 paralelo.py <inicio> <fim> [processos]
```

O terceiro argumento é opcional e, se omitido, usa 2 processos.

Exemplo da medição oficial na EC2 `t3.micro` (2 vCPUs):

```bash
python3 paralelo.py 1 50000000 2
```

Exemplo para uma demonstração menor:

```bash
python3 sequencial.py 1 5000000
python3 paralelo.py 1 5000000 2
```
