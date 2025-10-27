export function PageContainer({ children }: React.PropsWithChildren) {
  return (
    <div
      style={{
        width: '100%',
        maxWidth: '1200px',
        margin: '0 auto',
      }}
    >
      {children}
    </div>
  );
}
