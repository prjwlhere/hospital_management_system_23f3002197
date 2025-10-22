// src/services/auth.js
// Simple front-end-only auth helper for demo/testing.
// Stores users in localStorage under "hms_users" and active session under "hms_session".

const STORAGE_USERS_KEY = "hms_users";
const STORAGE_SESSION_KEY = "hms_session";

/**
 * Returns stored users array (never null).
 */
export function getStoredUsers() {
  try {
    const raw = localStorage.getItem(STORAGE_USERS_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error("Failed to parse users from localStorage", e);
    return [];
  }
}

/**
 * Save updated users list
 */
export function saveUsers(users) {
  localStorage.setItem(STORAGE_USERS_KEY, JSON.stringify(users || []));
}

/**
 * Create a new user (frontend-only). Returns created user object.
 * role: 'patient' | 'doctor' | 'admin'
 */
export function createUser({ username, email, password, role = "patient", full_name = "", phone = "" }) {
  const users = getStoredUsers();

  // basic uniqueness check
  if (users.some(u => u.username === username)) {
    throw new Error("Username already exists");
  }
  if (users.some(u => u.email === email)) {
    throw new Error("Email already registered");
  }

  // create user object (note: password stored plaintext here for demo only)
  const id = users.length ? Math.max(...users.map(u => u.id)) + 1 : 1;
  const user = {
    id,
    username,
    email,
    password, // demo only. replace with secure backend hashing in production.
    role,
    full_name,
    phone,
    is_active: true,
    blacklisted: false,
    created_at: new Date().toISOString(),
  };

  users.push(user);
  saveUsers(users);
  return user;
}

/**
 * Attempt login. Returns session object { token, user } or throws.
 * For demo: supports special admin backdoor if username==='admin' && password==='admin123'
 */
export function login({ username, password }) {
  const users = getStoredUsers();

  // backdoor admin (useful for demo)
  if (username === "admin" && password === "admin123") {
    const adminUser = users.find(u => u.username === "admin") || createUser({
      username: "admin",
      email: "admin@example.com",
      password: "admin123",
      role: "admin",
      full_name: "System Admin"
    });
    const token = "demo-admin-token";
    const session = { token, user: adminUser };
    localStorage.setItem(STORAGE_SESSION_KEY, JSON.stringify(session));
    return session;
  }

  const user = users.find(u => u.username === username);
  if (!user) throw new Error("User not found");
  if (user.password !== password) throw new Error("Invalid credentials");
  if (!user.is_active) throw new Error("User is not active");
  if (user.blacklisted) throw new Error("User is blacklisted");

  const token = "demo-token-" + user.id;
  const session = { token, user };
  localStorage.setItem(STORAGE_SESSION_KEY, JSON.stringify(session));
  return session;
}

/**
 * Logout (clear session)
 */
export function logout() {
  localStorage.removeItem(STORAGE_SESSION_KEY);
}

/**
 * Get current session or null
 */
export function getSession() {
  try {
    const raw = localStorage.getItem(STORAGE_SESSION_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}
