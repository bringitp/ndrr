import React, { useEffect } from 'react';
import keycloak from './keycloak';


function Login() {
  useEffect(() => {
    // keycloakの初期化は削除する
  }, []);

  return <div>Login Page</div>;
}

export default Login;