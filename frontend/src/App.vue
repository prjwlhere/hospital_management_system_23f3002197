<template>
  <div id="app">
    <!-- AUTH PAGES -->
    <div v-if="isAuthPage" class="auth-wrapper">
      <router-view />
    </div>

    <!-- ADMIN LAYOUT -->
    <div v-else>
      <!-- NAVBAR -->
      <nav class="navbar navbar-expand-lg shadow-sm bg-white py-2 fixed-top">
        <div class="container-fluid align-items-center">
          <div class="d-flex align-items-center gap-3">
            <!-- mobile drawer button -->
            <button
              class="btn btn-link p-0 d-md-none text-decoration-none"
              @click="sidebarOpen = true"
              aria-label="Open sidebar"
            >
              <i class="bi bi-list text-success fs-4" />
            </button>

            <div class="d-flex align-items-center gap-2">
              <img src="./assets/MMM-removebg-preview.png" alt="Logo" class="logo-img" />
              <div class="brand-text">
                <div class="h6 mb-0 text-success"><b>CareSlot</b></div>
                <small class="text-muted">By <b class="text-danger">MarkMyMeet</b></small>
              </div>
            </div>
          </div>

          <div class="d-flex align-items-center gap-3 ms-auto">
            <div class="d-none d-md-block">
              <input v-model="globalSearch" class="form-control form-control-sm search-input"
                     placeholder="Search doctors, patients, appointments..." />
            </div>

            <div class="dropdown">
              <button class="btn btn-sm btn-outline-secondary dropdown-toggle" id="userMenu" data-bs-toggle="dropdown">
                <i class="bi bi-person-circle me-1"></i> Admin
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item text-danger" href="#" @click.prevent="doLogout">Logout</a></li>
              </ul>
            </div>
          </div>
        </div>
      </nav>

      <!-- SIDEBAR -->
      <aside
        :class="[
          'sidebar bg-success text-white d-flex flex-column',
          { collapsed: sidebarCollapsed && !isMobile, 'drawer-open': sidebarOpen }
        ]"
      >
        <div class="sidebar-top p-3 d-flex align-items-center justify-content-between">
          <span v-if="!sidebarCollapsed || isMobile" class="fw-semibold">Menu</span>
          <div class="d-flex">
            <button
              class="btn btn-sm btn-light text-success me-1 d-none d-md-inline"
              @click="toggleCollapse"
              :aria-pressed="sidebarCollapsed"
            >
              <i class="bi" :class="sidebarCollapsed ? 'bi-arrow-bar-right' : 'bi-arrow-bar-left'"></i>
            </button>
            <button class="btn btn-sm btn-light text-success d-md-none" @click="sidebarOpen = false">
              <i class="bi bi-x-lg" />
            </button>
          </div>
        </div>

        <nav class="nav flex-column px-2 mb-3 gap-2">
          <a
            v-for="item in navItems"
            :key="item.name"
            href="#"
            class="nav-link text-white py-2 d-flex align-items-center gap-2"
            :class="{ active: active === item.name }"
            @click.prevent="go(item.name)"
          >
            <i :class="['bi', item.icon, 'sidebar-icon']"></i>
            <span class="sidebar-label" v-if="!sidebarCollapsed || isMobile">{{ item.label }}</span>
          </a>
        </nav>

        <div class="sidebar-bottom mt-auto p-3">
          <div class="small text-white-50 mb-2" v-if="!sidebarCollapsed || isMobile">Quick actions</div>
          <div class="d-grid gap-2">
            <button class="btn btn-sm btn-light text-danger" @click="doLogout">
              <i class="bi bi-box-arrow-right" /> <span v-if="!sidebarCollapsed || isMobile">Logout</span>
            </button>
            <button class="btn btn-sm btn-outline-light" @click="go('profile')">
              <i class="bi bi-gear-fill" /> <span v-if="!sidebarCollapsed || isMobile">Update Profile</span>
            </button>
          </div>
        </div>
      </aside>

      <!-- overlay for mobile -->
      <div v-if="sidebarOpen && isMobile" class="overlay" @click="sidebarOpen = false"></div>

      <!-- CONTENT AREA -->
      <main class="content-area" :style="contentAreaStyle">
        <div class="content-inner p-4">
          <transition name="fade-slide" mode="out-in">
            <AdminDashboard
              v-if="isAdminRoute"
              :global-search="globalSearch"
              :active-section="active"
              key="admin-dashboard"
            />
            <router-view v-else key="route-view" />
          </transition>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import AdminDashboard from "@/components/AdminDashboard.vue";

export default {
  name: "App",
  components: { AdminDashboard },
  data() {
    return {
      globalSearch: "",
      sidebarCollapsed: false,
      sidebarOpen: false,
      active: "dashboard",
      navItems: [
        { name: "dashboard", label: "Dashboard", icon: "bi-speedometer2" },
        { name: "doctors", label: "Doctors", icon: "bi-person-badge" },
        { name: "patients", label: "Patients", icon: "bi-people-fill" },
        { name: "appointments", label: "Appointments", icon: "bi-calendar-check" },
      ],
      autoCollapseWidth: 1100,
      resizeDebounceMs: 150,
      windowWidth: window.innerWidth,
    };
  },
  computed: {
    isAuthPage() {
      const n = this.$route?.name?.toLowerCase() || "";
      return n === "login" || n === "register";
    },
    isAdminRoute() {
      const name = this.$route?.name || "";
      return name === "AdminHome" || name === "Admin" || name === "";
    },
    isMobile() {
      return this.windowWidth < 992;
    },
    contentAreaStyle() {
      if (this.isMobile) return { left: 0 };
      return {
        left: this.sidebarCollapsed ? `var(--sidebar-collapsed-w)` : `var(--sidebar-w)`,
      };
    },
  },
  mounted() {
    const stored = localStorage.getItem("hms_sidebar_collapsed");
    if (stored !== null) this.sidebarCollapsed = stored === "1";

    this.handleResize();
    this._resizeTimer = null;
    window.addEventListener("resize", this._onResize);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this._onResize);
    if (this._resizeTimer) clearTimeout(this._resizeTimer);
  },
  methods: {
    toggleCollapse() {
      if (this.isMobile) return;
      this.sidebarCollapsed = !this.sidebarCollapsed;
      localStorage.setItem("hms_sidebar_collapsed", this.sidebarCollapsed ? "1" : "0");
    },
    go(section) {
      this.active = section;
      if (this.isMobile) this.sidebarOpen = false;
    },
    doLogout() {
      localStorage.removeItem("hms_session");
      this.$router.push({ name: "Login" });
    },
    _onResize() {
      if (this._resizeTimer) clearTimeout(this._resizeTimer);
      this._resizeTimer = setTimeout(() => this.handleResize(), this.resizeDebounceMs);
    },
    handleResize() {
      this.windowWidth = window.innerWidth || document.documentElement.clientWidth;
      if (!this.isMobile) {
        this.sidebarCollapsed = this.windowWidth > this.autoCollapseWidth;
        this.sidebarOpen = false;
      }
    },
  },
};
</script>

<style>
:root {
  --green: #0f9d58;
  --green-2: #0b7a44;
  --app-bg: #fff;
  --sidebar-w: 220px;
  --sidebar-collapsed-w: 70px;
  --navbar-h: 64px;
  --footer-h: 56px;
  --anim-speed: 280ms;
  --anim-ease: cubic-bezier(.2,.9,.2,1);
}

html, body, #app {
  height: 100%;
  margin: 0;
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto;
  overflow: hidden;
}

.navbar { height: var(--navbar-h); }

.logo-img { width: 90px; height: auto; transition: width 0.3s ease; }
.brand-text { transition: transform 0.3s ease; }

.sidebar {
  position: fixed;
  top: var(--navbar-h);
  bottom: 0;
  left: 0;
  width: var(--sidebar-w);
  background: linear-gradient(180deg, var(--green), var(--green-2));
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease, transform 0.3s ease;
  z-index: 1050;
}
.sidebar.collapsed { width: var(--sidebar-collapsed-w); }
.sidebar-icon { font-size: 1.2rem; transition: font-size 0.3s ease; }
.sidebar-label { transition: opacity 0.3s ease, transform 0.3s ease; }
.sidebar.collapsed .sidebar-icon { font-size: 1rem; }
.sidebar.collapsed .sidebar-label { opacity: 0; transform: translateX(-10px); pointer-events: none; }

/* Mobile drawer */
@media (max-width: 991.98px) {
  .sidebar { transform: translateX(-100%); }
  .sidebar.drawer-open { transform: translateX(0); }
  .content-area { left: 0 !important; }
}

.content-area { position: fixed; top: var(--navbar-h); bottom: 0; right: 0; overflow-y: auto; transition: left 0.3s ease; }
.sidebar.collapsed ~ .content-area { left: var(--sidebar-collapsed-w); }

.overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.35); z-index: 1040; }
</style>
