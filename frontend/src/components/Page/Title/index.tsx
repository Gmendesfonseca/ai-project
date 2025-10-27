export function PageTitle({ children }: React.PropsWithChildren) {
  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>{children}</h1>
    </div>
  );
}
