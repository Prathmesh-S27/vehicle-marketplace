import React from 'react';
import Link from 'next/link';
import { useAuth } from '../../utils/auth';

const Navbar: React.FC = () => {
  const { isAuthenticated, logout, userRole } = useAuth();

  return (
    <nav>
      <div className="logo">
        <Link href="/">Vehicle Marketplace</Link>
      </div>
      
      <div className="nav-links">
        <Link href="/search">Search Vehicles</Link>
        
        {isAuthenticated && userRole === 'admin' && (
          <>
            <Link href="/admin/dashboard">Admin Dashboard</Link>
            <Link href="/admin/vehicles">Vehicle Management</Link>
            <Link href="/admin/users">User Management</Link>
          </>
        )}

        {isAuthenticated ? (
          <>
            <Link href="/user/profile">Profile</Link>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <Link href="/login">Login</Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
