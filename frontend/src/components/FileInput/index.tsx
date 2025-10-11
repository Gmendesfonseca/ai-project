type Props = {
  handleFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  helper?: React.ReactNode;
};

export default function FileInput({ handleFileUpload, helper }: Props) {
  return (
    <div style={{ marginBottom: '8px' }}>
      <label
        htmlFor="graph-file"
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '10px',
          padding: '8px 12px',
          width: '300px',
          boxSizing: 'border-box',
          border: '1px solid #e0e0e0',
          borderRadius: '8px',
          background: 'linear-gradient(180deg,#f2,#f7f7f9)',
          cursor: 'pointer',
          color: '#FFF',
          fontWeight: 600,
        }}
      >
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden
        >
          <path
            d="M12 16V4"
            stroke="#4CAF50"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <path
            d="M8 8l4-4 4 4"
            stroke="#4CAF50"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <rect x="3" y="18" width="18" height="2" rx="1" fill="#e8f5e9" />
        </svg>
        Carregar arquivo (.txt)
      </label>
      <input
        id="graph-file"
        type="file"
        accept=".txt"
        onChange={handleFileUpload}
        style={{ display: 'none' }}
      />
      {helper}
    </div>
  );
}
