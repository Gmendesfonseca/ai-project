'use client';

import { PageComposition } from '@/components/Page';

export default function AboutPage() {
  return (
    <PageComposition.Container>
      <PageComposition.Title>
        Sobre o Projeto - Algoritmos de Busca e IA
      </PageComposition.Title>
      <PageComposition.Content>
        <div style={{ maxWidth: '800px', margin: '0 auto', lineHeight: '1.6' }}>
          {/* Project Overview */}
          <section style={{ marginBottom: '2rem' }}>
            <h2
              style={{
                color: '#FFF',
                borderBottom: '2px solid #007bff',
                paddingBottom: '0.5rem',
              }}
            >
              Visão Geral do Projeto
            </h2>
            <p>
              Este projeto implementa e visualiza algoritmos de busca em duas
              modalidades principais:
            </p>
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li>
                <strong>Busca em Grafos Gerais</strong>: Algoritmos clássicos
                para encontrar caminhos entre nós
              </li>
              <li>
                <strong>Sequenciamento de Tarefas</strong>: Aplicação dos
                algoritmos para otimização de sequências de produção
              </li>
            </ul>
            <p>
              O sistema oferece uma interface interativa para visualização e
              teste dos algoritmos, desenvolvido com React/TypeScript no
              frontend e Flask/Python no backend.
            </p>
          </section>

          {/* Algorithms */}
          <section style={{ marginBottom: '2rem' }}>
            <h2
              style={{
                color: '#FFF',
                borderBottom: '2px solid #007bff',
                paddingBottom: '0.5rem',
              }}
            >
              Algoritmos Implementados
            </h2>

            <h3 style={{ color: '#FFF', marginTop: '1.5rem' }}>
              Busca Não-Informada
            </h3>
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li>
                <strong>Busca em Largura (BFS)</strong>: Explora nível por
                nível, garantindo caminho mais curto
              </li>
              <li>
                <strong>Busca em Profundidade (DFS)</strong>: Explora ramos até
                o final
              </li>
              <li>
                <strong>DFS Limitado</strong>: DFS com limite de profundidade
              </li>
              <li>
                <strong>Aprofundamento Iterativo</strong>: DFS com limites
                crescentes
              </li>
              <li>
                <strong>Busca Bidirecional</strong>: Busca simultânea do início
                e fim
              </li>
            </ul>

            <h3 style={{ color: '#FFF', marginTop: '1.5rem' }}>
              Busca Informada
            </h3>
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li>
                <strong>Custo Uniforme</strong>: Dijkstra para grafos com pesos
              </li>
              <li>
                <strong>A*</strong>: Busca com função heurística f(n) = g(n) +
                h(n)
              </li>
              <li>
                <strong>Busca Gulosa</strong>: Usa apenas heurística h(n)
              </li>
              <li>
                <strong>IDA*</strong>: A* com aprofundamento iterativo
              </li>
            </ul>
          </section>

          {/* Task Scheduling */}
          <section style={{ marginBottom: '2rem' }}>
            <h2
              style={{
                color: '#FFF',
                borderBottom: '2px solid #007bff',
                paddingBottom: '0.5rem',
              }}
            >
              Sequenciamento de Tarefas (ATSP)
            </h2>
            <p>
              O projeto modela o problema de{' '}
              <strong>sequenciamento de tarefas em linhas de produção</strong>
              como um Problema do Caixeiro Viajante Assimétrico (ATSP). Em
              ambientes industriais (manufatura, envase, impressão), a troca
              entre produtos diferentes exige configurações (setups) que
              consomem tempo e recursos.
            </p>

            <h3 style={{ color: '#FFF', marginTop: '1.5rem' }}>
              Heurísticas Especializadas
            </h3>
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li>
                <strong>H1 - Mínimos de Saída</strong>: Para cada nó que
                precisará de aresta de saída, considera menor custo (O(|R|²))
              </li>
              <li>
                <strong>H2 - MST Simétrico</strong>: Usa árvore geradora mínima
                quando custos são aproximadamente simétricos
              </li>
              <li>
                <strong>H3 - Famílias de Produto</strong>: Explora estrutura de
                famílias onde setup intrafamília é zero
              </li>
            </ul>
            <p style={{ fontStyle: 'italic', color: '#666' }}>
              Todas as heurísticas são admissíveis (não superestimam o custo
              real).
            </p>
          </section>

          {/* Technical Implementation */}
          <section style={{ marginBottom: '2rem' }}>
            <h2
              style={{
                color: '#FFF',
                borderBottom: '2px solid #007bff',
                paddingBottom: '0.5rem',
              }}
            >
              Implementação Técnica
            </h2>

            <h3 style={{ color: '#FFF', marginTop: '1.5rem' }}>
              Backend (Python/Flask)
            </h3>
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li>
                18 endpoints RESTful (9 para grafos gerais + 9 para
                sequenciamento)
              </li>
              <li>
                Representação eficiente com bitmasks para estados de tarefas
              </li>
              <li>Arquitetura modular com classes especializadas</li>
              <li>Validação robusta e tratamento de erros</li>
            </ul>

            <h3 style={{ color: '#FFF', marginTop: '1.5rem' }}>
              Frontend (React/TypeScript)
            </h3>
            <ul style={{ paddingLeft: '1.5rem' }}>
              <li>React 19 com React Server Components (RSC)</li>
              <li>Clean Architecture com padrão Gateway</li>
              <li>Visualização interativa com vis-network</li>
              <li>
                Interface dupla: páginas separadas para grafos e sequenciamento
              </li>
            </ul>
          </section>

          {/* How to Use */}
          <section style={{ marginBottom: '2rem' }}>
            <h2
              style={{
                color: '#FFF',
                borderBottom: '2px solid #007bff',
                paddingBottom: '0.5rem',
              }}
            >
              Como Usar o Sistema
            </h2>

            <h3 style={{ color: '#FFF', marginTop: '1.5rem' }}>
              Busca em Grafos
            </h3>
            <ol style={{ paddingLeft: '1.5rem' }}>
              <li>Carregue um arquivo .txt com formato "nó1 nó2 peso"</li>
              <li>Selecione o algoritmo desejado</li>
              <li>Escolha nós inicial e objetivo</li>
              <li>Configure parâmetros específicos (heurísticas, limites)</li>
              <li>Execute a busca e visualize o resultado</li>
            </ol>

            <h3 style={{ color: '#FFF', marginTop: '1.5rem' }}>
              Sequenciamento de Tarefas
            </h3>
            <ol style={{ paddingLeft: '1.5rem' }}>
              <li>
                Carregue um arquivo .txt com formato "origem,destino:custo"
              </li>
              <li>Configure famílias de produtos (opcional, para H3)</li>
              <li>Selecione algoritmo e heurística</li>
              <li>Execute a busca para encontrar sequência ótima</li>
              <li>Visualize a sequência e custos de transição</li>
            </ol>
          </section>

          {/* Academic Context */}
          <section style={{ marginBottom: '2rem' }}>
            <h2
              style={{
                color: '#FFF',
                borderBottom: '2px solid #007bff',
                paddingBottom: '0.5rem',
              }}
            >
              Contexto Acadêmico
            </h2>
            <p>
              Este projeto foi desenvolvido no contexto da disciplina de{' '}
              <strong>Introdução à Inteligência Artificial</strong>,
              demonstrando a aplicação prática de algoritmos de busca em
              problemas reais de otimização industrial.
            </p>
            <p>
              O sistema serve como uma ferramenta educacional completa,
              mostrando tanto algoritmos de propósito geral quanto técnicas de
              otimização específicas para domínios industriais.
            </p>
          </section>

          {/* Technologies */}
          <section style={{ marginBottom: '2rem' }}>
            <h2
              style={{
                color: '#FFF',
                borderBottom: '2px solid #007bff',
                paddingBottom: '0.5rem',
              }}
            >
              Tecnologias Utilizadas
            </h2>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '1rem',
              }}
            >
              <div>
                <h4 style={{ color: '#FFF' }}>Backend</h4>
                <ul style={{ paddingLeft: '1rem', fontSize: '0.9rem' }}>
                  <li>Python 3.12</li>
                  <li>Flask</li>
                  <li>Flask-CORS</li>
                </ul>
              </div>
              <div>
                <h4 style={{ color: '#FFF' }}>Frontend</h4>
                <ul style={{ paddingLeft: '1rem', fontSize: '0.9rem' }}>
                  <li>React 19</li>
                  <li>TypeScript 5</li>
                  <li>Vite 7</li>
                  <li>React Hook Form</li>
                  <li>vis-network</li>
                  <li>Axios</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Footer */}
          <footer
            style={{
              textAlign: 'center',
              padding: '2rem 0',
              borderTop: '1px solid #eee',
              marginTop: '3rem',
              color: '#FFF',
            }}
          >
            <p>
              Projeto desenvolvido para demonstrar algoritmos de busca e
              otimização em IA
            </p>
            <p style={{ fontSize: '0.9rem' }}>
              Utilize as páginas de navegação acima para testar os diferentes
              algoritmos
            </p>
          </footer>
        </div>
      </PageComposition.Content>
    </PageComposition.Container>
  );
}
