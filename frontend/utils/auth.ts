import { createContext, useContext, useState, useEffect } from 'react';
import { apiClient } from './api';

interface AuthContextType {
  isAuthenticated: boolean;
  userRole: string | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  userRole: null,
  login: () => {},
  logout: () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState<string | null>(null);

  useEffect(() => {
    // Check token on initial load
    const token = getToken();
    if (token) {
      validateToken(token);
    }
  }, []);

  const validateToken = async (token: string) => {
    try {
      const response = await apiClient.post('/auth/validate-token', { token });
      if (response.data.valid) {
        setIsAuthenticated(true);
        setUserRole(response.data.role);
      } else {
        removeToken();
      }
    } catch (error) {
      removeToken();
    }
  };

  const login = (token: string) => {
    // Store token in localStorage
    localStorage.setItem('authToken', token);
    setIsAuthenticated(true);
    
    // Decode token to get user role
    const payload = JSON.parse(atob(token.split('.')[1]));
    setUserRole(payload.role);
  };

  const logout = () => {
    removeToken();
    setIsAuthenticated(false);
    setUserRole(null);
  };

  return (
    <AuthContext.Provider value={{ 
      isAuthenticated, 
      userRole, 
      login, 
      logout 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// Helper functions for token management
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('authToken');
  }
  return null;
};

export const removeToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('authToken');
  }
};

// Custom hook for using auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
