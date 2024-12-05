import type { AppProps } from 'next/app';
import { AuthProvider } from '../utils/auth';
import Layout from '../components/common/Layout';
import '../styles/globals.css'; // Assuming you have global styles

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </AuthProvider>
  );
}

export default MyApp;
