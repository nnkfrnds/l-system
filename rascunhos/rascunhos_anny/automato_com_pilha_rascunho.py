from typing import Dict, Set, List
from dataclasses import dataclass

class Estado:
  identificador: str
  eh_estado_inicial: bool = False
  eh_estado_final: bool = False

  def __hash__(self):
    return hash(self.identificador)
  
  def __eq__(self, outro):
    return self.identificador == outro.identificador

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
    pilha.extend(reversed(self.simbolo_desempilhavel))
    return pilha
  def __repr__(self):
    return (
      f"Transicao(\n"
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
  estado_final: str

  def validar_cadeia(self, cadeia: str, transicoes: List[Transicao]) -> bool:
    
    pilha: List[str] = ['$']  # Símbolo inicial de pilha
     
    for simbolo in cadeia:
      # Encontra transições válidas
      transicoes_validas = [
        t for t in transicoes 
          if (t.estado_origem == self.estado_inicial and t.simbolo_desempilhavel == '$') or
                ((t.estado_origem == self.estado_final and 
                t.simbolo_leitura == simbolo and 
                (not t.simbolos_empilhar or
                not pilha or 
                t.simbolos_empilhar == pilha[-1])))
      ]

      if not transicoes_validas:
        return False

      transicao = transicoes_validas[0]
      
      # Aplica a transição
      pilha = transicao.aplicar(pilha)
      estado_atual = transicao.estado_destino
    # Verifica se chegou ao estado final com pilha vazia
    return estado_atual == self.estado_final and pilha == ['$']



  def construir_transicoes(self, n: int) -> List[Transicao]:
    transicoes = []
    
    transicoes.append(Transicao(self.estado_inicial, self.estado_final, '', '$', [f'{simbolo},0' for simbolo in self.l_system.axioma if self.l_system.alfabeto.get(simbolo) == 'variavel'] + ['$']))

    # Regras: e, X_i → [produção de X_i com níveis incrementados]
    for simbolo, producao in self.l_system.regras_producao.items():
      for i in range(n):

        simbolos_empilhar = [f'{s},{i+1}' for s in producao if self.l_system.alfabeto.get(s) == 'variavel']
        transicoes.append(Transicao(
          self.estado_final, self.estado_final, '', f'{simbolo},{i}', simbolos_empilhar
        ))
    
     # Regras: +, e → e e -, e → e
    for simbolo, tipo in self.l_system.alfabeto.items():
      if tipo == 'constante':
        transicoes.append(Transicao(self.estado_final, self.estado_final, simbolo, '', []))

    # Regras: X, X_n → e (para cada símbolo não-terminal X)
    for simbolo, tipo in self.l_system.alfabeto.items():
      if tipo == 'variavel':
        transicoes.append(Transicao(
            self.estado_final, self.estado_final, simbolo, f'{simbolo},{n}', []
        ))
    #talvez nao precise dessa
    transicoes.append(Transicao(self.estado_final, self.estado_final, '', '$', []))
            
    print(transicoes)

    return transicoes

def debug_validacao(cadeia: str, automato: AutomatoPilha, transicoes: List[Transicao]):
  estado_atual = automato.estado_inicial
  pilha: List[str] = ['$']  # Símbolo inicial de pilha
  
  print(f"Iniciando validação da cadeia: {cadeia}")
  print(f"Estado inicial: {estado_atual}")
  print(f"Pilha inicial: {pilha}")
  
  for i, simbolo in enumerate(cadeia):
    print(f"\nProcessando símbolo {i}: {simbolo}")
    
    # Encontra transições válidas
    transicoes_validas = [
        t for t in transicoes 
        if (t.estado_origem == estado_atual and 
            t.simbolo_leitura == simbolo and 
            (not pilha or t.simbolo_desempilhavel == pilha[-1]))
    ]
    
    print(f"Transições válidas encontradas: {len(transicoes_validas)}")
    
    if not transicoes_validas:
      print(f"Nenhuma transição válida encontrada para o símbolo {simbolo}")
      print(f"Estado atual: {estado_atual}")
      print(f"Pilha atual: {pilha}")
      return False
    
    # Escolhe a primeira transição válida
    transicao = transicoes_validas[0]
    
    print(f"Transição escolhida:")
    print(f"  Origem: {transicao.estado_origem.identificador}")
    print(f"  Destino: {transicao.estado_destino.identificador}")
    print(f"  Símbolo de leitura: {transicao.simbolo_leitura}")
    print(f"  Símbolo desempilhavel: {transicao.simbolo_desempilhavel}")
    print(f"  Símbolos a empilhar: {transicao.simbolos_empilhar}")
    
    # Aplica a transição
    pilha = transicao.aplicar(pilha.copy())
    estado_atual = transicao.estado_destino
    
    print(f"Pilha após transição: {pilha}")
    print(f"Estado atual: {estado_atual.identificador}")
 
  # Verifica se chegou ao estado final com pilha vazia
  resultado_final = estado_atual == automato.estado_final and pilha == ['$']
  
  print("\nValidação concluída:")
  print(f"Estado final: {estado_atual.identificador}")
  print(f"Pilha final: {pilha}")
  print(f"Resultado: {resultado_final}")
  
  return resultado_final


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
  #INPUT
  l_system = LSystem(
    alfabeto = alfabeto,
    axioma='F',
    regras_producao={'F': 'F+F-F-F+F'}
  )
  #INPUT
  n = 2

  cadeia = l_system.gerar_cadeia(n)
  print("Cadeia gerada:", cadeia)

  alfabeto_pilha = gerar_alfabeto_da_pilha(n,alfabeto)
  #variaveis e constantes
  print("Alfabeto lsystem:", alfabeto)
  #so variaveis
  print("Alfabeto da pilha:", alfabeto_pilha)

  #Criação do autômato com pilha
  automato = AutomatoPilha(
      estado_inicial='q0',
      estado_final='q1',
      l_system=l_system,
      alfabeto_pilha=alfabeto_pilha,
  )

  transicoes = automato.construir_transicoes(n)

  resultado = automato.validar_cadeia(cadeia, transicoes)


  # Valida a cadeia com depuração
  debug_validacao(cadeia, automato, transicoes)

# Executa a demonstração
demonstrar_validacao()