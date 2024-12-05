import React, { ReactNode } from 'react';
import Navbar from './Navbar';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="app-layout">
      <Navbar />
      <main>{children}main>
      <footer>
        © {new Date().getFullYear()} Vehicle Marketplace
      </footer>
    </div>
  );
};

export default Layout;
