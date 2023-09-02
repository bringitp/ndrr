import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import Keycloak from 'keycloak-js';
import Room from './Room';

const keycloakConfigLocal = {
  url: 'https://ron-the-rocker.net/auth',
  realm: 'ndrr',
  clientId: 'react-local',
  resource: 'test',
};

const keycloakConfigServer = {
  url: 'https://ron-the-rocker.net/auth',
  realm: 'ndrr',
  clientId: 'react-server',
  resource: 'test',
};

const useKeycloakConfig =
  process.env.NODE_ENV === 'development' ? keycloakConfigLocal : keycloakConfigServer;

const keycloak = new Keycloak(useKeycloakConfig);

function App() {
  return (
 <ReactKeycloakProvider authClient={keycloak} initOptions={{
          checkLoginIframe: false,
            }}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/room/:roomId" element={<Room />} />
          {/* 他のルートをここに追加 */}
        </Routes>
      </Router>
    </ReactKeycloakProvider>
  );
}

function Home() {
  return <div>Hello  <a href="http://localhost:3000/room/1">room -1 </a></div>;
}

export default App;
