import { Link, useLocation } from 'react-router-dom';

interface NavigationLinkProps {
  to: string;
  children: React.ReactNode;
  icon?: string;
}

export function NavigationLink({ to, children, icon }: NavigationLinkProps) {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link
      to={to}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        padding: '0.75rem 1rem',
        color: 'white',
        textDecoration: 'none',
        borderRadius: '8px',
        fontSize: '0.9rem',
        fontWeight: '500',
        background: isActive ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
        border: isActive
          ? '1px solid rgba(255, 255, 255, 0.3)'
          : '1px solid transparent',
        transition: 'all 0.3s ease',
        boxShadow: isActive ? '0 2px 8px rgba(0, 0, 0, 0.1)' : 'none',
        whiteSpace: 'nowrap' as const,
      }}
      onMouseEnter={(e) => {
        if (!isActive) {
          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
          e.currentTarget.style.transform = 'translateY(-1px)';
        }
      }}
      onMouseLeave={(e) => {
        if (!isActive) {
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.transform = 'translateY(0)';
        }
      }}
    >
      {icon && <span style={{ fontSize: '1.2rem' }}>{icon}</span>}
      {children}
    </Link>
  );
}
