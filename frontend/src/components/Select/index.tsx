type Props = Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'children'> & {
  options: { label: string; value: string }[];
};

export default function Select({ options, ...props }: Props) {
  return (
    <select
      disabled={options.length === 0}
      style={{
        width: '300px',
        padding: '8px',
        marginBottom: '10px',
        boxSizing: 'border-box',
      }}
      {...props}
    >
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
