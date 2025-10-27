export function PageTitle({ children }: React.PropsWithChildren) {
  return (
    <div style={{ textAlign: 'center', marginBottom: '20px' }}>
      <h1>{children}</h1>
    </div>
  );
}
