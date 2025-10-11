export default function Label({ children }: React.PropsWithChildren) {
  return (
    <label
      style={{
        display: 'block',
        marginBottom: '5px',
        fontWeight: 'bold',
      }}
    >
      {children}
    </label>
  );
}
