import turtle
import time

class Alfabeto:
  def __init__(self):
    self.simbolos = {}

  def adicionar_novo_simbolo(self, valor, tipo, descricao, comando_turtle=None):
    self.simbolos[valor] = {"tipo": tipo, "descricao": descricao, "comando_turtle": comando_turtle}

  def adicionar_simbolos(self, simbolos):
    for simbolo in simbolos:
      self.adicionar_novo_simbolo(**simbolo)
  
  def obter_simbolo(self, valor):
        return self.simbolos.get(valor, None)

  def executar_turtle(self, valor, turtle):
    simbolo = self.simbolos.get(valor)
    if simbolo and callable(simbolo["comando_turtle"]):
      simbolo["comando_turtle"](turtle)
    else:
      raise ValueError(f"O símbolo '{valor}' não possui um comando Turtle válido.")

  def __repr__(self):
    return f"Alfabeto(simbolos={list(self.simbolos.keys())})"

class Lsystem:
  def __init__(self, alfabeto: Alfabeto, axioma:str, regras:dict):
    self.alfabeto = alfabeto
    self.axioma = axioma
    self.regras = regras

    self.cadeia_obtida = ""

    # Configuração da tela Turtle
    self.screen = turtle.Screen()  
    self.screen.setup(width=600, height=600)  
    self.turtle = turtle.Turtle()
    self.turtle.speed(100)
    self.turtle.penup()  #
    self.turtle.setpos(-self.screen.window_width() / 2, -self.screen.window_height() / 2)  
    self.turtle.pendown()
    
  
  def gerar_sequencia_lsystem(self, iteracoes):
    cadeia_obtida = self.axioma
    for _ in range(iteracoes):
      cadeia_obtida = "".join(self.regras.get(simbolo, simbolo) for simbolo in cadeia_obtida)
      print(cadeia_obtida)
    self.cadeia_obtida = cadeia_obtida
    

  def desenhar(self):
    for simbolo in self.cadeia_obtida:
      self.alfabeto.executar_turtle(simbolo, self.turtle)
      turtle.update()  # Atualiza o desenho

    turtle.done()

    

def tratar_regras(regras_str):
  regras = {}
  for regra in regras_str.split(','):
    chave, valor = regra.split(':')
    regras[chave] = valor
  return regras

def comando_avancar(t):
  t.color("blue")
  t.forward(10)

def comando_rotacionar_direita(t):
    t.right(90)

def comando_rotacionar_esquerda(t):
    t.left(90)


if __name__ == "__main__":
  
  alfabeto = Alfabeto()
  alfabeto.adicionar_simbolos([
      {"valor": "F", "tipo": "variavel","descricao": "avancar para frente","comando_turtle": comando_avancar},
      {"valor": "+", "tipo": "constante","descricao": "rotacionar a esquerda 90 graus","comando_turtle":comando_rotacionar_esquerda},
      {"valor": "x", "tipo": "constante","descricao": "rotacionar a direita 90 graus", "comando_turtle":comando_rotacionar_direita}
  ])
  print(alfabeto)

  n = 4

  regras = tratar_regras("F:F+FxFxF+F")
  axioma = "F"

  koch_curve = Lsystem(alfabeto, axioma, regras )

  koch_curve.gerar_sequencia_lsystem(n)

  print(koch_curve.cadeia_obtida)
  
  koch_curve.desenhar()