/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'wube-fsnd.us', // the auth0 domain prefix
    audience: 'coffeeshopapi', // the audience set for the auth0 app
    clientId: 'TjA2fS9x65oui5ZM8rb5h5hH68w1fO8V', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
