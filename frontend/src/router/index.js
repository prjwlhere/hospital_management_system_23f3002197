// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

// views
import AuthLogin from "@/views/AuthLogin.vue";
import AuthRegister from "@/views/AuthRegister.vue";
import AdminHome from "@/views/AdminHome.vue";
import DoctorHome from "@/views/DoctorHome.vue";
import PatientHome from "@/views/PatientHome.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login",  name: "Login",    component: AuthLogin },
  { path: "/register", name: "Register", component: AuthRegister },

  // Admin dashboard entry (named exactly "AdminHome")
  { path: "/admin", name: "AdminHome", component: AdminHome },

  // placeholders for other roles
  { path: "/doctor", name: "DoctorHome", component: DoctorHome },
  { path: "/patient", name: "PatientHome", component: PatientHome },

  // fallback - optional
  { path: "/:pathMatch(.*)*", redirect: "/login" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
