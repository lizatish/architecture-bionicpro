import React, { useEffect, useState } from 'react';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import Keycloak, { KeycloakConfig, KeycloakInitOptions } from 'keycloak-js';
import ReportPage from './components/ReportPage';
import { generateCodeVerifier, saveCodeVerifier, removeCodeVerifier, generateCodeChallenge } from './auth/pkceUtils';

const keycloakConfig: KeycloakConfig = {
  url: process.env.REACT_APP_KEYCLOAK_URL,
  realm: process.env.REACT_APP_KEYCLOAK_REALM || "",
  clientId: process.env.REACT_APP_KEYCLOAK_CLIENT_ID || ""
};

const App: React.FC = () => {
  const [initOptions, setInitOptions] = useState<KeycloakInitOptions | null>(null);

  useEffect(() => {
    const setupKeycloak = async () => {
      const codeVerifier = generateCodeVerifier();
      const codeChallenge = await generateCodeChallenge(codeVerifier);
      saveCodeVerifier(codeVerifier);

      setInitOptions({
        pkceMethod: 'S256',
        flow: 'standard',
        onLoad: 'login-required'
      });
    };

    setupKeycloak();
  }, []);

  if (!initOptions) {
    return <div>Loading...</div>;
  }

  return (
    <ReactKeycloakProvider
      authClient={new Keycloak(keycloakConfig)}
      initOptions={initOptions}
      onEvent={(event, error) => {
        if (event === 'onAuthSuccess') {
          removeCodeVerifier();
        }
        if (event === 'onAuthError') {
          console.error('Auth error:', error);
        }
      }}
    >
      <div className="App">
        <ReportPage />
      </div>
    </ReactKeycloakProvider>
  );
};

export default App;