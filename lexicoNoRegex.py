import sys
import re

DEFINICAO_TOKENS = [
    (r'\bint\b', 'tipo_variavel'),
    (r'[a-zA-Z][a-zA-Z0-9]*', 'identificador'),
    (r'\d+', 'numero'),
    (r'\+', 'soma'),
    (r'-', 'subtracao'),
    (r'\*', 'multiplicacao'),
    (r'/', 'divisao'),
    (r'=', 'atribuicao'),
    (r';', 'delimitador'),
    (r'\(', 'abre_parenteses'),
    (r'\)', 'fecha_parenteses'),
    (r'\s+', None)
]

def analise(pathArquivo):
    with open(pathArquivo, 'r') as f:
        linhas = f.readlines()
    
    tabela = []
    erro = ""
    for numeroDaLinha, linha in enumerate(linhas, 1):
        posicao = 0
        while posicao < len(linha):
            deuMatch = False
            for regra, tipo in DEFINICAO_TOKENS:
                m = re.match(regra, linha[posicao:])
                if m:
                    if tipo:
                        tabela.append({"tipo":tipo, "valor":m.group(0), "linha":numeroDaLinha})
                    posicao += len(m.group(0))
                    deuMatch = True
                    break
            if not deuMatch:
                if linha[posicao] not in ['\n','\r']:
                    erro = erro + f"Erro léxico na linha {numeroDaLinha}. Caractere inesperado:{linha[posicao]}\n"
                posicao += len(linha)
    return tabela, erro

tabela, erros = analise(sys.argv[1])

print(f"{'Tipo':<24} {'Valor':<20} {'Linha':<5}")
print('-'*60)
for token in tabela:
    print(f"{token['tipo']:<24} {token['valor']:<20} {token['linha']:<5}")

print(f"\n{erros}")        
