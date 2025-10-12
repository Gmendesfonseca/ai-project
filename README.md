# Projeto de IA - Algoritmos de Busca e Visualização de Grafos

## Visão Geral

Este projeto implementa e visualiza algoritmos de busca em grafos, incluindo busca não-informada (BFS, DFS, DFS limitado, aprofundamento iterativo, bidirecional) e busca informada (custo uniforme, A*, gulosa, IDA*). O sistema é composto por um backend Flask em Python e um frontend React com TypeScript.

## Arquitetura do Sistema

- **Backend**: API REST em Flask que implementa os algoritmos de busca
- **Frontend**: Interface React/TypeScript com visualização interativa de grafos
- **Visualização**: Utiliza vis-network para renderização de grafos e caminhos encontrados

---

## 🖥️ Backend (Python/Flask)

### Estrutura de Diretórios

```
backend/
├── app.py              # Servidor Flask principal
├── requirements.txt    # Dependências Python
├── run.sh             # Script de execução
└── service/           # Módulos de algoritmos
    ├── __init__.py
    ├── Node.py        # Classe base para nós
    ├── NodeP.py       # Extensão de nó com prioridade
    ├── UninformedSearch.py    # Algoritmos não-informados
    ├── InformedSearch.py      # Algoritmos informados
    ├── GenerateProblem.py     # Geração de problemas teste
    └── GenerateProblemWeights.py
```

### Algoritmos Implementados

#### Busca Não-Informada

- **Busca em Largura (BFS)**: Explora nível por nível
- **Busca em Profundidade (DFS)**: Explora ramos até o final
- **DFS Limitado**: DFS com limite de profundidade
- **Aprofundamento Iterativo**: DFS com limites crescentes
- **Busca Bidirecional**: Busca simultânea do início e fim

#### Busca Informada

- **Custo Uniforme**: Dijkstra para grafos com pesos
- **A\***: Busca com função heurística f(n) = g(n) + h(n)
- **Busca Gulosa**: Usa apenas heurística h(n)
- **IDA\***: A\* com aprofundamento iterativo

### Endpoints da API

| Método | Endpoint                                 | Descrição                |
| ------ | ---------------------------------------- | ------------------------ |
| POST   | `/search/uninformed/breadth_first`       | Busca em largura         |
| POST   | `/search/uninformed/depth_first`         | Busca em profundidade    |
| POST   | `/search/uninformed/depth_limited`       | DFS limitado             |
| POST   | `/search/uninformed/iterative_deepening` | Aprofundamento iterativo |
| POST   | `/search/uninformed/bidirectional`       | Busca bidirecional       |
| POST   | `/search/uninformed/uniform_cost`        | Custo uniforme           |
| POST   | `/search/informed/a_star`                | A\*                      |
| POST   | `/search/informed/greedy`                | Busca gulosa             |
| POST   | `/search/informed/ida_star`              | IDA\*                    |

### Como Executar o Backend

```bash
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python -m flask run
# ou
chmod +x run.sh && ./run.sh
```

O servidor estará disponível em `http://localhost:5000`

---

## 🌐 Frontend (React/TypeScript)

### Estrutura de Diretórios

```
frontend/
├── package.json       # Dependências e scripts
├── tsconfig.json      # Configuração TypeScript
├── vite.config.ts     # Configuração Vite
├── run.sh            # Script de execução
└── src/
    ├── components/    # Componentes reutilizáveis
    ├── core/         # Arquitetura limpa (gateways, adapters)
    ├── features/     # Funcionalidades principais
    │   └── Methods/  # Interface de busca e visualização
    ├── lib/          # Bibliotecas customizadas
    └── utils/        # Utilitários
```

### Funcionalidades

- **Upload de Arquivos**: Carregamento de grafos via arquivo .txt
- **Seleção de Algoritmos**: Interface para escolher algoritmo de busca
- **Visualização Interativa**: Renderização do grafo com vis-network
- **Destaque de Caminhos**: Visualização do caminho encontrado
- **Validação**: Verificação de nós inicial e objetivo
- **Geração de Dados de Teste**: Grafos grandes para testes de performance

### Tecnologias Utilizadas

- **React 18**: Biblioteca de interface
- **TypeScript**: Tipagem estática
- **Vite**: Build tool e dev server
- **React Hook Form**: Gerenciamento de formulários
- **Axios**: Cliente HTTP
- **vis-network**: Visualização de grafos

### Como Executar o Frontend

```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install
# ou
pnpm install

# Executar em modo desenvolvimento
npm run dev
# ou
chmod +x run.sh && ./run.sh
```

O frontend estará disponível em `http://localhost:3000`

---

## 📋 Como Usar o Sistema

1. **Iniciar o Backend**: Execute o servidor Flask na porta 5000
2. **Iniciar o Frontend**: Execute o servidor de desenvolvimento na porta 3000
3. **Carregar Grafo**:
   - Use o botão "Carregar arquivo (.txt)" para upload
   - Formato esperado: cada linha contém "nó1 nó2 peso" (lista de arestas)
4. **Configurar Busca**:
   - Selecione o algoritmo desejado
   - Escolha nó inicial e objetivo
   - Configure parâmetros específicos (limite de profundidade, etc.)
5. **Executar**: Clique em "Executar Busca" para visualizar o resultado

### Formato do Arquivo de Grafo

```
A B 5
B C 3
A C 8
C D 2
B D 4
```

---

## 🧪 Contexto Acadêmico: Sequenciamento de Tarefas

### Descrição do Problema

Este projeto foi desenvolvido no contexto de **sequenciamento de tarefas em linhas de produção com setups**. Em ambientes industriais (manufatura, envase, impressão), a troca entre produtos diferentes exige configurações (setups) que consomem tempo e recursos.

**Objetivo**: Encontrar uma ordem de processamento que minimize o tempo total de setup, maximizando a eficiência da linha de produção.

### Modelagem como Problema de Busca

O problema é modelado como um **Problema do Caixeiro Viajante Assimétrico (ATSP)**:

- **Estados**: Sequências parciais de tarefas processadas
- **Ações**: Adicionar próxima tarefa à sequência
- **Custo**: Tempo de setup entre tarefas consecutivas
- **Objetivo**: Encontrar sequência completa de custo mínimo

#### Representação Computacional

**Grafo dirigido e completo G=(V,E)**:

- **Vértices**: V = J ∪ {0} onde 0 é o estado inicial fictício
- **Arestas**: E = {(i,j) | i≠j, i,j ∈ V} com pesos w(i,j)=s\_{ij}
- **Solução**: Caminho Hamiltoniano iniciando em 0 que visita cada j∈J exatamente uma vez

#### Estados para Implementação de Busca

Para implementação, usamos estados como permutação parcial:

- **sequência**: Tupla ordenada das tarefas já processadas
- **restantes**: Conjunto (ou bitmask) de tarefas não alocadas
- **último**: Última tarefa executada (ou 0 no início)

#### Funções do Problema

**Função Sucessor**: Para estado s=(R, ℓ) onde R são as restantes e ℓ é o último:

- Para cada tarefa t ∈ R: Novo estado s'=(R\{t}, t)
- Custo de ação: c(s→s') = s\_{ℓ,t}

**Função de Custo**: g(s₀→sₖ) = Σ(r=0 to k-1) s\_{xᵣ,xᵣ₊₁}

### Heurísticas Implementadas

#### H1: Limite por Mínimos de Saída (ATSP)

- Para cada nó v que precisará de aresta de saída, considera menor custo
- Admissível e computacionalmente eficiente O(|R|²)
- Usado como heurística padrão para problemas ATSP gerais

#### H2: MST para Setups Simétricos

- Quando s*{ij}=s*{ji}, usa árvore geradora mínima
- h₂ = min*{j∈R} s*{ℓ,j} + MST(R)
- Eficaz quando custos são aproximadamente simétricos

#### H3: Relaxação por Famílias de Produto

- Quando tarefas têm famílias e s\_{ij}=0 para mesma família
- Lower bound baseado no número de trocas de família
- Útil em ambientes com setups zero intrafamília

Todas as heurísticas são **admissíveis** (não superestimam o custo real).

---

## 🔧 Scripts de Execução

### Backend

```bash
# Desenvolvimento
python -m flask run --debug

# Produção
python -m flask run --host=0.0.0.0 --port=5000
```

### Frontend

```bash
# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

---

## 📚 Dependências Principais

### Backend

- `Flask`: Framework web
- `Flask-CORS`: Habilitação de CORS
- `typing`: Anotações de tipo

### Frontend

- `React`: ^18.0.0
- `TypeScript`: ^5.0.0
- `Vite`: ^5.0.0
- `axios`: Cliente HTTP
- `react-hook-form`: Gerenciamento de formulários
- `vis-network`: Visualização de grafos
