<template>
  <div>
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="mb-0 text-success">{{ headerTitle }}</h3>
        <small class="text-muted">{{ headerSubtitle }}</small>
      </div>

      <div class="d-flex gap-2 align-items-center">
        <button class="btn btn-sm btn-outline-success" @click="refreshData">
          <i class="bi bi-arrow-clockwise"></i> Refresh
        </button>
      </div>
    </div>

    <!-- === DASHBOARD: analytics & KPIs === -->
    <section v-if="activeSection === 'dashboard'">
      <div class="row g-3 mb-4">
        <div class="col-lg-3" v-for="c in kpis" :key="c.label">
          <div class="card p-3">
            <div class="small text-muted">{{ c.label }}</div>
            <div class="d-flex align-items-baseline justify-content-between">
              <h4 class="fw-bold mb-0 text-success">{{ c.value }}</h4>
              <i :class="c.icon" class="fs-3 text-muted"></i>
            </div>
            <small class="text-muted d-block mt-2">{{ c.help }}</small>
          </div>
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-lg-8">
          <div class="card p-3">
            <div class="d-flex justify-content-between mb-2">
              <strong>Appointments — last 14 days</strong>
              <small class="text-muted">Trend</small>
            </div>
            <canvas id="appointmentsChart" height="140"></canvas>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card p-3">
            <div class="d-flex justify-content-between mb-2">
              <strong>Doctors by Specialization</strong>
              <small class="text-muted">Distribution</small>
            </div>
            <canvas id="doctorsChart" height="200"></canvas>
          </div>
        </div>
      </div>

      <!-- quick actions -->
      <div class="card mb-4">
        <div class="card-body d-flex gap-2 flex-wrap align-items-center">
          <button class="btn btn-success" @click="openDoctorModal"><i class="bi bi-person-plus"></i> Add Doctor</button>
          <button class="btn btn-success" @click="openPatientModal"><i class="bi bi-person-plus-fill"></i> Add Patient</button>
          <button class="btn btn-outline-success" @click="exportAppointments"><i class="bi bi-download"></i> Export Appointments</button>
          <button class="btn btn-danger" @click="bulkBlacklist"><i class="bi bi-slash-circle-fill"></i> Bulk Blacklist (demo)</button>
        </div>
      </div>
    </section>

    <!-- === DOCTORS: management === -->
    <section v-if="activeSection === 'doctors'">
      <div class="card mb-3">
        <div class="card-header bg-white d-flex justify-content-between align-items-center">
          <strong>Manage Doctors</strong>
          <div class="d-flex gap-2">
            <input v-model="filters.doctor" class="form-control form-control-sm" placeholder="Search doctors" />
            <button class="btn btn-sm btn-success" @click="openDoctorModal"><i class="bi bi-plus-lg"></i> Add</button>
          </div>
        </div>
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>Name</th><th>Specialization</th><th>Contact</th><th>Available</th><th class="text-end">Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="doc in filteredDoctors" :key="doc.id" :class="{ 'table-danger': doc.blacklisted }">
                <td>{{ doc.name }}</td>
                <td>{{ doc.specialization }}</td>
                <td>{{ doc.phone }}</td>
                <td>{{ doc.is_available ? 'Yes' : 'No' }}</td>
                <td class="text-end">
                  <button class="btn btn-sm btn-outline-success me-1" @click="editDoctor(doc)"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-sm btn-danger" @click="toggleBlacklistDoctor(doc)"><i class="bi bi-slash-circle"></i></button>
                </td>
              </tr>
              <tr v-if="filteredDoctors.length === 0"><td colspan="5" class="text-center py-3 text-muted">No doctors</td></tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="card mb-3">
        <div class="card-header bg-white d-flex justify-content-between align-items-center">
          <strong>Manage Specializations</strong>
          <div class="d-flex gap-2">
            <input v-model="filters.specializations" class="form-control form-control-sm" placeholder="Search Specializations" />
            <button class="btn btn-sm btn-success" @click="openDoctorModal"><i class="bi bi-plus-lg"></i> Add</button>
          </div>
        </div>
        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>Name</th><th>Specialization</th><th>Description</th><th class="text-end">Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="doc in filteredSpecializations" :key="doc.id" :class="{ 'table-danger': doc.blacklisted }">
                <td>{{ doc.id }}</td>
                <td>{{ doc.specialization }}</td>
                <td>{{ doc.description }}</td>
                <td class="text-end">
                  <button class="btn btn-sm btn-outline-success me-1" @click="editDoctor(doc)"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-sm btn-danger" @click="toggleBlacklistDoctor(doc)"><i class="bi bi-slash-circle"></i></button>
                </td>
              </tr>
              <tr v-if="filteredDoctors.length === 0"><td colspan="5" class="text-center py-3 text-muted">No doctors</td></tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- Doctor details / availability quick-edit -->
      <!-- <div class="card">
        <div class="card-header bg-white"><strong>Doctor Availability (Quick Edit)</strong></div>
        <div class="card-body">
          <small class="text-muted">Select a doctor to edit availability (demo)</small>
          <div class="mt-3 d-flex gap-2 flex-wrap">
            <select v-model="availabilityDoctorId" class="form-select form-select-sm" style="max-width:250px;">
              <option :value="null">Select doctor</option>
              <option v-for="d in doctors" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
            <input type="date" v-model="availDate" class="form-control form-control-sm" style="max-width:180px"/>
            <input v-model="availSlot" placeholder="09:00-09:30" class="form-control form-control-sm" style="max-width:160px"/>
            <button class="btn btn-sm btn-success" @click="addAvailability">Add Slot</button>
          </div>
          <div class="mt-3">
            <small class="text-muted">Current availability (demo list)</small>
            <ul class="list-group list-group-flush mt-2">
              <li class="list-group-item" v-for="(s,i) in sampleAvailability" :key="i">
                <strong>{{ s.doctorName }}</strong> — {{ s.date }} @ {{ s.slot }}
              </li>
            </ul>
          </div>
        </div>
      </div> -->
    </section>

    <!-- === PATIENTS: management === -->
    <section v-if="activeSection === 'patients'">
      <div class="card mb-3">
        <div class="card-header bg-white d-flex justify-content-between align-items-center">
          <strong>Manage Patients</strong>
          <div class="d-flex gap-2">
            <input v-model="filters.patient" class="form-control form-control-sm" placeholder="Search patients (name / id / contact)" />
            <button class="btn btn-sm btn-success" @click="openPatientModal"><i class="bi bi-plus-lg"></i> Add</button>
          </div>
        </div>

        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>Name</th><th>Patient ID</th><th>Contact</th><th>Last Visit</th><th class="text-end">Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="p in filteredPatients" :key="p.id" :class="{ 'table-danger': p.blacklisted }">
                <td>{{ p.name }}</td>
                <td>{{ p.pid }}</td>
                <td>{{ p.phone }}</td>
                <td>{{ p.last_visit || '—' }}</td>
                <td class="text-end">
                  <button class="btn btn-sm btn-outline-success me-1" @click="editPatient(p)"><i class="bi bi-pencil"></i></button>
                  <button class="btn btn-sm btn-danger" @click="toggleBlacklistPatient(p)"><i class="bi bi-slash-circle"></i></button>
                </td>
              </tr>
              <tr v-if="filteredPatients.length === 0"><td colspan="5" class="text-center py-3 text-muted">No patients</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- patient quick export -->
      <div class="card">
        <div class="card-body d-flex gap-2 align-items-center">
          <div>
            <div class="small text-muted">Export patient treatment history</div>
            <div class="text-muted small">CSV export — runs as background job</div>
          </div>
          <div class="ms-auto">
            <button class="btn btn-success" @click="triggerExport"><i class="bi bi-file-earmark-arrow-up"></i> Export CSV</button>
          </div>
        </div>
      </div>
    </section>

    <!-- === APPOINTMENTS: management === -->
    <section v-if="activeSection === 'appointments'">
      <div class="card mb-3">
        <div class="card-header bg-white d-flex justify-content-between align-items-center">
          <strong>Manage Appointments</strong>
          <div class="d-flex gap-2">
            <select v-model="filters.status" class="form-select form-select-sm">
              <option value="">All</option>
              <option value="booked">Booked</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
            <input v-model="filters.date" type="date" class="form-control form-control-sm" />
          </div>
        </div>

        <div class="card-body p-0">
          <table class="table table-hover mb-0">
            <thead class="table-light">
              <tr><th>ID</th><th>Date</th><th>Time</th><th>Doctor</th><th>Patient</th><th>Status</th><th class="text-end">Actions</th></tr>
            </thead>
            <tbody>
              <tr v-for="a in filteredAppointments" :key="a.id">
                <td>{{ a.id }}</td>
                <td>{{ a.date }}</td>
                <td>{{ a.time }}</td>
                <td>{{ getDoctorName(a.doctor_id) }}</td>
                <td>{{ getPatientName(a.patient_id) }}</td>
                <td><span :class="badgeClass(a.status)">{{ a.status }}</span></td>
                <td class="text-end">
                  <button class="btn btn-sm btn-outline-primary me-1" @click="StatusHistoryPlaceholder(a)">Status History</button>
                  <button class="btn btn-sm btn-outline-success me-1" @click="setAppointmentStatus(a,'completed')">Complete</button>
                  <button class="btn btn-sm btn-danger me-1" @click="setAppointmentStatus(a,'cancelled')">Cancel</button>
                  <button class="btn btn-sm btn-outline-primary" @click="reschedulePlaceholder(a)"><i class="bi bi-file-text"></i>Treatment</button>
                </td>
              </tr>
              <tr v-if="filteredAppointments.length === 0"><td colspan="7" class="text-center py-3 text-muted">No appointments</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- appointment stats quick -->
      <div class="row g-3">
        <div class="col-md-6">
          <div class="card p-3">
            <div class="small text-muted">Upcoming Today</div>
            <div class="h5 fw-bold">{{ todayAppointments.length }}</div>
            <small class="text-muted">Appointments for current date</small>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card p-3">
            <div class="small text-muted">Missed / No-shows</div>
            <div class="h5 fw-bold">{{ missedCount }}</div>
            <small class="text-muted">Manual review recommended</small>
          </div>
        </div>
      </div>
    </section>

    <!-- === REPORTS: monthly & export management === -->
    <section v-if="activeSection === 'reports'">
      <div class="row g-3">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <strong>Monthly Reports</strong>
              <div>
                <select v-model="reportFilter.doctor" class="form-select form-select-sm">
                  <option value="">All doctors</option>
                  <option v-for="d in doctors" :key="d.id" :value="d.id">{{ d.name }}</option>
                </select>
              </div>
            </div>
            <div class="card-body p-0">
              <table class="table mb-0">
                <thead class="table-light"><tr><th>Doctor</th><th>Month</th><th>Year</th><th class="text-end">Actions</th></tr></thead>
                <tbody>
                  <tr v-for="r in sampleReports" :key="r.id">
                    <td>{{ getDoctorName(r.doctor_id) }}</td>
                    <td>{{ r.month }}</td>
                    <td>{{ r.year }}</td>
                    <td class="text-end">
                      <button class="btn btn-sm btn-outline-success me-1">View</button>
                      <button class="btn btn-sm btn-success" @click="downloadReport(r)"><i class="bi bi-download"></i> Download</button>
                    </td>
                  </tr>
                  <tr v-if="sampleReports.length===0"><td colspan="4" class="text-center py-3 text-muted">No reports</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="card p-3">
            <div class="d-flex justify-content-between mb-2">
              <strong>Export Jobs</strong>
              <small class="text-muted">Background jobs</small>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item d-flex justify-content-between align-items-center" v-for="job in exportJobs" :key="job.id">
                <div>
                  <div><strong>{{ getUserName(job.user_id) }}</strong> — {{ job.job_type }}</div>
                  <small class="text-muted">Status: {{ job.status }} • requested {{ job.created_at }}</small>
                </div>
                <div>
                  <button class="btn btn-sm btn-outline-secondary me-1" @click="viewExport(job)">View</button>
                  <button class="btn btn-sm btn-danger" @click="cancelExport(job)">Cancel</button>
                </div>
              </li>
              <li v-if="exportJobs.length===0" class="list-group-item text-center text-muted py-3">No export jobs</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Modals (Doctor/Patient) -->
    <div v-if="showDoctorModal" class="modal-backdrop d-flex align-items-center justify-content-center">
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="saveDoctor">
            <div class="modal-header"><h5 class="modal-title">{{ editingDoctor ? 'Edit Doctor' : 'Add Doctor' }}</h5></div>
            <div class="modal-body">
              <input v-model="doctorForm.name" class="form-control mb-2" placeholder="Name" required/>
              <input v-model="doctorForm.specialization" class="form-control mb-2" placeholder="Specialization" required/>
              <input v-model="doctorForm.phone" class="form-control" placeholder="Phone"/>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeDoctorModal">Close</button>
              <button type="submit" class="btn btn-success">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showPatientModal" class="modal-backdrop d-flex align-items-center justify-content-center">
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="savePatient">
            <div class="modal-header"><h5 class="modal-title">{{ editingPatient ? 'Edit Patient' : 'Add Patient' }}</h5></div>
            <div class="modal-body">
              <input v-model="patientForm.name" class="form-control mb-2" placeholder="Name" required/>
              <input v-model="patientForm.pid" class="form-control mb-2" placeholder="Patient ID" required/>
              <input v-model="patientForm.phone" class="form-control" placeholder="Phone"/>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closePatientModal">Close</button>
              <button type="submit" class="btn btn-success">Save</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* global Chart */
export default {
  name: "AdminDashboard",
  props: {
    globalSearch: { type: String, default: "" },
    activeSection: { type: String, default: "dashboard" },
  },
  data() {
    return {
      // static demo data (replace with API)
      doctors: [
        { id: 1, name: "Dr John Smith", specialization: "Cardiology", phone: "+91 9876543210", blacklisted: false, is_available: true },
        { id: 2, name: "Dr Alice Park", specialization: "Orthopedics", phone: "+91 2223334444", blacklisted: false, is_available: true },
        { id: 3, name: "Dr Bob Lee", specialization: "Dermatology", phone: "+91 9998887777", blacklisted: true, is_available: false },
      ],
      specializations : [
        { id: 1, specialization: "Cardiology", description: "This is new"},
        { id: 2, specialization: "Orthopedics", description: "This is new"},
        { id: 3, specialization: "Dermatology", description: "This is new"},
      ],
      patients: [
        { id: 101, pid: "P1001", name: "John Doe", phone: "+91 9876543210", blacklisted: false, last_visit: "2025-09-20" },
        { id: 102, pid: "P1002", name: "Jane Roe", phone: "+91 7776665555", blacklisted: false, last_visit: "2025-08-10" },
      ],
      appointments: [
        { id: 1001, date: "2025-10-05", time: "09:00", doctor_id: 1, patient_id: 101, status: "booked" },
        { id: 1002, date: "2025-09-20", time: "10:30", doctor_id: 2, patient_id: 102, status: "completed" },
        { id: 1003, date: this._dateOffset(-2), time: "11:00", doctor_id: 1, patient_id: 102, status: "cancelled" },
      ],

      sampleAvailability: [
        { doctorId: 1, doctorName: "Dr John Smith", date: this._dateOffset(1), slot: "09:00-10:00" }
      ],
      sampleReports: [{ id: 1, doctor_id: 1, month: "September", year: 2025 }],
      exportJobs: [{ id: 1, user_id: 1, job_type: "treatment_export", status: "pending", created_at: "2025-09-29" }],

      // UI & Modals
      filters: { doctor: "", patient: "", status: "", date: "" },
      showDoctorModal: false,
      showPatientModal: false,
      editingDoctor: null,
      editingPatient: null,
      doctorForm: { id: null, name: "", specialization: "", phone: "" },
      patientForm: { id: null, pid: "", name: "", phone: "" },

      // availability quick-edit state
      availabilityDoctorId: null,
      availDate: null,
      availSlot: "",

      charts: { appointmentsChart: null, doctorsChart: null }
    };
  },
  computed: {
    headerTitle() {
      return this.activeSection === "dashboard" ? "Admin Dashboard" :
             this.activeSection === "doctors" ? "Doctors & Specializations Management" :
             this.activeSection === "patients" ? "Patients Management" :
             this.activeSection === "appointments" ? "Appointments Management" :
             "Reports & Exports";
    },
    headerSubtitle() {
      return this.activeSection === "dashboard" ? "Analytics & KPIs" : "Manage records and actions";
    },
    kpis() {
      return [
        { label: "Total Patients", value: this.patients.length, help: "Active / Blacklisted", icon: "bi bi-people-fill" },
        { label: "Total Doctors", value: this.doctors.length, help: "Active / Blacklisted", icon: "bi bi-person-badge" },
        { label: "Appointments (30d)", value: this.appointments.length, help: "Last 30 days", icon: "bi bi-calendar3" },
        { label: "Pending Exports", value: this.exportJobs.filter(j => j.status !== "completed").length, help: "Background jobs", icon: "bi bi-cloud-arrow-up" }
      ];
    },

    // filters
    filteredDoctors() {
      const q = (this.filters.doctor || this.globalSearch || "").toLowerCase();
      return this.doctors.filter(d => d.name.toLowerCase().includes(q) || d.specialization.toLowerCase().includes(q));
    },
    filteredSpecializations() {
      const q = (this.filters.specializations || this.globalSearch || "").toLowerCase();
      return this.specializations.filter(s => s.specialization.toLowerCase().includes(q) || s.description.toLowerCase().includes(q));
    },
    filteredPatients() {
      const q = (this.filters.patient || this.globalSearch || "").toLowerCase();
      return this.patients.filter(p => p.name.toLowerCase().includes(q) || p.pid.toLowerCase().includes(q) || (p.phone||"").includes(q));
    },
    filteredAppointments() {
      return this.appointments.filter(a => {
        if (this.filters.status && a.status !== this.filters.status) return false;
        if (this.filters.date && a.date !== this.filters.date) return false;
        const q = (this.globalSearch || "").toLowerCase();
        if (q) {
          const doc = this.getDoctorName(a.doctor_id).toLowerCase();
          const pat = this.getPatientName(a.patient_id).toLowerCase();
          if (!doc.includes(q) && !pat.includes(q) && !String(a.id).includes(q)) return false;
        }
        return true;
      }).sort((x,y) => x.date.localeCompare(y.date));
    },
    todayAppointments() {
      const today = new Date().toISOString().slice(0,10);
      return this.appointments.filter(a => a.date === today && a.status === "booked");
    },
    missedCount() {
      // demo: completed < today? treat as missed (placeholder)
      return this.appointments.filter(a => new Date(a.date) < Date.now() && a.status === "booked").length;
    },
    exportJobsForList() { return this.exportJobs; }
  },
  mounted() {
    this.renderCharts();
  },
  methods: {
    refreshData() {
      // TODO: replace with real API calls
      this.renderCharts(true);
    },

    /* Charts */
    renderCharts(force=false) {
      // appointments line (last 14 days)
      const ctx = document.getElementById("appointmentsChart");
      if (ctx) {
        const labels = [];
        const values = [];
        for (let i = 13; i >= 0; i--) {
          const d = new Date(); d.setDate(d.getDate() - i);
          const s = d.toISOString().slice(0,10);
          labels.push(s);
          values.push(this.appointments.filter(a => a.date === s).length);
        }
        if (this.charts.appointmentsChart && !force) {
          this.charts.appointmentsChart.data.labels = labels;
          this.charts.appointmentsChart.data.datasets[0].data = values;
          this.charts.appointmentsChart.update();
        } else {
          this.charts.appointmentsChart = new Chart(ctx, {
            type: "line",
            data: { labels, datasets: [{ label: "Appointments", data: values, borderColor: "rgba(15,157,88,0.95)", backgroundColor: "rgba(15,157,88,0.12)", fill: true, tension:0.25 }] },
            options: { responsive:true, plugins:{legend:{display:false}}, scales:{ y:{beginAtZero:true}}}
          });
        }
      }

      // doctors doughnut
      const ctx2 = document.getElementById("doctorsChart");
      if (ctx2) {
        const group = {};
        this.doctors.forEach(d => group[d.specialization] = (group[d.specialization]||0)+1);
        const labels2 = Object.keys(group);
        const values2 = Object.values(group);
        if (this.charts.doctorsChart && !force) {
          this.charts.doctorsChart.data.labels = labels2; this.charts.doctorsChart.data.datasets[0].data = values2; this.charts.doctorsChart.update();
        } else {
          this.charts.doctorsChart = new Chart(ctx2, {
            type: "doughnut",
            data: { labels: labels2, datasets: [{ data: values2, backgroundColor:["rgba(15,157,88,0.9)","rgba(75,192,192,0.8)","rgba(255,205,86,0.8)"] }] },
            options: { responsive:true, plugins:{legend:{position:"bottom"}} }
          });
        }
      }
    },

    /* Helpers */
    _dateOffset(days) { const d = new Date(); d.setDate(d.getDate()+days); return d.toISOString().slice(0,10); },
    getDoctorName(id) { const d = this.doctors.find(x=>x.id===id); return d?d.name:"—"; },
    getPatientName(id) { const p = this.patients.find(x=>x.id===id); return p? p.name : "—"; },

    badgeClass(status){ if(status==="booked") return "badge bg-warning text-dark"; if(status==="completed") return "badge bg-success"; if(status==="cancelled") return "badge bg-danger"; return "badge bg-secondary"; },

    /* Doctors CRUD (demo in-memory) */
    openDoctorModal(){ this.editingDoctor=null; this.doctorForm={id:null,name:'',specialization:'',phone:''}; this.showDoctorModal=true; },
    editDoctor(doc){ this.editingDoctor=doc; this.doctorForm=Object.assign({},doc); this.showDoctorModal=true; },
    closeDoctorModal(){ this.showDoctorModal=false; },
    saveDoctor(){ if(this.editingDoctor) Object.assign(this.editingDoctor,this.doctorForm); else { const id=Math.max(0,...this.doctors.map(d=>d.id))+1; this.doctors.push({id,...this.doctorForm,blacklisted:false,is_available:true}); } this.showDoctorModal=false; this.renderCharts(true); },
    toggleBlacklistDoctor(doc){ doc.blacklisted = !doc.blacklisted; },

    addAvailability(){ if(!this.availabilityDoctorId || !this.availDate || !this.availSlot) return; const doc = this.doctors.find(d=>d.id===this.availabilityDoctorId); this.sampleAvailability.push({ doctorId:this.availabilityDoctorId, doctorName: doc ? doc.name : 'Unknown', date:this.availDate, slot:this.availSlot }); this.availDate=null; this.availSlot=''; },

    /* Patients CRUD (demo in-memory) */
    openPatientModal(){ this.editingPatient=null; this.patientForm={id:null,pid:'',name:'',phone:''}; this.showPatientModal=true; },
    editPatient(p){ this.editingPatient=p; this.patientForm=Object.assign({},p); this.showPatientModal=true; },
    closePatientModal(){ this.showPatientModal=false; },
    savePatient(){ if(this.editingPatient) Object.assign(this.editingPatient,this.patientForm); else { const id=Math.max(0,...this.patients.map(p=>p.id))+1; this.patients.push({id,...this.patientForm,blacklisted:false}); } this.showPatientModal=false; },

    toggleBlacklistPatient(p){ p.blacklisted = !p.blacklisted; },

    /* Appointments */
    setAppointmentStatus(a, status){ a.status = status; this.renderCharts(true); },
    reschedulePlaceholder(a){ alert("Reschedule dialog (implement later) — appointment id: "+a.id); },
    StatusHistoryPlaceholder(a){ alert("Showing Status History (implement later) — appointment id: "+a.id); },
    /* Reports & Exports (demo) */
    exportAppointments(){ alert("Triggering export job (demo). In production this would call API/Celery job."); this.exportJobs.push({ id: Date.now(), user_id:1, job_type:'appointments_export', status:'pending', created_at: new Date().toISOString().slice(0,10) }); },
    triggerExport(){ alert("Trigger patient export (demo)."); },
    downloadReport(r){ alert("Download report demo: "+r.id); },
    viewExport(job){ alert("View export demo: "+job.id); },
    cancelExport(job){ job.status='cancelled'; },

    bulkBlacklist(){ alert("Demo bulk blacklist — implement backend endpoint for real action."); },

    getUserName(user_id){ return user_id===1 ? "Admin" : "User "+user_id; }
  }
};
</script>

<style scoped>
/* small layout & visual polish */
.card { border-radius: 8px; }
.table td, .table th { vertical-align: middle; }

/* modal backdrop simple */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 1200; }
.modal-dialog { width: 560px; max-width: 95%; }

/* chart sizing */
canvas { width: 100% !important; height: auto !important; }
</style>
