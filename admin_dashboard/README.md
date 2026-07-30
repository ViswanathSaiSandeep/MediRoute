# MediRoute Web Admin Dashboard

A standalone, dedicated Web Admin Dashboard application for **MediRoute** that manages all users, tracks total user counts, and provides workflow approvals for volunteers and hospitals.

Designed with MediRoute's signature **Dark Maroon & Emergency Red Theme** (`#1A0A0A` dark maroon background, `#2A1212` card surface, `#5A2D2D` subtle red borders, `#E53935` primary red accents, `#4CAF50` green approval badges, `#42A5F5` volunteer blue accents).

---

## Key Features

1. **Dashboard Overview & Metrics**:
   - **Total Users Tracking**: Real-time counter and breakdown across Bystanders, Volunteers, Hospitals, and Admins.
   - **Pending Approvals Metric**: Immediate counter for volunteer applications and hospital facility requests awaiting review.
   - **Approved Hospitals**: Total active medical intake centers.
   - **Active Emergencies**: Live emergency response tracking.
   - **Role Distribution Bars**: Interactive progress breakdown of the user base.
   - **System Audit Timeline**: Log of latest registrations and approval actions.

2. **Manage All Users**:
   - Interactive search bar (by Name, Email, Phone, UID).
   - Filter by Role (All, Bystander, Volunteer, Hospital, Admin).
   - Filter by Status (Approved, Pending, Rejected).
   - Inline actions to Approve, Reject, Revoke, or Delete accounts.

3. **Approve Volunteers**:
   - Dedicated review tab for community volunteer applicants.
   - Inspection of certified medical skills (e.g. CPR, Paramedic, AED, First Aid).
   - Contact details and registration date.
   - One-click **Approve Volunteer** (Green) and **Reject** (Red) actions.

4. **Approve Hospitals**:
   - Dedicated review tab for hospital partners.
   - Verification of Accreditation Proof Type (e.g. Certificate of Registration, Medical Practice License, Permit), Accreditation ID Number, Physical Address, and GPS Location Coordinates.
   - Handled Emergency Capability tags (Cardiac, Trauma, Burn Unit, ICU, Pediatric).
   - One-click **Approve Facility** (Green) and **Reject** (Red) actions.

5. **Live Emergency Monitor**:
   - Real-time SOS dispatch logs, assigned responders, victim locations, and completion status.

---

## How to Run

Since this is a standalone Web Application, no complex server build is required!

### Option 1: Open Directly in Browser
Double-click `admin_dashboard/index.html` or open it directly in Google Chrome, Microsoft Edge, Firefox, or Safari.

### Option 2: Run via Local HTTP Server (Optional)
If using Node.js / Python / VS Code Live Server:
```bash
# Python
python -m http.server 8080 --directory admin_dashboard

# Node npx serve
npx serve admin_dashboard
```
Then navigate to `http://localhost:8080` in your web browser.

---

## Project Structure

```
admin_dashboard/
├── index.html       # Main Web Application Page (Sidebar, Header, Metric Cards, Data Tables)
├── styles.css       # Design System & Dark Maroon Emergency Theme Styles
├── app.js           # State Manager, Interactive Filters, Approval Engine & Toasts
└── README.md        # Documentation
```
