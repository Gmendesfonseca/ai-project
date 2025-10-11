import HelperText from '../HelperText';
import Label from '../Label';

type Props = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

export default function Input({ label, error, ...props }: Props) {
  return (
    <div>
      {label && <Label>{label}</Label>}
      <input
        style={{
          width: '300px',
          padding: '8px',
          marginBottom: '5px',
          boxSizing: 'border-box',
        }}
        {...props}
      />
      {error && <HelperText>{error}</HelperText>}
    </div>
  );
}
