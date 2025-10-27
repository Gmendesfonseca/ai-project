export function PageContainer({ children }: React.PropsWithChildren) {
  return (
    <div
      style={{
        width: '100%',
        alignItems: 'center',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {children}
    </div>
  );
}
