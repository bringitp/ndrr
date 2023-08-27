import React, { useEffect } from 'react';
import keycloak from './keycloak';

function Login() {
  useEffect(() => {
    keycloak.init({ onLoad: 'login-required' }).then((authenticated) => {
      if (authenticated) {
        console.log('User is authenticated');
      } else {
        console.log('User is not authenticated');
      }
    });
  }, []);

  return <div>Login Page</div>;
}

export default Login;