import React, { useState, useEffect } from 'react';
import { ReactKeycloakProvider, useKeycloak } from '@react-keycloak/web';
import Keycloak from 'keycloak-js';

const keycloakConfigLocal = {
  url: 'https://ron-the-rocker.net/auth',
  realm: 'ndrr',
  clientId: 'react-local',
  resource: 'test'
};

const keycloakConfigServer = {
  url: 'https://ron-the-rocker.net/auth',
  realm: 'ndrr',
  clientId: 'react-server',
  resource: 'test'
};

const useKeycloakConfig = process.env.REACT_APP_ENV === 'server' ? keycloakConfigServer : keycloakConfigLocal;

const keycloak = new Keycloak(useKeycloakConfig);

function App() {
  return (
    <ReactKeycloakProvider authClient={keycloak}>
      <MainComponent />
    </ReactKeycloakProvider>
  );
}

function MainComponent() {
  const { keycloak, initialized } = useKeycloak();
  const [jsonData, setJsonData] = useState(null);

  useEffect(() => {
    if (initialized && keycloak.authenticated) {
      const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/ndrr/static')
        ? 'https://ron-the-rocker.net/ndrr/api/rooms/1/messages'
        : 'http://localhost:7777/rooms/1/messages';

      const headers = new Headers();
      headers.append('Authorization', `Bearer ${keycloak.token}`);

      const fetchData = async () => {
        try {
          const response = await fetch(apiUrl, { headers });
          if (response.ok) {
            const data = await response.json();
            setJsonData(data);
          } else {
            console.error('Error fetching data:', response.status);
          }
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };

      // Fetch data initially and set interval for regular updates
      fetchData();
      const fetchInterval = setInterval(fetchData, 2000);

      return () => {
        clearInterval(fetchInterval);
      };
    }
  }, [initialized, keycloak.authenticated]);

  if (!initialized) {
    return <div>Loading...</div>;
  }

  if (!keycloak.authenticated) {
    return <button onClick={() => keycloak.login()}>Login</button>;
  }

  return (
    <div>
      <p>Welcome</p>
      <button onClick={() => keycloak.logout()}>Logout</button>

      {jsonData ? (
        <pre>{JSON.stringify(jsonData, null, 2)}</pre>
      ) : (
        <div>Loading JSON data...</div>
      )}
    </div>
  );
}

export default App;
