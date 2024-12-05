import React, { useState } from 'react';
import AuthenticationModal from '../components/user/AuthenticationModal';
import { useRouter } from 'next/router';

const LoginPage: React.FC = () => {
  const [showAuthModal, setShowAuthModal] = useState(false);
  const router = useRouter();

  const handleOpenAuthModal = () => {
    setShowAuthModal(true);
  };

  const handleCloseAuthModal = () => {
    setShowAuthModal(false);
  };

  return (
    <div className="login-page">
      <h1>Welcome to Vehicle Marketplace</h1>
      
      <div className="login-options">
        <button onClick={handleOpenAuthModal}>
          Login with Mobile Number
        </button>
      </div>

      {showAuthModal && (
        <AuthenticationModal onClose={handleCloseAuthModal} />
      )}
    </div>
  );
};

export default LoginPage;
