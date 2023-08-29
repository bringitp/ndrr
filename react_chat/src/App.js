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

const useKeycloakConfig = keycloakConfigLocal;
const keycloak = new Keycloak(useKeycloakConfig);

function App() {
  return (
   <ReactKeycloakProvider authClient={keycloak}>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/rooms/:roomId" element={<Room />} />
          {/* 他のルートをここに追加 */}
        </Routes>
      </Router>
    </ReactKeycloakProvider>
  );
}
function Home() {
  return <div>Hello</div>;
}

export default App;

