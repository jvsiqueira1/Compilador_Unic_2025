# Transpilador JS para Python

Um mini-compilador que converte declarações de variáveis JavaScript (estilo `var`) para código Python equivalente. Este projeto demonstra os conceitos fundamentais de compiladores, implementando um transpilador completo com análise léxica e sintática.

## 📋 Descrição

O transpilador lê declarações de variáveis no formato JavaScript (`var nome = valor;`) e gera código Python equivalente. Durante o processo, exibe logs detalhados com análise hexadecimal dos valores processados.

**Exemplo de Entrada:**
```
var x = 10; var nome = "Lucas";
```

**Exemplo de Saída:**
```python
x = 10
nome = 'Lucas'
```

## 🏗️ Arquitetura

O projeto implementa as principais fases de um compilador:

1. **Análise Léxica (Lexer)**: Converte o texto de entrada em tokens
2. **Análise Sintática e Geração de Código (Transpiler)**: Processa os tokens seguindo regras gramaticais e gera código Python

### Estrutura do Código

O arquivo `transpiler.py` contém:

- **`Token`**: Namedtuple para representar tokens (tipo e valor)
- **`Lexer`**: Classe responsável pela análise léxica
- **`Transpiler`**: Classe responsável pela análise sintática e geração de código
- **`main()`**: Função principal que interage com o usuário

## 🔍 Componentes Detalhados

### Token

`Token` é uma `namedtuple` com dois campos:
- `type`: Tipo do token (VAR, IDENTIFIER, EQUALS, NUMBER, STRING, SEMICOLON, EOF)
- `value`: Valor do token (ex: 'var', 'x', 10, 'Lucas')

### Classe Lexer

Responsável por ler a string de entrada e converter em tokens.

#### Métodos Principais

**`__init__(self, text)`**
- Inicializa o lexer com o texto de entrada
- Define a posição inicial (`pos = 0`)
- Define o caractere atual (`current_char`)

**`advance()`**
- Avança a posição no texto
- Atualiza `current_char` para o próximo caractere
- Define `current_char = None` quando chega ao fim do texto

**`skip_whitespace()`**
- Pula espaços em branco, tabs e quebras de linha
- Chama `advance()` enquanto encontra caracteres de espaço

**`integer()`**
- Lê uma sequência de dígitos
- Retorna o número inteiro correspondente
- Para quando encontra um caractere não numérico

**`string()`**
- Lê uma string entre aspas duplas
- Pula a primeira aspas, lê o conteúdo e pula a última aspas
- Retorna a string sem as aspas

**`identifier()`**
- Lê um identificador (nome de variável ou palavra-chave)
- Aceita letras, números e underscore (`_`)
- Retorna a string do identificador

**`get_next_token()`**
- Método principal que identifica e retorna o próximo token
- Processa o texto caracter por caracter
- Retorna tokens do tipo:
  - `VAR`: Palavra-chave 'var'
  - `IDENTIFIER`: Nome de variável (ex: 'x', 'nome')
  - `EQUALS`: Sinal de igual '='
  - `NUMBER`: Número inteiro (ex: 10, 42)
  - `STRING`: String entre aspas duplas (ex: "Lucas")
  - `SEMICOLON`: Ponto e vírgula ';'
  - `EOF`: Fim do texto

### Classe Transpiler

Responsável pelo parsing sintático e geração de código Python.

#### Métodos Principais

**`__init__(self, lexer)`**
- Recebe uma instância do Lexer
- Inicializa `current_token` com o primeiro token

**`eat(token_type)`**
- Consome o token esperado (verifica se o tipo está correto)
- Avança para o próximo token chamando `lexer.get_next_token()`
- Lança exceção se o token não for do tipo esperado

**`parse_statement()`**
- Implementa a gramática: `var IDENTIFIER = VALOR ;`
- Processo:
  1. Consome o token `VAR`
  2. Lê e salva o `IDENTIFIER` (nome da variável)
  3. Consome o token `EQUALS`
  4. Lê e salva o `NUMBER` ou `STRING` (valor)
  5. Consome o token `SEMICOLON`
- Retorna uma tupla `(nome, valor)`

**`run()`**
- Método principal que processa múltiplas declarações
- Funcionamento:
  1. Cria lista `python_code` para armazenar código gerado
  2. Imprime cabeçalho "--- LOG DE TRANSPILAÇÃO ---"
  3. Entra em loop processando declarações até encontrar `EOF`
  4. Para cada declaração:
     - Chama `parse_statement()` para obter `(nome, valor)`
     - Imprime log hexadecimal:
       - **Inteiros**: `Processando ('nome', valor): Hex: 0x...`
       - **Strings**: `Processando ('nome', "valor"): Hex: 0x.. 0x.. 0x..` (hex de cada caractere)
     - Formata linha Python: `f"{name} = {repr(value)}"`
     - Adiciona à lista `python_code`
  5. Retorna código Python unido por quebras de linha (`\n`.join()`)

### Função main()

Função principal que interage com o usuário:
- Exibe cabeçalho e instruções
- Loop interativo que:
  - Solicita entrada do usuário via `input()`
  - Verifica se o usuário digitou 'sair' para encerrar
  - Cria instâncias de `Lexer` e `Transpiler`
  - Chama `transpiler.run()` e exibe o resultado
- Trata exceções (erros de parsing, interrupção por Ctrl+C)

## 🚀 Como Usar

### Requisitos

- Python 3.6 ou superior

### Execução

```bash
python transpiler.py
```

### Exemplos de Uso

**Exemplo 1: Declarações simples**
```
Digite suas declarações: var x = 10; var y = 20;
```

**Saída:**
```
--- LOG DE TRANSPILAÇÃO ---
Processando ('x', 10): Hex: 0xa
Processando ('y', 20): Hex: 0x14

--- CÓDIGO GERADO (Python) ---
x = 10
y = 20
```

**Exemplo 2: Com strings**
```
Digite suas declarações: var nome = "Lucas"; var idade = 25;
```

**Saída:**
```
--- LOG DE TRANSPILAÇÃO ---
Processando ('nome', "Lucas"): Hex: 0x4c 0x75 0x63 0x61 0x73
Processando ('idade', 25): Hex: 0x19

--- CÓDIGO GERADO (Python) ---
nome = 'Lucas'
idade = 25
```

**Exemplo 3: Múltiplas declarações**
```
Digite suas declarações: var x = 42; var nome = "ola"; var teste = 123;
```

**Saída:**
```
--- LOG DE TRANSPILAÇÃO ---
Processando ('x', 42): Hex: 0x2a
Processando ('nome', "ola"): Hex: 0x6f 0x6c 0x61
Processando ('teste', 123): Hex: 0x7b

--- CÓDIGO GERADO (Python) ---
x = 42
nome = 'ola'
teste = 123
```

### Formato de Entrada

- Declarações no formato: `var IDENTIFIER = VALOR ;`
- `IDENTIFIER`: Nome da variável (letras, números, underscore)
- `VALOR`: Número inteiro ou string entre aspas duplas
- Múltiplas declarações separadas por espaço
- Sempre termine com ponto e vírgula (`;`)

### Encerrar o Programa

Digite `'sair'` para encerrar o programa.

## 📊 Análise Hexadecimal

O transpilador exibe a representação hexadecimal dos valores processados:

- **Números inteiros**: Conversão direta para hexadecimal
  - Exemplo: `42` → `0x2a`

- **Strings**: Hexadecimal de cada caractere (código Unicode)
  - Exemplo: `"ola"` → `0x6f 0x6c 0x61` (o, l, a)

## 🎯 Conceitos de Compiladores Demonstrados

Este projeto demonstra:

1. **Análise Léxica (Lexical Analysis)**:
   - Tokenização do código fonte
   - Reconhecimento de palavras-chave, identificadores, literais
   - Tratamento de espaços em branco

2. **Análise Sintática (Parsing)**:
   - Processamento de tokens seguindo regras gramaticais
   - Validação da estrutura do código
   - Técnica de "descida recursiva"

3. **Geração de Código (Code Generation)**:
   - Conversão de AST (estrutura parseada) em código alvo
   - Formatação adequada do código gerado

4. **Tratamento de Erros**:
   - Validação de tokens inesperados
   - Mensagens de erro descritivas

## 🐛 Tratamento de Erros

O programa trata os seguintes erros:

- **Caracteres inválidos**: Lança exceção se encontrar caractere não reconhecido
- **Tokens inesperados**: Lança exceção se a estrutura da declaração estiver incorreta
- **Entrada vazia**: Solicita nova entrada
- **Interrupção pelo usuário**: Trata `KeyboardInterrupt` (Ctrl+C) graciosamente

### Exemplos de Erros

**Token inesperado:**
```
Digite suas declarações: var x = 10
Erro: Token inesperado: esperado SEMICOLON, encontrado EOF
```

**Caractere não reconhecido:**
```
Digite suas declarações: var x @ 10;
Erro: Caractere não reconhecido: @
```

## 📝 Estrutura de Arquivos

```
Compiladores/
├── transpiler.py    # Código principal do transpilador
└── README.md        # Esta documentação
```

## 🔧 Como Funciona Internamente

### Fluxo de Execução

1. **Entrada do Usuário**: Texto JavaScript digitado pelo usuário
2. **Lexer**: Converte texto em sequência de tokens
3. **Transpiler**: Processa tokens e gera código Python
4. **Saída**: Código Python formatado + logs hexadecimais

### Exemplo de Processamento

**Entrada:**
```
var x = 10;
```

**Tokens gerados pelo Lexer:**
1. `Token('VAR', 'var')`
2. `Token('IDENTIFIER', 'x')`
3. `Token('EQUALS', '=')`
4. `Token('NUMBER', 10)`
5. `Token('SEMICOLON', ';')`
6. `Token('EOF', None)`

**Processamento pelo Transpiler:**
1. Consome `VAR`
2. Lê `IDENTIFIER` → nome = 'x'
3. Consome `EQUALS`
4. Lê `NUMBER` → valor = 10
5. Consome `SEMICOLON`
6. Retorna `('x', 10)`
7. Formata: `"x = 10"`
8. Adiciona à lista de código Python

**Saída:**
```
--- LOG DE TRANSPILAÇÃO ---
Processando ('x', 10): Hex: 0xa

--- CÓDIGO GERADO (Python) ---
x = 10
```

## 👨‍💻 Autor

João Vitor de Siqueira Campos

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.
