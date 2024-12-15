#descrição formal:
#conjunto de estados
#alfabeto de entrada
#função de transição: Structure: {(current_state, input_symbol, pop_symbol): [(next_state, push_symbols)]}
#estado inicial
#estado final

#descrição instantânea: com essas três coisas podemos descrever qualquer estado de um autômato com pilha naquele momento:
#um estado (estado ativo naquele momento) 
#uma cadeia w (que vai ser o restante da entrada, ou seja, o que ainda não foi lido. chegamos nesse estado lendo alguma coisa, mas o que ainda nao foi lido estará aqui para lembrar).
#cadeia com elementos da pilha, com o topo à direita



class Lsystem:
  def __init__(self, alfabeto, axioma, regras):
    self.alfabeto = alfabeto
    self.axioma = axioma
    self.regras = regras

class Estado:
  def __init__ (self)

class Transicao:
  def __init__ (self, estado_atual, simbolo_da_entrada, simbolo_desempilhavel):
    self.estado_atual = estado_atual
    self.simbolo_da_entrada = simbolo_da_entrada
    self.simbolo_desempilhavel = simbolo_desempilhavel



  def executar_transicao(self):
     

class Automato:
  def __init__(self, 
              estados: Set[str],
              alfabeto_da_entrada: Set[str], 
              alfabeto_da_pilha: Set[str], 
              estado_inicial: str,
              estados_finais: Set[str]):
  
  def rodar_automato(self, transicao: Transicao, ):



if __name__ = "__main__":

alfabeto = {"F", "+", "-"}
axioma = 'F'
estado_inicial = 