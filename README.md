# l-system

##Descrição do programa 

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
