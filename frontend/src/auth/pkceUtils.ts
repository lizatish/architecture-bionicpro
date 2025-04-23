import { encode } from 'js-base64';

export const generateCodeVerifier = (): string => {
  const array = new Uint8Array(32);
  window.crypto.getRandomValues(array);

  // Convert Uint8Array to string without spread operator
  let str = '';
  for (let i = 0; i < array.length; i++) {
    str += String.fromCharCode(array[i]);
  }

  const base64 = btoa(str);
  return base64
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
};

export const generateCodeChallenge = async (verifier: string): Promise<string> => {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await window.crypto.subtle.digest('SHA-256', data);

  // Convert ArrayBuffer without spread operator
  const hashArray = new Uint8Array(digest);
  let str = '';
  for (let i = 0; i < hashArray.length; i++) {
    str += String.fromCharCode(hashArray[i]);
  }

  const base64 = btoa(str);
  return base64
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
};
// Save verifier to sessionStorage
export const saveCodeVerifier = (verifier: string): void => {
  sessionStorage.setItem('pkce_code_verifier', verifier);
};

// Get saved verifier
export const getCodeVerifier = (): string | null => {
  return sessionStorage.getItem('pkce_code_verifier');
};

// Remove verifier after use
export const removeCodeVerifier = (): void => {
  sessionStorage.removeItem('pkce_code_verifier');
};