import React, { useState } from 'react';
import { apiClient } from '../../utils/api';
import { useAuth } from '../../utils/auth';

interface AuthenticationModalProps {
  onClose: () => void;
}

const AuthenticationModal: React.FC<AuthenticationModalProps> = ({ onClose }) => {
  const [mobileNumber, setMobileNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const { login } = useAuth();

  const sendOtp = async () => {
    try {
      await apiClient.post('/auth/send-otp', { mobileNumber });
      setOtpSent(true);
    } catch (error) {
      console.error('Failed to send OTP', error);
    }
  };

  const verifyOtp = async () => {
    try {
      const response = await apiClient.post('/auth/verify-otp', { 
        mobileNumber, 
        otp 
      });

      if (response.data.authenticated) {
        login(response.data.token);
        onClose();
      } else {
        alert('Invalid OTP');
      }
    } catch (error) {
      console.error('OTP verification failed', error);
    }
  };

  return (
    <div className="authentication-modal">
      <h2>Authentication</h2>
      
      <input
        type="tel"
        placeholder="Mobile Number"
        value={mobileNumber}
        onChange={(e) => setMobileNumber(e.target.value)}
        disabled={otpSent}
      />

      {!otpSent ? (
        <button onClick={sendOtp}>Send OTP</button>
      ) : (
        <>
          <input
            type="text"
            placeholder="Enter OTP"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
          />
          <button onClick={verifyOtp}>Verify OTP</button>
        </>
      )}

      <button onClick={onClose}>Close</button>
    </div>
  );
};

export default AuthenticationModal;
