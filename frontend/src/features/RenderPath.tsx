type Props = {
  path: string[] | null;
};

export function RenderPath({ path }: Props) {
  if (!path) return null;

  if (path.length === 0)
    return (
      <div
        style={{
          marginBottom: '15px',
          padding: '10px',
          backgroundColor: '#ffebee',
          borderRadius: '8px',
          border: '1px solid #f44336',
        }}
      >
        <strong style={{ color: '#c62828' }}>No Path Found</strong>
      </div>
    );

  return (
    <div
      style={{
        marginBottom: '15px',
        padding: '10px',
        backgroundColor: '#e8f5e8',
        borderRadius: '8px',
        border: '1px solid #4CAF50',
      }}
    >
      <strong style={{ color: '#2E7D32' }}>Path Found: </strong>
      <span style={{ color: '#1B5E20' }}>{path.join(' → ')}</span>
    </div>
  );
}
