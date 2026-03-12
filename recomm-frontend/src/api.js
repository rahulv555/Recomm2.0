// api.js
import { auth } from './firebase-config'; //

const BASE_URL = "http://localhost:4005/api";

export const apiCall = async (endpoint, method = 'GET', body = null) => {
  const user = auth.currentUser;
  if (!user) throw new Error("User not authenticated");

  const token = await user.getIdToken();
  console.log(token);
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}` // Standard Bearer token
  };

  const options = { method, headers };
  if (body) options.body = JSON.stringify(body);

  const response = await fetch(`${BASE_URL}${endpoint}`, options);
  
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.message || "API request failed");
  }
  
  // Return empty object for 204 No Content or endpoints like PATCH that return nothing
  const text = await response.text();
  return text ? JSON.parse(text) : {}; 
};