import router from './router/index';

// export const BASE_URL = 'http://127.0.0.1:5000';
export const BASE_URL = 'http://159.89.105.228:5000';

export const TOKEN_KEY = 'token';

export const USER_DATA_KEY = 'userData';

export const USER_DATA_NAME = 'userName';

export const USER_PERMISSIONS_KEY = 'userPermissions';

export const USER_ROLES = [{ text: 'Superadmin', value: '1', disabled: true }, { text: 'Admin', value: '2' }, { text: 'User', value: '3' }, { text: 'Visitor', value: '0' }];

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

export const checkUser = () => {
  let token = null
  token = getToken()
  // console.log('here1')
  if (token == null || token == '' || token == undefined){
    // console.log('here2')
    saveUserDataInSession2('UserName','Visitor')
    saveUserDataInSession2('UserRole',0)
  }
  else {
    // console.log('here3')
    return
  }
};
