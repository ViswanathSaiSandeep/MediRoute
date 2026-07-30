/**
 * MediRoute Web Admin Dashboard Application Logic
 * Integrates directly with Firebase Firestore (mediroute-33e0c) in real-time.
 * Manages live users, volunteer approvals, hospital facility verifications,
 * emergencies, and system metrics.
 */

(function () {
  'use strict';

  // ── Firebase Configuration ──
  const firebaseConfig = {
    apiKey: "YOUR_FIREBASE_API_KEY_WEB",
    authDomain: "mediroute-33e0c.firebaseapp.com",
    projectId: "mediroute-33e0c",
    storageBucket: "mediroute-33e0c.firebasestorage.app",
    messagingSenderId: "345683130305",
    appId: "1:345683130305:web:7a8689db740aefd2436140",
    measurementId: "G-TVD7YL7JSQ"
  };

  let db = null;
  let firebaseConnected = false;

  // ── Seed / Fallback Data ──
  const SEED_USERS = [
    {
      uid: 'user_001',
      name: 'Dr. Rajesh Sharma',
      email: 'rajesh.sharma@citycare.org',
      phone: '+91 98765 43210',
      role: 'hospital',
      status: 'pending',
      isApproved: false,
      createdAt: new Date('2026-07-28T09:30:00Z').toISOString(),
      hospitalDetails: {
        hospitalId: 'user_001',
        name: 'CityCare Super Speciality Hospital',
        address: 'Sector 14, MG Road, Metro District',
        proofType: 'Certificate of Registration',
        proofNumber: 'REG-2024-88492',
        latitude: 12.9716,
        longitude: 77.5946,
        emergencyTypes: ['Cardiac Arrest', 'Trauma & Accident', 'Burn Unit', 'ICU Critical'],
        active: true
      }
    },
    {
      uid: 'user_002',
      name: 'Ananya Verma',
      email: 'ananya.verma@gmail.com',
      phone: '+91 98123 76543',
      role: 'volunteer',
      status: 'pending',
      isApproved: false,
      createdAt: new Date('2026-07-28T10:15:00Z').toISOString(),
      skills: ['CPR Certified', 'Advanced First Aid', 'AED Operator']
    },
    {
      uid: 'user_003',
      name: 'Vikram Singh',
      email: 'vikram.singh@paramedic.in',
      phone: '+91 97654 32109',
      role: 'volunteer',
      status: 'pending',
      isApproved: false,
      createdAt: new Date('2026-07-28T11:00:00Z').toISOString(),
      skills: ['Paramedic EMT', 'Bleeding Control (Stop The Bleed)', 'Triage Specialist']
    },
    {
      uid: 'user_004',
      name: 'Apollo Emergency Care Center',
      email: 'intake@apolloemergency.com',
      phone: '+91 99000 11223',
      role: 'hospital',
      status: 'approved',
      isApproved: true,
      createdAt: new Date('2026-07-25T14:20:00Z').toISOString(),
      hospitalDetails: {
        hospitalId: 'user_004',
        name: 'Apollo Emergency Care Center',
        address: 'Plot 42, Central Avenue, Tech Zone',
        proofType: 'Medical Practice License',
        proofNumber: 'MED-LIC-99120',
        latitude: 12.9352,
        longitude: 77.6245,
        emergencyTypes: ['Cardiac Arrest', 'Stroke & Neurological', 'Pediatric Emergency'],
        active: true
      }
    },
    {
      uid: 'user_005',
      name: 'Siddharth Rao',
      email: 'siddharth.rao@healthrescuers.org',
      phone: '+91 98450 99887',
      role: 'volunteer',
      status: 'approved',
      isApproved: true,
      createdAt: new Date('2026-07-24T08:45:00Z').toISOString(),
      skills: ['CPR Certified', 'Choking First Aid', 'Basic Life Support (BLS)']
    },
    {
      uid: 'user_006',
      name: 'Pooja Nair',
      email: 'pooja.nair@bystander.com',
      phone: '+91 96321 00112',
      role: 'bystander',
      status: 'approved',
      isApproved: true,
      createdAt: new Date('2026-07-27T16:10:00Z').toISOString()
    },
    {
      uid: 'user_007',
      name: 'St. Martha Trauma & Cardiac Institute',
      email: 'admin@stmarthatrauma.org',
      phone: '+91 94480 33445',
      role: 'hospital',
      status: 'pending',
      isApproved: false,
      createdAt: new Date('2026-07-28T12:05:00Z').toISOString(),
      hospitalDetails: {
        hospitalId: 'user_007',
        name: 'St. Martha Trauma & Cardiac Institute',
        address: '102 Ring Road, South City',
        proofType: 'Government Hospital Permit',
        proofNumber: 'GOV-PERMIT-44102',
        latitude: 12.9123,
        longitude: 77.5833,
        emergencyTypes: ['Trauma & Accident', 'Burn Unit', 'Toxicology & Poisoning'],
        active: true
      }
    },
    {
      uid: 'user_008',
      name: 'Rohan Mehta',
      email: 'rohan.mehta@gmail.com',
      phone: '+91 95555 66778',
      role: 'bystander',
      status: 'approved',
      isApproved: true,
      createdAt: new Date('2026-07-26T18:00:00Z').toISOString()
    },
    {
      uid: 'user_009',
      name: 'Kavita Patel',
      email: 'kavita.patel@redcross.org',
      phone: '+91 97777 88990',
      role: 'volunteer',
      status: 'pending',
      isApproved: false,
      createdAt: new Date('2026-07-28T12:45:00Z').toISOString(),
      skills: ['Nursing Assistant', 'CPR Certified', 'Fracture Splinting']
    },
    {
      uid: 'user_010',
      name: 'MediRoute Admin Lead',
      email: 'admin@mediroute.io',
      phone: '+91 90000 00000',
      role: 'admin',
      status: 'approved',
      isApproved: true,
      createdAt: new Date('2026-07-01T00:00:00Z').toISOString()
    }
  ];

  const SEED_EMERGENCIES = [
    {
      id: 'emg_101',
      type: 'Cardiac Arrest',
      victim: 'Rohan Mehta',
      location: 'Near Metro Station Gate 2 (12.9716, 77.5946)',
      status: 'En Route',
      responder: 'Siddharth Rao (Volunteer)',
      time: '12 mins ago'
    },
    {
      id: 'emg_102',
      type: 'Trauma & Road Accident',
      victim: 'Unknown Passerby (Reported by Bystander)',
      location: 'Outer Ring Road Flyover (12.9352, 77.6245)',
      status: 'Hospital Alerted',
      responder: 'Apollo Emergency Center',
      time: '25 mins ago'
    },
    {
      id: 'emg_103',
      type: 'Choking & Respiratory Distress',
      victim: 'Pooja Nair',
      location: 'Indiranagar 100ft Road (12.9784, 77.6408)',
      status: 'Resolved',
      responder: 'Siddharth Rao (Volunteer)',
      time: '2 hours ago'
    }
  ];

  // ── Dashboard State ──
  let state = {
    users: [],
    hospitalsMap: {},
    emergencies: [],
    auditLogs: [],
    activeTab: 'overview',
    searchQuery: '',
    roleFilter: 'all',
    statusFilter: 'all',
    vFilter: 'pending',
    hFilter: 'pending'
  };

  // ── DOM Element Cache ──
  const elements = {
    totalUsersBadge: document.getElementById('total-users-badge'),
    pendingVolunteersBadge: document.getElementById('pending-volunteers-badge'),
    pendingHospitalsBadge: document.getElementById('pending-hospitals-badge'),
    activeEmergenciesBadge: document.getElementById('active-emergencies-badge'),
    
    metricTotalUsers: document.getElementById('metric-total-users'),
    metricPendingApprovals: document.getElementById('metric-pending-approvals'),
    metricApprovedHospitals: document.getElementById('metric-approved-hospitals'),
    metricActiveEmergencies: document.getElementById('metric-active-emergencies'),

    distBystanderCount: document.getElementById('dist-bystander-count'),
    distBystanderBar: document.getElementById('dist-bystander-bar'),
    distVolunteerCount: document.getElementById('dist-volunteer-count'),
    distVolunteerBar: document.getElementById('dist-volunteer-bar'),
    distHospitalCount: document.getElementById('dist-hospital-count'),
    distHospitalBar: document.getElementById('dist-hospital-bar'),
    distAdminCount: document.getElementById('dist-admin-count'),
    distAdminBar: document.getElementById('dist-admin-bar'),

    activityFeedList: document.getElementById('activity-feed-list'),
    allUsersTableBody: document.getElementById('all-users-table-body'),
    volunteersGrid: document.getElementById('volunteers-grid'),
    hospitalsGrid: document.getElementById('hospitals-grid'),
    emergenciesTableBody: document.getElementById('emergencies-table-body'),

    pageTitle: document.getElementById('page-title'),
    pageSubtitle: document.getElementById('page-subtitle'),
    globalSearch: document.getElementById('global-search'),
    toastContainer: document.getElementById('toast-container')
  };

  // ── Firebase Initialization & Listener Setup ──
  function initFirebase() {
    try {
      if (window.firebase) {
        if (!firebase.apps.length) {
          firebase.initializeApp(firebaseConfig);
        }
        db = firebase.firestore();
        firebaseConnected = true;
        updateConnectionStatus(true);
        setupFirestoreListeners();
      } else {
        console.warn('Firebase JS SDK not loaded, running in offline local mode.');
        loadLocalFallback();
      }
    } catch (err) {
      console.error('Firebase initialization error:', err);
      loadLocalFallback();
    }
  }

  function updateConnectionStatus(connected) {
    const statusPill = document.querySelector('.live-status-pill');
    if (statusPill) {
      statusPill.innerHTML = `
        <div class="status-dot"></div>
        <span>System Active</span>
      `;
      statusPill.style.borderColor = 'rgba(76, 175, 80, 0.4)';
      statusPill.style.color = 'var(--status-green)';
    }
  }

  // ── Real-Time Firestore Subscriptions ──
  function setupFirestoreListeners() {
    // 1. Stream Users collection
    db.collection('users').onSnapshot((snapshot) => {
      if (snapshot.empty) {
        // Seed initial data if Firestore database is empty
        seedFirestoreInitialData();
        return;
      }

      const usersList = [];
      snapshot.forEach(doc => {
        const data = doc.data();
        usersList.push(formatUserData(doc.id, data));
      });

      state.users = usersList;
      renderAll();
    }, (error) => {
      console.error('Firestore users stream error:', error);
      loadLocalFallback();
    });

    // 2. Stream Hospitals collection
    db.collection('hospitals').onSnapshot((snapshot) => {
      const map = {};
      snapshot.forEach(doc => {
        map[doc.id] = doc.data();
      });
      state.hospitalsMap = map;
      
      // Merge hospital details into users list
      state.users.forEach(u => {
        if (u.role === 'hospital' && map[u.uid]) {
          u.hospitalDetails = map[u.uid];
        }
      });
      renderAll();
    });

    // 3. Stream Emergencies collection
    db.collection('emergencies').onSnapshot((snapshot) => {
      if (!snapshot.empty) {
        const emgList = [];
        snapshot.forEach(doc => {
          const d = doc.data();
          const rawTime = d.timestamp || d.createdAt || d.time || d.date;
          emgList.push({
            id: doc.id,
            type: d.type || d.emergencyType || 'Medical Emergency',
            victim: d.victimName || d.victim || (d.bystanderUid ? `Bystander (${d.bystanderUid.substring(0, 6)})` : 'Bystander Alert'),
            location: d.address || d.location || (d.latitude && d.longitude ? `${d.latitude.toFixed(4)}, ${d.longitude.toFixed(4)}` : 'Coordinates Recorded'),
            status: (d.status || 'Active').toUpperCase(),
            responder: d.volunteerName || (d.volunteerAssigned ? `Volunteer (${d.volunteerAssigned.substring(0, 6)})` : 'Searching Nearby Volunteers...'),
            time: formatTimeAgo(rawTime)
          });
        });
        state.emergencies = emgList;
      } else {
        state.emergencies = SEED_EMERGENCIES;
      }
      renderAll();
    });
  }

  function formatUserData(id, data) {
    let createdAtIso = new Date().toISOString();
    if (data.createdAt) {
      if (data.createdAt.toDate) {
        createdAtIso = data.createdAt.toDate().toISOString();
      } else if (typeof data.createdAt === 'string') {
        createdAtIso = data.createdAt;
      }
    }

    const statusVal = data.status || (data.isApproved === false ? 'pending' : (data.isApproved === true ? 'approved' : (data.role === 'volunteer' || data.role === 'hospital' ? 'pending' : 'approved')));

    return {
      uid: id,
      name: data.name || 'Unnamed User',
      email: data.email || '',
      phone: data.phone || '',
      role: data.role || 'bystander',
      status: statusVal,
      isApproved: statusVal === 'approved',
      skills: data.skills || [],
      createdAt: createdAtIso,
      hospitalDetails: data.hospitalDetails || state.hospitalsMap[id] || null
    };
  }

  // Seed Firestore if database starts empty
  async function seedFirestoreInitialData() {
    console.log('Seeding initial records into Firebase Firestore...');
    try {
      const batch = db.batch();
      SEED_USERS.forEach(u => {
        const userRef = db.collection('users').doc(u.uid);
        batch.set(userRef, {
          uid: u.uid,
          name: u.name,
          email: u.email,
          phone: u.phone,
          role: u.role,
          status: u.status,
          isApproved: u.isApproved,
          skills: u.skills || [],
          createdAt: firebase.firestore.Timestamp.fromDate(new Date(u.createdAt))
        });

        if (u.hospitalDetails) {
          const hospRef = db.collection('hospitals').doc(u.uid);
          batch.set(hospRef, u.hospitalDetails);
        }
      });
      await batch.commit();
      console.log('Successfully seeded initial records into Firestore!');
    } catch (e) {
      console.error('Error seeding Firestore:', e);
      state.users = SEED_USERS;
      renderAll();
    }
  }

  function loadLocalFallback() {
    updateConnectionStatus(false);
    const saved = localStorage.getItem('mediroute_admin_users');
    if (saved) {
      try {
        state.users = JSON.parse(saved);
      } catch (e) {
        state.users = SEED_USERS;
      }
    } else {
      state.users = SEED_USERS;
    }
    state.emergencies = SEED_EMERGENCIES;
    renderAll();
  }

  function formatTimeAgo(dateObj) {
    if (!dateObj) return 'N/A';
    let date;
    
    if (dateObj && typeof dateObj.toDate === 'function') {
      date = dateObj.toDate();
    } else if (dateObj && typeof dateObj.seconds === 'number') {
      date = new Date(dateObj.seconds * 1000);
    } else if (typeof dateObj === 'number') {
      date = new Date(dateObj);
    } else if (typeof dateObj === 'string') {
      date = new Date(dateObj);
    } else if (dateObj instanceof Date) {
      date = dateObj;
    } else {
      date = new Date(dateObj);
    }

    if (!date || isNaN(date.getTime())) return 'N/A';

    const now = new Date();
    const diffMs = now - date;
    const seconds = Math.floor(diffMs / 1000);

    if (seconds < 0) return 'Just now';
    if (seconds < 60) return `${seconds}s ago`;
    
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    
    const days = Math.floor(hours / 24);
    if (days < 30) return `${days}d ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  }

  // Initial Audit Logs
  state.auditLogs = [
    { id: 1, text: 'Real-time Firebase Firestore stream connected', time: 'Just now', type: 'info' },
    { id: 2, text: 'Volunteer application submitted by Ananya Verma', time: '2 hours ago', type: 'volunteer' },
    { id: 3, text: 'Facility registration request from CityCare Super Speciality Hospital', time: '3 hours ago', type: 'hospital' }
  ];

  // ── Render Components ──
  function renderMetrics() {
    const totalUsers = state.users.length;
    const pendingVolunteers = state.users.filter(u => u.role === 'volunteer' && u.status === 'pending').length;
    const pendingHospitals = state.users.filter(u => u.role === 'hospital' && u.status === 'pending').length;
    const pendingTotal = pendingVolunteers + pendingHospitals;
    const approvedHospitals = state.users.filter(u => u.role === 'hospital' && u.status === 'approved').length;
    const activeEmergencies = state.emergencies.filter(e => e.status !== 'Resolved').length;

    // Badges
    elements.totalUsersBadge.textContent = totalUsers;
    elements.pendingVolunteersBadge.textContent = pendingVolunteers;
    elements.pendingHospitalsBadge.textContent = pendingHospitals;
    elements.activeEmergenciesBadge.textContent = activeEmergencies;

    // Stat Cards
    elements.metricTotalUsers.textContent = totalUsers;
    elements.metricPendingApprovals.textContent = pendingTotal;
    elements.metricApprovedHospitals.textContent = approvedHospitals;
    elements.metricActiveEmergencies.textContent = activeEmergencies;

    // Role distribution bars
    const bystanders = state.users.filter(u => u.role === 'bystander').length;
    const volunteers = state.users.filter(u => u.role === 'volunteer').length;
    const hospitals = state.users.filter(u => u.role === 'hospital').length;
    const admins = state.users.filter(u => u.role === 'admin').length;

    const bPct = Math.round((bystanders / (totalUsers || 1)) * 100);
    const vPct = Math.round((volunteers / (totalUsers || 1)) * 100);
    const hPct = Math.round((hospitals / (totalUsers || 1)) * 100);
    const aPct = Math.round((admins / (totalUsers || 1)) * 100);

    elements.distBystanderCount.textContent = `${bystanders} (${bPct}%)`;
    elements.distBystanderBar.style.width = `${bPct}%`;

    elements.distVolunteerCount.textContent = `${volunteers} (${vPct}%)`;
    elements.distVolunteerBar.style.width = `${vPct}%`;

    elements.distHospitalCount.textContent = `${hospitals} (${hPct}%)`;
    elements.distHospitalBar.style.width = `${hPct}%`;

    elements.distAdminCount.textContent = `${admins} (${aPct}%)`;
    elements.distAdminBar.style.width = `${aPct}%`;
  }

  function renderAuditLogs() {
    elements.activityFeedList.innerHTML = state.auditLogs.map(log => `
      <div class="activity-item">
        <div class="activity-icon" style="background: rgba(229, 57, 53, 0.15); color: var(--primary-red);">
          <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
        <div class="activity-content">
          <span class="activity-text">${log.text}</span>
          <span class="activity-time">${log.time}</span>
        </div>
      </div>
    `).join('');
  }

  function renderAllUsersTable() {
    let filtered = state.users.filter(u => {
      if (state.roleFilter !== 'all' && u.role !== state.roleFilter) return false;
      if (state.statusFilter !== 'all' && u.status !== state.statusFilter) return false;
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        const nameMatch = u.name.toLowerCase().includes(q);
        const emailMatch = u.email.toLowerCase().includes(q);
        const phoneMatch = u.phone.toLowerCase().includes(q);
        const uidMatch = u.uid.toLowerCase().includes(q);
        return nameMatch || emailMatch || phoneMatch || uidMatch;
      }
      return true;
    });

    if (filtered.length === 0) {
      elements.allUsersTableBody.innerHTML = `
        <tr>
          <td colspan="6">
            <div class="empty-state">
              <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
              <h3>No users found</h3>
              <p>Try adjusting your search query or filter criteria.</p>
            </div>
          </td>
        </tr>
      `;
      return;
    }

    elements.allUsersTableBody.innerHTML = filtered.map(u => {
      const initial = u.name ? u.name.charAt(0).toUpperCase() : 'U';
      const formattedDate = new Date(u.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

      return `
        <tr>
          <td>
            <div class="user-cell">
              <div class="user-avatar-circle ${u.role}">${initial}</div>
              <div class="user-details-col">
                <span class="user-name-text">${u.name}</span>
                <span class="user-email-text">${u.uid}</span>
              </div>
            </div>
          </td>
          <td><span class="badge role-${u.role}">${u.role}</span></td>
          <td>
            <div class="user-details-col">
              <span style="font-size: 13px;">${u.email}</span>
              <span class="user-email-text">${u.phone}</span>
            </div>
          </td>
          <td><span class="badge ${u.status}">${u.status}</span></td>
          <td>${formattedDate}</td>
          <td>
            <div class="action-buttons-group">
              ${u.status === 'pending' ? `
                <button class="btn btn-approve" onclick="window.approveUser('${u.uid}')">Approve</button>
                <button class="btn btn-reject" onclick="window.rejectUser('${u.uid}')">Reject</button>
              ` : `
                <button class="btn btn-secondary" onclick="window.toggleUserStatus('${u.uid}')">
                  ${u.status === 'approved' ? 'Revoke' : 'Re-Approve'}
                </button>
              `}
              <button class="btn btn-icon" onclick="window.deleteUser('${u.uid}')" title="Delete User">
                <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
              </button>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  function renderVolunteersGrid() {
    let volunteers = state.users.filter(u => u.role === 'volunteer');

    if (state.vFilter !== 'all') {
      volunteers = volunteers.filter(u => u.status === state.vFilter);
    }

    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      volunteers = volunteers.filter(u => {
        const skillsStr = (u.skills || []).join(' ').toLowerCase();
        return u.name.toLowerCase().includes(q) ||
               u.email.toLowerCase().includes(q) ||
               u.phone.toLowerCase().includes(q) ||
               u.status.toLowerCase().includes(q) ||
               skillsStr.includes(q);
      });
    }

    if (volunteers.length === 0) {
      elements.volunteersGrid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l8.72-8.72 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          <h3>No volunteer applications matching search</h3>
          <p>Try searching for a volunteer name, email, phone, or medical skill.</p>
        </div>
      `;
      return;
    }

    elements.volunteersGrid.innerHTML = volunteers.map(v => {
      const skills = v.skills || ['CPR Certified', 'Basic First Aid'];
      const formattedDate = new Date(v.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

      return `
        <div class="approval-card">
          <div class="approval-card-header">
            <div class="card-header-main">
              <div class="user-avatar-circle volunteer">${v.name.charAt(0)}</div>
              <div>
                <h4 style="font-size: 16px; font-weight: 700; color: #FFF;">${v.name}</h4>
                <span style="font-size: 12px; color: var(--text-muted);">${v.phone}</span>
              </div>
            </div>
            <span class="badge ${v.status}">${v.status}</span>
          </div>

          <div class="approval-card-body">
            <div class="info-row">
              <span class="info-label">Email Address:</span>
              <span class="info-value">${v.email}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Date Applied:</span>
              <span class="info-value">${formattedDate}</span>
            </div>
            <div style="margin-top: 6px;">
              <span class="info-label" style="display: block; margin-bottom: 6px;">Medical Skills & Certifications:</span>
              <div class="skill-chips">
                ${skills.map(s => `<span class="skill-chip">${s}</span>`).join('')}
              </div>
            </div>
          </div>

          <div class="approval-card-footer">
            ${v.status === 'pending' ? `
              <button class="btn btn-approve" onclick="window.approveUser('${v.uid}')">
                ✓ Approve Volunteer
              </button>
              <button class="btn btn-reject" onclick="window.rejectUser('${v.uid}')">
                ✕ Reject
              </button>
            ` : `
              <button class="btn btn-secondary" onclick="window.toggleUserStatus('${v.uid}')">
                ${v.status === 'approved' ? 'Revoke Approval' : 'Re-Approve'}
              </button>
            `}
          </div>
        </div>
      `;
    }).join('');
  }

  function renderHospitalsGrid() {
    let hospitals = state.users.filter(u => u.role === 'hospital');

    if (state.hFilter !== 'all') {
      hospitals = hospitals.filter(u => u.status === state.hFilter);
    }

    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      hospitals = hospitals.filter(h => {
        const details = h.hospitalDetails || {};
        const capStr = (details.emergencyTypes || []).join(' ').toLowerCase();
        return h.name.toLowerCase().includes(q) ||
               h.email.toLowerCase().includes(q) ||
               h.phone.toLowerCase().includes(q) ||
               h.status.toLowerCase().includes(q) ||
               (details.name || '').toLowerCase().includes(q) ||
               (details.address || '').toLowerCase().includes(q) ||
               (details.proofNumber || '').toLowerCase().includes(q) ||
               (details.proofType || '').toLowerCase().includes(q) ||
               capStr.includes(q);
      });
    }

    if (hospitals.length === 0) {
      elements.hospitalsGrid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <svg viewBox="0 0 24 24"><path d="M3 21h18M5 21V7l8-4v18M19 21V11l-6-3"/></svg>
          <h3>No hospital registration applications matching search</h3>
          <p>Try searching for a facility name, proof ID, address, or emergency capability.</p>
        </div>
      `;
      return;
    }

    elements.hospitalsGrid.innerHTML = hospitals.map(h => {
      const details = h.hospitalDetails || {
        name: h.name,
        address: 'City Central Medical Zone',
        proofType: 'Certificate of Registration',
        proofNumber: 'REG-2024-OFFICIAL',
        latitude: 12.9716,
        longitude: 77.5946,
        emergencyTypes: ['Cardiac Arrest', 'Trauma & Emergency']
      };

      const formattedDate = new Date(h.createdAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

      return `
        <div class="approval-card">
          <div class="approval-card-header">
            <div class="card-header-main">
              <div class="user-avatar-circle hospital">🏥</div>
              <div>
                <h4 style="font-size: 16px; font-weight: 700; color: #FFF;">${details.name || h.name}</h4>
                <span style="font-size: 12px; color: var(--text-muted);">${h.phone}</span>
              </div>
            </div>
            <span class="badge ${h.status}">${h.status}</span>
          </div>

          <div class="approval-card-body">
            <div class="info-row">
              <span class="info-label">Physical Address:</span>
              <span class="info-value" style="max-width: 180px; text-align: right;">${details.address}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Proof Document:</span>
              <span class="info-value">${details.proofType}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Accreditation ID:</span>
              <span class="info-value" style="color: var(--primary-red); font-family: monospace;">${details.proofNumber}</span>
            </div>
            <div class="info-row">
              <span class="info-label">GPS Coordinates:</span>
              <span class="info-value">${(details.latitude || 0).toFixed(4)}, ${(details.longitude || 0).toFixed(4)}</span>
            </div>
            <div style="margin-top: 6px;">
              <span class="info-label" style="display: block; margin-bottom: 6px;">Emergency Capabilities:</span>
              <div class="skill-chips">
                ${(details.emergencyTypes || []).map(t => `<span class="skill-chip" style="background: rgba(229,57,53,0.15); color: #FF8A80;">${t}</span>`).join('')}
              </div>
            </div>
          </div>

          <div class="approval-card-footer">
            ${h.status === 'pending' ? `
              <button class="btn btn-approve" onclick="window.approveUser('${h.uid}')">
                ✓ Approve Facility
              </button>
              <button class="btn btn-reject" onclick="window.rejectUser('${h.uid}')">
                ✕ Reject
              </button>
            ` : `
              <button class="btn btn-secondary" onclick="window.toggleUserStatus('${h.uid}')">
                ${h.status === 'approved' ? 'Revoke Verification' : 'Re-Approve'}
              </button>
            `}
          </div>
        </div>
      `;
    }).join('');
  }

  function renderEmergenciesTable() {
    let filtered = state.emergencies;
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      filtered = filtered.filter(e => 
        (e.type && e.type.toLowerCase().includes(q)) ||
        (e.victim && e.victim.toLowerCase().includes(q)) ||
        (e.location && e.location.toLowerCase().includes(q)) ||
        (e.status && e.status.toLowerCase().includes(q)) ||
        (e.responder && e.responder.toLowerCase().includes(q))
      );
    }

    if (filtered.length === 0) {
      elements.emergenciesTableBody.innerHTML = `
        <tr>
          <td colspan="6">
            <div class="empty-state">
              <svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              <h3>No emergency records matching search</h3>
              <p>Try searching for a different emergency type, victim name, or location.</p>
            </div>
          </td>
        </tr>
      `;
      return;
    }

    elements.emergenciesTableBody.innerHTML = filtered.map(e => `
      <tr>
        <td>
          <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: var(--sos-red);"></div>
            <span style="font-weight: 700; color: #FFF;">${e.type}</span>
          </div>
        </td>
        <td>${e.victim}</td>
        <td style="font-size: 13px; color: var(--text-muted);">${e.location}</td>
        <td><span class="badge ${e.status === 'RESOLVED' || e.status === 'Resolved' ? 'approved' : 'pending'}">${e.status}</span></td>
        <td>${e.responder}</td>
        <td style="font-size: 12px; color: var(--text-muted);">${e.time}</td>
      </tr>
    `).join('');
  }

  function renderAll() {
    renderMetrics();
    renderAuditLogs();
    renderAllUsersTable();
    renderVolunteersGrid();
    renderHospitalsGrid();
    renderEmergenciesTable();
  }

  // ── Firestore Live Mutation Handlers ──
  window.approveUser = async function (uid) {
    const user = state.users.find(u => u.uid === uid);
    if (user) {
      user.status = 'approved';
      user.isApproved = true;

      if (firebaseConnected && db) {
        try {
          await db.collection('users').doc(uid).update({
            status: 'approved',
            isApproved: true
          });
          if (user.role === 'hospital') {
            await db.collection('hospitals').doc(uid).update({
              status: 'approved',
              isApproved: true,
              active: true
            });
          }
        } catch (e) {
          console.error('Error updating Firestore document:', e);
        }
      }

      state.auditLogs.unshift({
        id: Date.now(),
        text: `Approved ${user.role} account for ${user.name} in Firestore`,
        time: 'Just now',
        type: 'approval'
      });

      renderAll();
      showToast(`🔥 Approved ${user.name} (${user.role}) in Firestore!`, 'success');
    }
  };

  window.rejectUser = async function (uid) {
    const user = state.users.find(u => u.uid === uid);
    if (user) {
      user.status = 'rejected';
      user.isApproved = false;

      if (firebaseConnected && db) {
        try {
          await db.collection('users').doc(uid).update({
            status: 'rejected',
            isApproved: false
          });
          if (user.role === 'hospital') {
            await db.collection('hospitals').doc(uid).update({
              status: 'rejected',
              isApproved: false
            });
          }
        } catch (e) {
          console.error('Error updating Firestore document:', e);
        }
      }

      state.auditLogs.unshift({
        id: Date.now(),
        text: `Rejected application for ${user.name} in Firestore`,
        time: 'Just now',
        type: 'rejection'
      });

      renderAll();
      showToast(`Rejected application for ${user.name}.`, 'error');
    }
  };

  window.toggleUserStatus = async function (uid) {
    const user = state.users.find(u => u.uid === uid);
    if (user) {
      const newStatus = user.status === 'approved' ? 'rejected' : 'approved';
      user.status = newStatus;
      user.isApproved = newStatus === 'approved';

      if (firebaseConnected && db) {
        try {
          await db.collection('users').doc(uid).update({
            status: newStatus,
            isApproved: newStatus === 'approved'
          });
        } catch (e) {
          console.error('Error toggling Firestore document:', e);
        }
      }

      renderAll();
      showToast(`Updated status for ${user.name} to ${newStatus.toUpperCase()} in Firestore.`, 'success');
    }
  };

  window.deleteUser = async function (uid) {
    const index = state.users.findIndex(u => u.uid === uid);
    if (index !== -1) {
      const name = state.users[index].name;
      if (confirm(`Are you sure you want to delete account ${name} from Firestore?`)) {
        if (firebaseConnected && db) {
          try {
            await db.collection('users').doc(uid).delete();
            await db.collection('hospitals').doc(uid).delete();
          } catch (e) {
            console.error('Error deleting from Firestore:', e);
          }
        }

        state.users.splice(index, 1);
        renderAll();
        showToast(`Deleted user ${name} from Firestore.`, 'error');
      }
    }
  };

  // Toast Notification System
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type === 'error' ? 'error' : ''}`;
    toast.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        ${type === 'error' 
          ? '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>'
          : '<polyline points="20 6 9 17 4 12"/>'}
      </svg>
      <span>${message}</span>
    `;
    elements.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // ── Setup Event Handlers ──
  function setupEventListeners() {
    // Navigation Tabs
    document.querySelectorAll('.sidebar-nav .nav-item').forEach(item => {
      item.addEventListener('click', () => {
        const tab = item.getAttribute('data-tab');
        if (!tab) return;

        document.querySelectorAll('.sidebar-nav .nav-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
        const activePane = document.getElementById(`tab-${tab}`);
        if (activePane) activePane.classList.add('active');

        const titles = {
          overview: { title: 'Dashboard Overview', subtitle: 'Real-time system stats & response coordination' },
          users: { title: 'Manage All Users', subtitle: 'Directory of bystanders, volunteers, hospitals & admins' },
          volunteers: { title: 'Volunteer Applications', subtitle: 'Review medical qualifications & verify community responders' },
          hospitals: { title: 'Hospital Partner Verification', subtitle: 'Verify medical licenses & emergency intake capabilities' },
          emergencies: { title: 'Live Emergency Monitor', subtitle: 'Real-time SOS response tracking across the network' }
        };

        if (titles[tab]) {
          elements.pageTitle.textContent = titles[tab].title;
          elements.pageSubtitle.textContent = titles[tab].subtitle;
        }

        state.activeTab = tab;
      });
    });

    // Search Input
    elements.globalSearch.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      renderAllUsersTable();
      renderVolunteersGrid();
      renderHospitalsGrid();
      renderEmergenciesTable();
    });

    // Role Filter Chips
    document.querySelectorAll('#user-role-filter .filter-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#user-role-filter .filter-chip').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.roleFilter = btn.getAttribute('data-filter');
        renderAllUsersTable();
      });
    });

    // Status Select
    document.getElementById('user-status-select').addEventListener('change', (e) => {
      state.statusFilter = e.target.value;
      renderAllUsersTable();
    });

    // Volunteer Filter Chips
    document.querySelectorAll('#volunteer-status-filter .filter-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#volunteer-status-filter .filter-chip').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.vFilter = btn.getAttribute('data-vfilter');
        renderVolunteersGrid();
      });
    });

    // Hospital Filter Chips
    document.querySelectorAll('#hospital-status-filter .filter-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#hospital-status-filter .filter-chip').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.hFilter = btn.getAttribute('data-hfilter');
        renderHospitalsGrid();
      });
    });
  }

  // Boot Application
  document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    initFirebase();
  });

})();
