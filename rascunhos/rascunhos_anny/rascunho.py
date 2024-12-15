from typing import Dict, Set, List, Tuple, Callable
from dataclasses import dataclass, field

@dataclass
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
  estado_origem: Estado
  estado_destino: Estado
  simbolo_leitura: str
  simbolo_pilha: str
  simbolos_empilhar: List[str]

  def aplicar(self, pilha: List[str]) -> List[str]:
    # Remove o símbolo do topo da pilha se necessário
    if pilha and self.simbolo_pilha and pilha[-1] == self.simbolo_pilha:
      pilha.pop()
    # Empilha novos símbolos (em ordem reversa)
    pilha.extend(reversed(self.simbolos_empilhar))
    return pilha

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
  estados: Set[Estado]
  alfabeto_entrada: Set[str]
  alfabeto_pilha: Set[str]
  estado_inicial: Estado
  estado_final: Estado
  transicoes: List[Transicao] = field(default_factory=list)


  
  
  def validar_cadeia(self, cadeia: str) -> bool:
    estado_atual = self.estado_inicial
    pilha: List[str] = ['$']  # Símbolo inicial de pilha
    
    for simbolo in cadeia:
      # Encontra transições válidas
      transicoes_validas = [
        t for t in self.transicoes 
        if (t.estado_origem == estado_atual and 
            t.simbolo_leitura == simbolo and 
            (not t.simbolo_pilha or
             not pilha or 
             t.simbolo_pilha == pilha[-1]))
      ]

      if not transicoes_validas:
        return False
      
      # Escolhe a primeira transição válida (pode ser modificado para ser mais específico)
      transicao = transicoes_validas[0]
      
      # Aplica a transição
      pilha = transicao.aplicar(pilha)
      estado_atual = transicao.estado_destino
    # Verifica se chegou ao estado final com pilha vazia
    return estado_atual == self.estado_final and pilha == ['$']

  def construir_transicoes(self, n: int) -> List[Transicao]:
    transicoes = []
    
    transicoes.append(Transicao(self.estado, self.estado, '', '$', [f'{simbolo},0' for simbolo in axioma] + ['$']))

    # Regras: e, X_i → [produção de X_i com níveis incrementados]
    for simbolo, producao in self.l_system.regras_producao.items():
      for i in range(n):
          transicoes.append(Transicao(
              self.estado, self.estado, '', f'{simbolo},{i}', [f'{s},{i+1}' for s in producao]
          ))
    
    
     # Regras: +, e → e e -, e → e
    for constante in self.l_system.simbolos_constantes:
        transicoes.append(Transicao(self.estado, self.estado, constante, '', []))

    # Regras: X, X_n → e (para cada símbolo não-terminal X)
    for simbolo in self.l_system.simbolos_nao_terminais:
        for i in range(n):
            transicoes.append(Transicao(
                self.estado, self.estado, simbolo, f'{simbolo},{i}', []
            ))

    return transicoes

def debug_validacao(cadeia: str, automato: AutomatoPilha):
  estado_atual = automato.estado_inicial
  pilha: List[str] = ['$']  # Símbolo inicial de pilha
  
  print(f"Iniciando validação da cadeia: {cadeia}")
  print(f"Estado inicial: {estado_atual.identificador}")
  print(f"Pilha inicial: {pilha}")
  
  for i, simbolo in enumerate(cadeia):
    print(f"\nProcessando símbolo {i}: {simbolo}")
    
    # Encontra transições válidas
    transicoes_validas = [
        t for t in automato.transicoes 
        if (t.estado_origem == estado_atual and 
            t.simbolo_leitura == simbolo and 
            (not pilha or t.simbolo_pilha == pilha[-1]))
    ]
    
    print(f"Transições válidas encontradas: {len(transicoes_validas)}")
    
    if not transicoes_validas:
      print(f"Nenhuma transição válida encontrada para o símbolo {simbolo}")
      print(f"Estado atual: {estado_atual.identificador}")
      print(f"Pilha atual: {pilha}")
      return False
    
    # Escolhe a primeira transição válida
    transicao = transicoes_validas[0]
    
    print(f"Transição escolhida:")
    print(f"  Origem: {transicao.estado_origem.identificador}")
    print(f"  Destino: {transicao.estado_destino.identificador}")
    print(f"  Símbolo de leitura: {transicao.simbolo_leitura}")
    print(f"  Símbolo desempilhavel: {transicao.simbolo_pilha}")
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


def gerar_alfabeto_da_pilha(n, alfabeto_lsystem):
  variaveis = {
      simbolo: tipo for simbolo, tipo in alfabeto_lsystem.items() 
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

  q0 = Estado('q0', eh_estado_inicial=True)
  q1 = Estado('q1')
  q2 = Estado('q2')
  qf = Estado('qf', eh_estado_final=True)

  #colocar isso em outro arquivo
  alfabeto_lsystem = {'F': 'variavel', '+': 'constante', '-': 'constante'}
  #INPUT
  l_system = LSystem(
    alfabeto_lsystem = alfabeto_lsystem,
    axioma='F',
    regras_producao={'F': 'F+F-F-F+F'}
  )
  #INPUT
  n = 2

  cadeia = l_system.gerar_cadeia(n)
  print("Cadeia gerada:", cadeia)

  alfabeto_pilha = gerar_alfabeto_da_pilha(n,alfabeto_lsystem)
  print("Alfabeto lsystem:", alfabeto_lsystem)

  transicoes = [
      Transicao(q0, q1, '', '$', ['', '$']),  # Primeira A
        Transicao(q1, q1, 'B', 'A', []),          # B
        Transicao(q1, qf, 'A', '$', []),          # Última A
        Transicao(qf, qf, 'A', '', [])            # Transição adicional para qf
  ]

  # Criação do autômato com pilha
  automato = AutomatoPilha(
      estados={q0, q1, qf},
      alfabeto_entrada={'A', 'B'},
      alfabeto_pilha={'a', 'b', '$'},
      estado_inicial=q0,
      estado_final=qf,
      transicoes=transicoes
  )

  # Valida a cadeia com depuração
  debug_validacao(cadeia, automato)

# Executa a demonstração
demonstrar_validacao()