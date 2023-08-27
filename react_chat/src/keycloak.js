import Keycloak from 'keycloak-js';

const keycloakConfig = {
  url: 'https://ron-the-rocker.net/auth',
  realm: 'ndrr',
  clientId: 'react-client-local',
  credentials: {
    secret: 'j7Edln00hjjhtPpVXwB2wNdwpzNSSeAD'
  },
  redirectUri: 'http://localhost:3000/*',

  // SSOの設定を追加
  checkLoginIframe: false, // SSOクッキーチェックを無効化
  silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html', // サイレントチェック用のリダイレクトURI
  onLoad: 'check-sso' // ロード時にSSOのチェックを行う
};

const keycloak = new Keycloak(keycloakConfig);

export default keycloak;
