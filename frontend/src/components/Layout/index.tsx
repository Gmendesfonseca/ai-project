import type { ReactNode } from 'react';
import { Navigation } from '../Navigation';
import { NavigationLink } from '../NavigationLink';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div
      style={{
        height: '100vh',
        width: '100vw',
      }}
    >
      <Navigation>
        <NavigationLink to="/" icon="⚙️">
          Sequenciamento de Tarefas
        </NavigationLink>
        <NavigationLink to="/base" icon="🔍">
          Busca em Grafos
        </NavigationLink>
        <NavigationLink to="/about" icon="📖">
          Sobre o Projeto
        </NavigationLink>
      </Navigation>
      <main style={{ paddingBottom: '2rem', paddingTop: '65px' }}>
        {children}
      </main>
    </div>
  );
}
