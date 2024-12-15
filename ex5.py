from typing import Dict, Set, List, Tuple, Callable
from dataclasses import dataclass, field

@dataclass
class Transicao:
  estado_origem: str
  estado_destino: str
  simbolo_leitura: str
  simbolo_desempilhavel: str
  simbolos_empilhar: List[str]

  def aplicar(self, pilha: List[str]) -> List[str]:
    # Remove o símbolo do topo da pilha se necessário
    if pilha and self.simbolo_desempilhavel and pilha[-1] == self.simbolo_desempilhavel:
      pilha.pop()
    
    # Empilha novos símbolos (em ordem reversa)
    pilha.extend(reversed(self.simbolos_empilhar))
    return pilha
  
  def __repr__(self):
    return (
      f"Transicao(\n"
      f"  estado_origem='{self.estado_origem}',\n"
      f"  estado_destino='{self.estado_destino}',\n"
      f"  simbolo_leitura='{self.simbolo_leitura}',\n"
      f"  simbolo_desempilhavel='{self.simbolo_desempilhavel}',\n"
      f"  simbolos_empilhar={self.simbolos_empilhar}\n"
      f")"
    )

@dataclass
class LSystem:
  alfabeto: Set[str]
  axioma: str
  regras_producao: Dict[str, str]
  
  def gerar_cadeia(self, iteracoes: int) -> str:
    cadeia_atual = self.axioma
    
    for _ in range(iteracoes):
      nova_cadeia = ""
      for simbolo in cadeia_atual:
          nova_cadeia += self.regras_producao.get(simbolo, simbolo)
      cadeia_atual = nova_cadeia
    return cadeia_atual

@dataclass
class AutomatoPilha:

  l_system: LSystem
  alfabeto_pilha: Set[str]
  estado_inicial: str
  estado_intermediario: str
  estado_final: str
  numero_niveis: int

  def validar_cadeia(self, cadeia: str, transicoes: List[Transicao]) -> bool:
    estado_atual = self.estado_inicial
    pilha: List[str] = ['$']  # simbolo inicial de pilha
    print(f"Iniciando validação da cadeia: {cadeia}")
    
    i = 0  #posicao atual de iteracao da cadeia

    while i <= len(cadeia):
       if i < len(cadeia):
            simbolo = cadeia[i]
       else:
            simbolo = '' 
            
       print(estado_atual)

       transicoes_validas = [
          t for t in transicoes 
            if (t.estado_origem == estado_atual and t.simbolo_desempilhavel == '$')
              or ((t.estado_origem == self.estado_intermediario and 
                  t.simbolo_leitura == simbolo and 
                  (not t.simbolos_empilhar or
                  not pilha or 
                  t.simbolo_desempilhavel == pilha[-1])))
              or ((t.estado_origem == self.estado_intermediario and  
                  t.simbolo_desempilhavel == pilha[-1]))
        ]      
       if not transicoes_validas:
          return False
       transicao = transicoes_validas[0]
       print(transicao)

       if (transicao.simbolo_leitura != '' or simbolo == ''):
        i += 1  
       pilha = transicao.aplicar(pilha)
       estado_atual = transicao.estado_destino
       print(f"Pilha após transição: {pilha}")
       
    # Verifica se chegou ao estado final com pilha vazia
    return estado_atual == self.estado_final and pilha == []



  def construir_transicoes(self) -> List[Transicao]:
    transicoes = []
    
    transicoes.append(Transicao(self.estado_inicial, self.estado_intermediario, '', '$', [f'{simbolo},0' for simbolo in self.l_system.axioma if self.l_system.alfabeto.get(simbolo) == 'variavel'] + ['$']))

    for simbolo, producao in self.l_system.regras_producao.items():
      for i in range(self.numero_niveis):

        simbolos_empilhar = [f'{s},{i+1}' for s in producao if self.l_system.alfabeto.get(s) == 'variavel']
        transicoes.append(Transicao(
          self.estado_intermediario, self.estado_intermediario, '', f'{simbolo},{i}', simbolos_empilhar
        ))
    
    for simbolo, tipo in self.l_system.alfabeto.items():
      if tipo == 'constante':
        transicoes.append(Transicao(self.estado_intermediario, self.estado_intermediario, simbolo, '', []))

    for simbolo, tipo in self.l_system.alfabeto.items():
      if tipo == 'variavel':
        transicoes.append(Transicao(
            self.estado_intermediario, self.estado_intermediario, simbolo, f'{simbolo},{self.numero_niveis}', []
        ))

    transicoes.append(Transicao(self.estado_intermediario, self.estado_final, '', '$', []))
            
    print(transicoes)

    return transicoes


def gerar_alfabeto_da_pilha(n, alfabeto):
  #o alfabeto da  pilha vai ter so as variaveis
  variaveis = {
      simbolo: tipo for simbolo, tipo in alfabeto.items() 
      if tipo == 'variavel'
  }

  alfabeto_da_pilha = set()

  for nivel in range(n):
    nivel_atual = nivel + 1
    for simbolo in variaveis:
      alfabeto_da_pilha.add((simbolo, nivel_atual))
   
  return sorted(list(alfabeto_da_pilha))


# Função principal para demonstração
def demonstrar_validacao():

  #colocar isso em outro arquivo
  alfabeto = {'F': 'variavel', 'F': 'variavel', '+': 'constante', '-': 'constante'}
  
  l_system = LSystem(
    alfabeto = alfabeto,
    axioma='F',
    regras_producao={'F': 'F+F-F-F+F'}
  )
  #numero de iteracoes
  n = 2

  cadeia = l_system.gerar_cadeia(n)
  print("Cadeia gerada:", cadeia)

  alfabeto_pilha = gerar_alfabeto_da_pilha(n,alfabeto)
  print("Alfabeto lsystem:", alfabeto)
  print("Alfabeto da pilha:", alfabeto_pilha)

  automato = AutomatoPilha(
      estado_inicial='q0',
      estado_intermediario='q1',
      estado_final='q2',
      l_system=l_system,
      alfabeto_pilha=alfabeto_pilha,
      numero_niveis=n
  )

  transicoes = automato.construir_transicoes()

  resultado = automato.validar_cadeia(cadeia, transicoes)

  print("RESULTADO: ", resultado)

demonstrar_validacao()