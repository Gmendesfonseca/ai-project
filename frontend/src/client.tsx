'use client';

import React, { Suspense } from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import MainPage from './features/Main';

export function ClientCounter() {
  const [count, setCount] = React.useState(0);

  return (
    <button onClick={() => setCount((count) => count + 1)}>
      Client Counter: {count}
    </button>
  );
}

const LoadingComponent = () => <div>Loading...</div>;

export function Router() {
  const isBrowser =
    typeof window !== 'undefined' && typeof document !== 'undefined';

  if (!isBrowser) {
    return <LoadingComponent />;
  }

  const router = createBrowserRouter([{ path: '/', element: <MainPage /> }]);

  return (
    <Suspense fallback={<LoadingComponent />}>
      <RouterProvider router={router} />
    </Suspense>
  );
}
