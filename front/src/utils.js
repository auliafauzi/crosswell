import router from './router/index';

export const BASE_URL = 'https://antares.pede.id/sg-web-service/v1';

export const TOKEN_KEY = 'token';

export const USER_DATA_KEY = 'userData';

export const USER_DATA_NAME = 'userName';

export const USER_PERMISSIONS_KEY = 'userPermissions';

export const USER_ROLES = [{ text: 'Superadmin', value: '1', disabled: true }, { text: 'Admin', value: '2' }, { text: 'User', value: '3' }];

export const RELATION_TO_CLIENT = [{ text: 'Peer', value: 'peer' }, { text: 'User', value: 'user' }, { text: 'Friend', value: 'friend' }];


export const setToken = token => localStorage.setItem(TOKEN_KEY, token);

export const getToken = () => localStorage.getItem(TOKEN_KEY);

export const getUserDataInSession2 = (LocalVar) => localStorage.getItem(LocalVar);

// export const datauser = {}

export const clearToken = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_DATA_KEY);
};

export const isLoggedIn = () => {
  const idToken = getToken();
  return !!idToken;
};

export const logout = () => {
  clearToken();
  router.go('/login');
};

export const saveUserDataInSession = (data) => {
  localStorage.setItem(USER_DATA_KEY, JSON.stringify(data));
  localStorage.setItem(USER_DATA_NAME, getUserName());
};

export const saveUserDataInSession2 = (LocalVar,data) => {
  localStorage.setItem(LocalVar, JSON.stringify(data));
  // localStorage.setItem(USER_DATA_NAME, getUserName());
};

export const getUserName = () => {
  const userData = getUserDataFromSession();
  if (userData) {
    return userData.name;
  }
  return 'user';
};

export const getUserDataFromSession = () => JSON.parse(localStorage.getItem(USER_DATA_KEY));

export const getUserPermissionsFromSession = () => {
  if (getUserDataFromSession() === null) {
    return { items: [] };
  }
  return { items: getUserDataFromSession().permissions };
};
