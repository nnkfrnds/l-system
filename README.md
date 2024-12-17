# l-system

### Descrição do programa 

Este programa é uma implementação de sistemas de Lindenmayer (L-Systems) em Python. A partir de uma sequência inicial (axioma) e regras de substituição, o sistema gera padrões gráficos iterativos que são desenhados usando a biblioteca turtle.

### Comando para rodar

**Atenção** deve sempre ter o ambiente conda ativado com as dependências necessárias


```bash
python ex1.py --d 30 --a 30 --i 2 --l 2 --axim "F" --rules "F:F[-F][+F]+[-F]"
```
### Explicação dos Parâmetros

| Parâmetro | Descrição | Default |
|---|---|---|
| `--d` | Distância que a tartaruga percorre em cada movimento | 10 |
| `--a` | Ângulo de rotação para os comandos + e - | 60 |
| `--i` | Número de iterações para aplicação das regras do L-System | 6 |
| `--l` | Largura da linha desenhada | 1 |
| `--axim` | Axioma inicial | "F" |
| `--rules` | Regras de substituição (ex: "F:F[-G][+G],G:F[-R][+R]") | Nenhum |

### Funcionamento

O programa funciona da seguinte maneira:

1.  **Entrada de parâmetros:** Através da biblioteca `argparse`, o programa recebe parâmetros pela linha de comando. Isso permite configurar diversos aspectos da geração e desenho, como:
    *   Distância de movimento (`--d`)
    *   Ângulo de rotação (`--a`)
    *   Número de iterações (`--i`)
    *   Axioma inicial (`--axim`)
    *   Regras de substituição (`--rules`)
2.  **Geração do L-System:** Com base nos parâmetros fornecidos, o programa gera a sequência do L-System aplicando as regras de substituição iterativamente.
3.  **Desenho com `turtle`:** A sequência gerada é então interpretada e desenhada utilizando a biblioteca `turtle`. Cada símbolo na sequência corresponde a uma ação específica da tartaruga, como mover para frente, rotacionar ou alterar a cor.

Os valores padrão para os parâmetros podem ser alterados através da linha de comando.


### Desenho com Turtle

O programa utiliza a biblioteca `turtle` para desenhar a sequência gerada. Os seguintes comandos são interpretados:

| Comando | Descrição |
|---|---|
| `F` | Move a tartaruga para frente desenhando uma linha. |
| `f` | Move a tartaruga para frente sem desenhar. |
| `+` | Rotaciona a tartaruga para a direita (ângulo especificado por `--a`). |
| `-` | Rotaciona a tartaruga para a esquerda (ângulo especificado por `--a`). |
| `[` | Salva a posição atual e o ângulo da tartaruga na pilha. |
| `]` | Restaura a última posição e ângulo salvos. |
| `G` | Altera a cor da linha para verde. |
| `R` | Altera a cor da linha para vermelho. |
| `B` | Altera a cor da linha para azul. |
| `Y` | Altera a cor da linha para amarelo. |
| `O` | Altera a cor da linha para laranja. |

### Validação com Autômato de Pilha

Esta seção descreve a implementação de um autômato de pilha para validar as cadeias geradas pelo L-System.

#### Funcionamento (Validação com Autômato de Pilha)

O programa implementa um autômato de pilha para verificar se uma cadeia gerada por um L-System é válida de acordo com a gramática definida. O processo consiste em:

1.  **Definição do Alfabeto:** O alfabeto do L-System é definido, classificando os símbolos como variáveis ou constantes.
2.  **Geração da Cadeia:** Uma cadeia é gerada usando as regras de produção do L-System.
3.  **Construção das Transições:** As transições do autômato de pilha são construídas com base no alfabeto, nas regras de produção e no número de iterações do L-System. As transições consideram a manipulação da pilha (empilhar e desempilhar) e a leitura da cadeia de entrada.
4.  **Validação:** O autômato percorre a cadeia, aplicando as transições e manipulando a pilha. A cadeia é considerada válida se o autômato atingir o estado final com a pilha vazia.

#### Estruturas de Dados

*   **`Transicao`:** Uma classe dataclass que representa uma transição do autômato, contendo o estado de origem, estado de destino, símbolo de leitura, símbolo a ser desempilhado e símbolos a serem empilhados.
*   **`LSystem`:** Uma classe dataclass que representa o L-System, contendo o alfabeto, o axioma e as regras de produção.
*   **`AutomatoPilha`:** Uma classe dataclass que representa o autômato de pilha, contendo uma instância do `LSystem`, o alfabeto da pilha, os estados do autômato e o número de iterações.

#### Função `validar_cadeia`

Esta função implementa a lógica de validação da cadeia usando o autômato de pilha. Ela itera pela cadeia, aplicando as transições válidas e manipulando a pilha.

#### Função `construir_transicoes`

Esta função constrói a lista de transições do autômato de pilha, considerando as regras de produção do L-System e o número de iterações.

#### Função `gerar_alfabeto_da_pilha`

Esta função gera o alfabeto da pilha com base nas variáveis do alfabeto do L-System e no número de iterações.

#### Exemplo de uso



### Requisitos

- Python
- Conda
- Biblioteca Turtle ( Já vem na instalação do Python )
