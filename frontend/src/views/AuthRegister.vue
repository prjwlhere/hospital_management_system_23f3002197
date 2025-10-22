<template>
  <div class="d-flex align-items-center justify-content-center vh-100" style="background: #ffffff;">
    <div class="card shadow-sm" style="width: 640px; border-radius: 12px;">
      <div class="card-body p-4">
        <div class="d-flex mb-3 align-items-center justify-content-between">
          <div>
            <h4 class="mb-0">Create an account</h4>
            <small class="text-muted">Register as a Patient or Doctor (demo only)</small>
          </div>
          <router-link to="/login" class="small">Already have an account? Sign in</router-link>
        </div>

        <div v-if="error" class="alert alert-danger py-2">
          {{ error }}
        </div>
        <div v-if="success" class="alert alert-success py-2">
          {{ success }}
        </div>

        <form @submit.prevent="onSubmit" novalidate>
          <div class="row g-2">
            <div class="col-md-6 mb-2">
              <label class="form-label small">Full name</label>
              <input v-model.trim="form.full_name" type="text" class="form-control" required />
            </div>

            <div class="col-md-6 mb-2">
              <label class="form-label small">Role</label>
              <select v-model="form.role" class="form-select">
                <option value="patient">Patient</option>
                <option value="doctor">Doctor</option>
              </select>
            </div>

            <div class="col-md-6 mb-2">
              <label class="form-label small">Username</label>
              <input v-model.trim="form.username" type="text" class="form-control" required />
            </div>

            <div class="col-md-6 mb-2">
              <label class="form-label small">Email</label>
              <input v-model.trim="form.email" type="email" class="form-control" required />
            </div>

            <div class="col-md-6 mb-2">
              <label class="form-label small">Phone</label>
              <input v-model.trim="form.phone" type="text" class="form-control" />
            </div>

            <div class="col-md-6 mb-2">
              <label class="form-label small">Password</label>
              <input v-model="form.password" type="password" class="form-control" required />
            </div>

            <div class="col-md-6 mb-2">
              <label class="form-label small">Confirm password</label>
              <input v-model="form.confirm_password" type="password" class="form-control" required />
            </div>

            <!-- doctor-only fields (demo) -->
            <div v-if="form.role === 'doctor'" class="col-12 mb-2">
              <label class="form-label small">Qualification (optional)</label>
              <input v-model="form.qualification" type="text" class="form-control" placeholder="MBBS, MD..." />
            </div>
          </div>

          <div class="d-grid mt-3">
            <button class="btn btn-success" :disabled="submitting">
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
              Create account
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { createUser } from "@/services/auth";

export default {
  name: "AuthRegister",
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        confirm_password: "",
        role: "patient",
        full_name: "",
        phone: "",
        qualification: ""
      },
      error: null,
      success: null,
      submitting: false,
    };
  },
  methods: {
    validate() {
      if (!this.form.username || !this.form.email || !this.form.password || !this.form.confirm_password) {
        this.error = "Please fill required fields.";
        return false;
      }
      if (this.form.password !== this.form.confirm_password) {
        this.error = "Passwords do not match.";
        return false;
      }
      if (this.form.password.length < 6) {
        this.error = "Password must be at least 6 characters.";
        return false;
      }
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(this.form.email)) {
        this.error = "Invalid email address.";
        return false;
      }
      return true;
    },

    onSubmit() {
      this.error = null;
      this.success = null;
      if (!this.validate()) return;

      this.submitting = true;
      try {
        const user = createUser({
          username: this.form.username,
          email: this.form.email,
          password: this.form.password,
          role: this.form.role,
          full_name: this.form.full_name,
          phone: this.form.phone,
        });
        this.success = "Account created (demo). You can now sign in.";
        // optionally auto-redirect to login
        setTimeout(() => {
          this.$router.push({ name: "Login" });
        }, 900);
      } catch (e) {
        this.error = e.message || "Failed to create account.";
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>

<style scoped>
:root { --green: #0f9d58; }
.card { border: none; }
</style>
