'use client';

import React, { createContext, useContext, type ReactNode } from 'react';
import type { IHttpClient } from '../../domain/ports/http-client.port';

export interface IDependencyContainer {
  httpClient: IHttpClient;
}

const DependencyContext = createContext<IDependencyContainer | null>(null);

export const useDependencies = (): IDependencyContainer => {
  const dependencies = useContext(DependencyContext);

  if (!dependencies)
    throw new Error('useDependencies must be used within a DependencyProvider');

  return dependencies;
};

interface DependencyProviderProps {
  dependencies: IDependencyContainer;
  children: ReactNode;
}

export const DependencyProvider: React.FC<DependencyProviderProps> = ({
  dependencies,
  children,
}) => {
  return (
    <DependencyContext.Provider value={dependencies}>
      {children}
    </DependencyContext.Provider>
  );
};
