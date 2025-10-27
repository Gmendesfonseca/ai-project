# Projeto de IA - Algoritmos de Busca em Grafos e Sequenciamento de Tarefas

## Visão Geral

Este projeto implementa e visualiza algoritmos de busca em duas modalidades principais:

1. **Busca em Grafos Gerais**: Algoritmos clássicos para encontrar caminhos entre nós
2. **Sequenciamento de Tarefas**: Aplicação dos algoritmos para otimização de sequências de produção

O sistema é composto por um backend Flask em Python e um frontend React com TypeScript, oferecendo uma interface interativa para visualização e teste dos algoritmos.

## Arquitetura do Sistema

- **Backend**: API REST em Flask que implementa os algoritmos de busca
- **Frontend**: Interface React/TypeScript com visualização interativa de grafos
- **Visualização**: Utiliza vis-network para renderização de grafos e caminhos encontrados

---

## 🖥️ Backend (Python/Flask)

### Estrutura de Diretórios

```
backend/
├── app.py              # Servidor Flask principal com todos os endpoints
├── requirements.txt    # Dependências Python
├── run.sh             # Script de execução
└── service/           # Módulos de algoritmos
    ├── __init__.py
    ├── base/          # Algoritmos básicos de busca em grafos
    │   ├── Node.py        # Classe base para nós
    │   ├── NodeP.py       # Extensão de nó com prioridade
    │   ├── UninformedSearch.py    # Algoritmos não-informados
    │   ├── InformedSearch.py      # Algoritmos informados
    │   ├── GenerateProblem.py     # Geração de problemas teste
    │   └── GenerateProblemWeights.py
    └── implementation/   # Implementação especializada para tarefas
        ├── TaskSchedulingSearch.py    # Algoritmos para sequenciamento
        ├── TaskSchedulingNode.py      # Nó especializado com bitmask
        ├── TaskSchedulingData.py      # Estruturas de dados (SetupMatrix)
        ├── TaskSchedulingHeuristics.py # Heurísticas H1, H2, H3
        └── TaskFamily.py              # Agrupamento de tarefas por família
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

#### Busca em Grafos Gerais

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

#### Sequenciamento de Tarefas

| Método | Endpoint                                        | Descrição                        |
| ------ | ----------------------------------------------- | -------------------------------- |
| POST   | `/scheduling/task-sequence/breadth_first`       | BFS para sequenciamento          |
| POST   | `/scheduling/task-sequence/depth_first`         | DFS para sequenciamento          |
| POST   | `/scheduling/task-sequence/depth_limited`       | DFS limitado para sequenciamento |
| POST   | `/scheduling/task-sequence/iterative_deepening` | Aprofundamento iterativo         |
| POST   | `/scheduling/task-sequence/bidirectional`       | Busca bidirecional               |
| POST   | `/scheduling/task-sequence/uniform_cost`        | Custo uniforme (Dijkstra)        |
| POST   | `/scheduling/task-sequence/a_star`              | A\* com heurísticas H1/H2/H3     |
| POST   | `/scheduling/task-sequence/greedy`              | Busca gulosa                     |
| POST   | `/scheduling/task-sequence/ida_star`            | IDA\* para sequenciamento        |

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
    ├── components/    # Componentes reutilizáveis (Input, Select, Loading)
    ├── core/         # Arquitetura limpa (gateways, adapters)
    │   ├── domain/   # Interfaces de gateway
    │   └── infra/    # Implementações HTTP
    ├── features/     # Funcionalidades principais
    │   ├── About/    # Página sobre o projeto
    │   ├── Methods/  # Interface de busca em grafos
    │   └── TaskSchedule/ # Interface de sequenciamento de tarefas
    ├── framework/    # Configuração React/RSC
    ├── lib/          # Bibliotecas customizadas (vis-network wrapper)
    └── utils/        # Utilitários e constantes
```

### Funcionalidades

#### Busca em Grafos (Methods)

- **Upload de Arquivos**: Carregamento de grafos via arquivo .txt
- **Seleção de Algoritmos**: Interface para escolher algoritmo de busca
- **Visualização Interativa**: Renderização do grafo com vis-network
- **Destaque de Caminhos**: Visualização do caminho encontrado
- **Validação**: Verificação de nós inicial e objetivo
- **Geração de Dados de Teste**: Grafos grandes para testes de performance

#### Sequenciamento de Tarefas (TaskSchedule)

- **Upload de Setup Matrix**: Carregamento de custos de setup via formato "origem,destino:custo"
- **Detecção Automática de Tarefas**: Identificação automática das tarefas baseada na matriz
- **Configuração de Famílias**: Definição manual de famílias de produtos para heurística H3
- **Seleção de Heurísticas**: Escolha entre H1 (mínimos), H2 (MST), H3 (famílias)
- **Visualização de Sequência**: Exibição da sequência ótima encontrada
- **Cálculo de Custos**: Detalhamento dos custos de setup por transição

### Tecnologias Utilizadas

- **React 19**: Biblioteca de interface com RSC (React Server Components)
- **TypeScript 5**: Tipagem estática
- **Vite 7**: Build tool e dev server
- **React Hook Form**: Gerenciamento de formulários
- **Axios**: Cliente HTTP para comunicação com backend
- **vis-network**: Visualização interativa de grafos
- **React Router DOM**: Roteamento entre páginas
- **Lodash**: Utilitários JavaScript

### Arquitetura Frontend

O frontend segue princípios de **Clean Architecture**:

- **Domain Layer**: Interfaces de gateway que definem contratos
- **Infrastructure Layer**: Implementações concretas dos gateways usando Axios
- **Features**: Componentes organizados por funcionalidade
- **Components**: Componentes reutilizáveis de UI
- **Utils**: Funções utilitárias e constantes

#### Padrão Gateway

- `TaskSchedulingGateway`: Interface para operações de sequenciamento
- `UninformedSearchGateway`: Interface para busca não-informada
- `InformedSearchGateway`: Interface para busca informada
- `AxiosHttpAdapter`: Adaptador HTTP para comunicação com API

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

### Configuração Inicial

1. **Iniciar o Backend**: Execute o servidor Flask na porta 5000
2. **Iniciar o Frontend**: Execute o servidor de desenvolvimento na porta 3000

### Busca em Grafos (Página Methods)

3. **Carregar Grafo**:
   - Use o botão "Carregar arquivo (.txt)" para upload
   - Formato esperado: cada linha contém "nó1 nó2 peso" (lista de arestas)
4. **Configurar Busca**:
   - Selecione o algoritmo desejado
   - Escolha nó inicial e objetivo
   - Configure parâmetros específicos (limite de profundidade, heurísticas)
5. **Executar**: Clique em "Executar Busca" para visualizar o resultado

### Sequenciamento de Tarefas (Página TaskSchedule)

3. **Carregar Setup Matrix**:
   - Use o botão "Carregar arquivo (.txt)" para upload
   - Formato esperado: cada linha contém "origem,destino:custo"
4. **Configurar Famílias** (opcional):
   - Para cada tarefa detectada, defina uma família de produto
   - Usado pela heurística H3 para otimização adicional
5. **Configurar Algoritmo**:
   - Selecione o algoritmo desejado
   - Para algoritmos informados, escolha a heurística (H1, H2, H3)
   - Configure parâmetros específicos conforme necessário
6. **Executar**: Clique em "Executar Busca" para encontrar a sequência ótima

### Formatos de Arquivo

#### Grafo Geral (Methods)

```
A B 5
B C 3
A C 8
C D 2
B D 4
```

#### Setup Matrix (TaskSchedule)

```
0,1:10
0,2:15
0,3:8
1,2:5
1,3:12
2,1:7
2,3:4
3,1:9
3,2:6
```

---

## 🧪 Contexto Acadêmico: Sequenciamento de Tarefas

### Descrição do Problema

Este projeto foi desenvolvido no contexto de **sequenciamento de tarefas em linhas de produção com setups**. Em ambientes industriais (manufatura, envase, impressão), a troca entre produtos diferentes exige configurações (setups) que consomem tempo e recursos.

**Objetivo**: Encontrar uma ordem de processamento que minimize o tempo total de setup, maximizando a eficiência da linha de produção.

### Implementação Técnica

O sistema oferece uma implementação completa com:

- **9 Algoritmos de Busca**: Todos os algoritmos clássicos adaptados para sequenciamento
- **3 Heurísticas Especializadas**: H1, H2, H3 otimizadas para o domínio
- **Interface Dupla**: Páginas separadas para grafos gerais e sequenciamento
- **Representação Eficiente**: Uso de bitmasks para estados de tarefas restantes
- **Validação Robusta**: Verificação de matrizes de setup e parâmetros
- **Visualização Detalhada**: Exibição de sequências e custos de transição

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

Para implementação, usamos estados como permutação parcial representados pela classe `TaskSchedulingNode`:

- **remaining_bitmask**: Bitmask das tarefas restantes (eficiente para verificação O(1))
- **last_task**: Última tarefa executada (ou 0 no estado inicial)
- **v1**: Custo f (g+h) para algoritmos informados ou g para não-informados
- **v2**: Custo g real acumulado
- **parent**: Referência ao nó pai para reconstrução do caminho

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

#### Tratamento de Famílias de Produtos

O sistema suporta agrupamento de tarefas em famílias, onde:

- **Setup intrafamília**: Custo zero ou muito baixo entre tarefas da mesma família
- **Setup interfamília**: Custo significativo entre famílias diferentes
- **Heurística H3**: Explora essa estrutura para melhores estimativas
- **Interface dinâmica**: Permite definição manual de famílias por tarefa

### Validações e Tratamento de Erros

- **Matriz de Setup**: Verificação de completude e consistência
- **JSON Safety**: Conversão de `float('inf')` para `null` em respostas HTTP
- **Logs Estruturados**: Sistema de logging para debug e monitoramento
- **Tratamento de Exceções**: Respostas HTTP estruturadas para diferentes tipos de erro

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
- `typing`: Anotações de tipo Python

### Frontend

- `React`: ^19.1.1 (com React Server Components)
- `TypeScript`: ^5.0.0
- `Vite`: ^7.1.4
- `axios`: ^1.12.2 - Cliente HTTP
- `react-hook-form`: ^7.63.0 - Gerenciamento de formulários
- `vis-network`: ^10.0.2 - Visualização de grafos
- `react-router-dom`: ^7.9.3 - Roteamento
- `lodash`: ^4.17.21 - Utilitários
- `uuid`: ^13.0.0 - Geração de IDs únicos
