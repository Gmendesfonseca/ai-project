type Props = {
  path: string[] | null;
};

export function RenderPath({ path }: Props) {
  if (!path) return null;

  const hasNoPath = path.length === 0;

  return (
    <div
      style={{
        marginBottom: '15px',
        padding: '10px',
        backgroundColor: hasNoPath ? '#ffebee' : '#e8f5e8',
        borderRadius: '8px',
        border: '1px solid '.concat(hasNoPath ? '#f44336' : '#4CAF50'),
      }}
    >
      {hasNoPath ? (
        <strong style={{ color: '#c62828' }}>Nenhum caminho encontrado</strong>
      ) : (
        <>
          <strong style={{ color: '#2E7D32' }}>Caminho encontrado: </strong>
          <span style={{ color: '#1B5E20' }}>{path.join(' → ')}</span>
        </>
      )}
    </div>
  );
}
