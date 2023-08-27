import React from 'react';
import { ReactKeycloakProvider, useKeycloak } from '@react-keycloak/web';
import Keycloak from 'keycloak-js';


const keycloak = new Keycloak({
  url: 'https://ron-the-rocker.net/auth', // Keycloakの認証URL
  realm: 'ndrr',     // レルム名
  clientId: 'react-local',   // クライアントID
  resource: "test"

});

function App() {
  return (
    <ReactKeycloakProvider authClient={keycloak}>
      <MainComponent />
    </ReactKeycloakProvider>
  );
}

function MainComponent() {
  const { keycloak, initialized } = useKeycloak();

  if (!initialized) {
    return <div>Loading...</div>;
  }

  if (!keycloak.authenticated) {
    return <button onClick={() => keycloak.login()}>Login</button>;
  }

  return (
    <div>
      <p>Welcome, {keycloak.tokenParsed.preferred_username}!</p>
      <button onClick={() => keycloak.logout()}>Logout</button>
    </div>
  );
}

export default App;
