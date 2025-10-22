<template>
  <div class="d-flex align-items-center justify-content-center vh-100" style="background: #ffffff;">
    <div class="card shadow-sm" style="width: 420px; border-radius: 12px;">
      <div class="card-body p-4">
        <div class="text-center mb-3">
          <div class="mb-2">
            <i class="bi bi-hospital fs-1" style="color: var(--green)"></i>
          </div>
          <h4 class="mb-0">Sign in to HMS</h4>
          <small class="text-muted">Enter your credentials to continue</small>
        </div>

        <div v-if="error" class="alert alert-danger py-2">
          {{ error }}
        </div>

        <form @submit.prevent="onSubmit" novalidate>
          <div class="mb-3">
            <label class="form-label small">Username</label>
            <input v-model.trim="form.username" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label small">Password</label>
            <div class="input-group">
              <input :type="showPassword ? 'text' : 'password'" v-model="form.password" class="form-control" required />
              <button class="btn btn-outline-secondary" type="button" @click="showPassword = !showPassword" :title="showPassword ? 'Hide' : 'Show'">
                <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
              </button>
            </div>
          </div>

          <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="form-check">
              <input v-model="remember" class="form-check-input" type="checkbox" id="remember" />
              <label class="form-check-label small" for="remember">Remember me</label>
            </div>
            <router-link to="/register" class="small">Register</router-link>
          </div>

          <div class="d-grid mb-2">
            <button class="btn btn-success" :disabled="submitting">
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
              Sign in
            </button>
          </div>

          <div class="text-center small text-muted">
            Tip: use <code>admin / admin123</code> for admin demo.
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { login } from "@/services/auth";

export default {
  name: "AuthLogin",
  data() {
    return {
      form: { username: "", password: "" },
      showPassword: false,
      remember: false,
      error: null,
      submitting: false,
    };
  },
  methods: {
    onSubmit() {
      this.error = null;
      if (!this.form.username || !this.form.password) {
        this.error = "Please enter username and password.";
        return;
      }
      this.submitting = true;
      try {
        const session = login({ username: this.form.username, password: this.form.password });
        // session contains token & user
        // redirect based on role:
        // after successful login...
        const role = session.user.role || "patient";
        if (role === "admin") this.$router.push({ name: "AdminHome" });
        else if (role === "doctor") this.$router.push({ name: "DoctorHome" });
        else this.$router.push({ name: "PatientHome" });  
      } catch (e) {
        this.error = e.message || "Login failed";
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>

<style scoped>
:root {
  --green: #0f9d58;
}
.card { border: none; }
</style>
