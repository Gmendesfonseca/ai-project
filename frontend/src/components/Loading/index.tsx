import './styles.css';

export default function LoadingComponent() {
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        width: '100vw',
        fontSize: '24px',
      }}
    >
      <div
        style={{
          width: '50px',
          height: '50px',
          border: '5px solid #ccc',
          borderTop: '5px solid #1d72b8',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
        }}
      />
    </div>
  );
}
