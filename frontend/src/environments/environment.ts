/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */
const secret = require('secrets.js');

// import * as dotenv from 'dotenv';
// dotenv.config();

export const environment = {
  production: false,
  apiServerUrl: secret.API_SERVER_URL, // the running FLASK api server url
  auth0: {
    url: secret.DOMAIN_PREFIX, // the auth0 domain prefix
    audience: secret.AUDIENCE, // the audience set for the auth0 app
    clientId: secret.CLIENT_ID, // the client id generated for the auth0 app
    callbackURL: secret.CALLBACK_URL, // the base url of the running ionic application. 
  }
};