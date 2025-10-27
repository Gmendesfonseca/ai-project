export function PageContent({ children }: React.PropsWithChildren) {
  return (
    <div
      style={{
        marginTop: '30px',
        display: 'flex',
        gap: '40px',
      }}
    >
      {children}
    </div>
  );
}
