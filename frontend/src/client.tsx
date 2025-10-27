'use client';

import React, { Suspense } from 'react';
import {
  Navigate,
  RouterProvider,
  createBrowserRouter,
} from 'react-router-dom';
import MainPage from './features/Methods';
import TaskSchedulePage from './features/TaskSchedule';
import AboutPage from './features/About';
import { Layout } from './components/Layout';
import LoadingComponent from './components/Loading';

export function ClientCounter() {
  const [count, setCount] = React.useState(0);

  return (
    <button onClick={() => setCount((count) => count + 1)}>
      Client Counter: {count}
    </button>
  );
}

export function Router() {
  const isBrowser =
    typeof window !== 'undefined' && typeof document !== 'undefined';

  if (!isBrowser) {
    return <LoadingComponent />;
  }

  const router = createBrowserRouter([
    {
      path: '/',
      element: (
        <Layout>
          <TaskSchedulePage />
        </Layout>
      ),
    },
    {
      path: '/base',
      element: (
        <Layout>
          <MainPage />
        </Layout>
      ),
    },
    {
      path: '/about',
      element: (
        <Layout>
          <AboutPage />
        </Layout>
      ),
    },
    {
      path: '*',
      element: <Navigate to="/" replace />,
    },
  ]);

  return (
    <Suspense fallback={<LoadingComponent />}>
      <RouterProvider router={router} />
    </Suspense>
  );
}
