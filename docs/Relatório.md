Sequenciamento de Tarefas em Linhas de Produção com Setups

1. Descrição detalhada do problema

Em muitas linhas de produção (ex.: manufatura discreta, envase, impressão), a troca de um trabalho (lote/produto) para outro exige setups (trocas de ferramenta, limpeza, calibração). O tempo/custo de setup depende da ordem em que os trabalhos são processados (setups dependentes da sequência).

Objetivo: encontrar uma ordem para processar todas as tarefas (cada tarefa deve ser executada exatamente uma vez na linha) que minimize o somatório de custos/tempos de setup (e, por consequência, aumente a eficiência e throughput). Opcionalmente, o modelo pode incluir tempos de processamento (p_j) e ponderar objetivos (e.g., minimizar ( + )).

Hipóteses base do caso monolinha (single-machine): - Existe um conjunto finito de tarefas (J = {1,2,,n}). - Cada tarefa é executada uma única vez, sem preempção. - Há um custo/tempo de setup (s*{ij} ) para trocar da tarefa (i) para a tarefa (j) (tipicamente assimétrico, i.e., (s*{ij} s*{ji})). - Existe um estado inicial “vazio” (máquina ociosa) modelado por um nó fictício (0) com custos (s*{0j}) para iniciar pela tarefa (j).

Esse problema é análogo ao ATSP – Travelling Salesman Problem assimétrico em trilha (Hamiltonian path) partindo de (0), onde as arestas representam custos de setup. Resolver via busca informada (A\*, Greedy Best-First) é natural se definirmos adequadamente estados, ações, função sucessor, custo e heurística admissível.

Extensões (fora do escopo principal, mas úteis): múltiplas linhas paralelas (máquinas idênticas) ou flow shop/job shop. A modelagem abaixo foca em uma linha e comenta rapidamente adaptações no final.

---

2. Modelagem do problema

2.a Representação computacional do problema

Grafo dirigido e completo (G=(V,E)): - Vértices: (V = J {0}) onde (0) é o estado inicial fictício. - Arestas: (E = {(i,j) ij, i,j V}) com pesos (w(i,j)=s\_{ij}) (custo/tempo de setup de (i) para (j)). - Solução: um caminho Hamiltoniano iniciando em (0) que visita cada (jJ) exatamente uma vez, minimizando (w(i,j)) das transições consecutivas.

Para implementação de busca, usamos estados como permutação parcial: - (): tupla ordenada das tarefas já escaladas. - (): conjunto (ou bitmask) de tarefas ainda não alocadas. - (): última tarefa executada (ou (0) no início).

Estruturas recomendadas: - Representar restantes como bitmask (inteiro) para performance (A\* sobre permutações é exponencial, otimizações importam). - último como inteiro (J {0}). - sequência pode ser omitida do estado e reconstruída via ponteiros de pai, reduzindo memória, mantendo no estado apenas (bitmask_restantes, ultimo).

2.b Exemplo de estado inicial e final

● Estado inicial (monolinha):

o sequência = []

o restantes = J (ou bitmask com todos os bits ligados)

o último = 0 (nó fictício de partida)

● Estado final:

o restantes = ∅ (bitmask = 0)

o sequência contém todas as tarefas (permuta completa); último é a última tarefa da ordem.

2.c Função “sucessor”

Para um estado (s=(R, )), onde R é o conjunto/bitmask de restantes e () é o último: - Para cada tarefa (t R): - Novo estado: (s’=(R{t}, t)). - Custo de ação: (c(ss’) = s\_{,t}). - Em implementação, iterar bits 1 de R, criando estados com R' = R \text{ sem } t e ultimo' = t.

2.d Função de custo (g)

O custo acumulado de um caminho (estado) é a soma dos setups das transições efetuadas até ali: [ g(s_0 s_k) = {r=0}^{k-1} s{x_r, x_{r+1}}, x_0=0, x_{r+1}J. ]

Variação opcional: incluir tempo de processamento (p*j) por tarefa, com ponderação (g’ = s*{ij} + p_j). Para “reduzir setups”, use () ou somente setups.

2.e Função heurística (h)

A heurística deve estimar um limite inferior (admissível) do custo mínimo restante para concluir as tarefas ainda em R a partir de (). Abaixo, três opções práticas:

(h1) Limite por mínimos de saídas (ATSP, admissível e barato): - Para cada nó (v) que ainda precisará ter uma aresta de saída no restante do caminho, considere o menor custo de sair dele. - No caminho final, apenas um nó não terá aresta de saída (o nó que terminará a sequência). Para manter admissibilidade: 1. Calcule (m() = {jR} s{j}). 2. Para cada (iR), calcule (m(i) = {jR{i}} s{ij}) (se (|R|=1), defina (m(i)=0)). 3. (h_1 = m() + {iR} m(i) - {iR} m(i)) (subtrai-se o maior (m(i)) para permitir que um nó termine sem saída). - Custo: (O(|R|^2)) por avaliação; simples e eficaz.

(h2) MST/AGM para setups simétricos (TSP, admissível): - Se (s*{ij}=s*{ji}) (aprox. simétrica), compute: (h*2 = {jR} s{j} + (R)), onde a MST é no grafo completo induzido por R com pesos (s*{ij}). (Intuição: conecta () ao componente via sua menor aresta e usa o custo mínimo para conectar todos em R.)

(h3) Relaxação por famílias de produto (setups 0 intrafamília): - Se tarefas têm famílias e (s\_{ij}=0) quando (i,j) são da mesma família, um lower bound é o número mínimo de trocas de família restantes multiplicado pelo menor setup inter-família observado. Útil em ambientes com trocas de cor/material.

Todas as heurísticas acima são admissíveis (não superestimam). Em prática, use (h1) para ATSP geral; use (h2) quando os setups forem aproximadamente simétricos; complemente com (h3) se houver famílias.
