# Cyber Automation Platform - Vue 3 SPA

A comprehensive single-page application for managing enterprise IT infrastructure cybersecurity automation, built with Vue 3, Pinia, and Tailwind CSS.

## Features

### 🎯 Core Capabilities

- **Automation Roadmap Dashboard**: Visualize automation strategy, quarterly objectives, and high-value use cases with interactive charts
- **Playbooks & Scripts Management**: Design, view, and execute Python-based playbooks for enrichment, decisioning, and remediation
- **Self-Service Portal**: CLI simulator, ChatOps interface, and quick actions for standardized security operations
- **API Integrations Hub**: Manage integrations between security tools (SIEM/SOAR, EDR, vulnerability management, cloud security)
- **CI/CD Workflows**: Build and manage deployment pipelines with environment promotion and secrets management
- **Observability & Monitoring**: Real-time metrics, logs, traces, and alerts for automation health
- **Collaboration Hub**: Technical leadership, mentoring resources, and team coordination
- **User Settings**: Profile management, preferences, and role-based access control

### 🛠️ Technical Stack

- **Vue 3** with Composition API
- **Vue Router** for navigation
- **Pinia** for state management
- **Chart.js** with vue-chartjs for data visualization
- **Tailwind CSS** for styling
- **Vuelidate** for form validation
- **Vue Toastification** for notifications
- **Axios** for simulated API calls

### 🎨 UI/UX Features

- Responsive design (mobile, tablet, desktop)
- Dark/Light mode toggle
- Search, filter, and sort on data tables
- Loading states and error handling
- Toast notifications
- Form validation
- Empty states

## Installation

### Prerequisites

- Node.js 18+ and npm

### Setup

1. Navigate to the project directory:
```bash
cd cyber-automation-spa
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
cyber-automation-spa/
├── src/
│   ├── components/          # Reusable components
│   ├── views/               # Page components
│   │   ├── Dashboard.vue
│   │   ├── Playbooks.vue
│   │   ├── PlaybookDetail.vue
│   │   ├── SelfService.vue
│   │   ├── Integrations.vue
│   │   ├── CICD.vue
│   │   ├── Observability.vue
│   │   ├── Collaboration.vue
│   │   └── Settings.vue
│   ├── stores/              # Pinia stores
│   │   ├── automation.js
│   │   ├── playbooks.js
│   │   ├── integrations.js
│   │   ├── cicd.js
│   │   ├── observability.js
│   │   └── user.js
│   ├── router/              # Vue Router configuration
│   │   └── index.js
│   ├── App.vue              # Root component
│   ├── main.js              # Application entry point
│   └── style.css            # Global styles
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies
├── vite.config.js           # Vite configuration
├── tailwind.config.js       # Tailwind CSS configuration
└── README.md                # This file
```

## Key Features by Section

### Dashboard
- Automation metrics and KPIs
- Toil reduction tracking
- Playbook success rates
- Platform coverage visualization
- Quarterly objectives with progress tracking
- Automation roadmap with filtering

### Playbooks
- Create, view, and execute playbooks
- Filter by category and status
- Real-time execution simulation
- Success rate and performance metrics
- Detailed playbook view with execution history

### Self-Service
- CLI simulator with command execution
- ChatOps interface for natural language actions
- Quick action buttons for common tasks
- Recent action history

### Integrations
- View all security tool integrations
- Test integration connectivity
- API call logs and metrics
- Integration architecture visualization
- Filter by category and status

### CI/CD
- Pipeline management and execution
- Deployment tracking with rollback capability
- Secrets management with rotation
- Pipeline configuration examples
- Environment-based filtering

### Observability
- Real-time metrics and charts
- Alert management (acknowledge/resolve)
- Log streaming with filtering
- Distributed tracing
- Service health checks
- Error budget tracking

### Collaboration
- Team task management
- Knowledge base articles
- Team member directory
- Upcoming events calendar
- Quick links to resources

### Settings
- Profile management
- Skills and expertise tracking
- Dark mode toggle
- Notification preferences
- Security settings

## Dummy Data

All data in this application is simulated using dummy JSON objects stored in Pinia stores. No backend connection is required. The application demonstrates:

- 10+ automation roadmap items
- 12+ playbooks across various categories
- 15+ integrations with major security tools
- 6+ CI/CD pipelines
- Real-time metrics and monitoring data
- Team collaboration features

## Simulated Actions

The following actions are simulated with realistic delays and responses:

- Playbook execution (2-3 seconds)
- Integration testing (1.5 seconds)
- Pipeline runs (3-5 seconds)
- CLI command execution (0.5 seconds)
- ChatOps message responses (1 second)
- Secret rotation (1.5 seconds)
- Deployment rollback (2 seconds)

## Security Tools Integrated (Simulated)

- **SIEM/SOAR**: Splunk, Cortex XSOAR
- **Endpoint/EDR**: SentinelOne, Microsoft Defender, CrowdStrike
- **Vulnerability Management**: Rapid7 InsightVM, Tenable.io
- **Email Security**: Proofpoint
- **Cloud Security**: AWS Security Hub, Palo Alto Prisma Cloud
- **Identity**: Azure AD, Okta
- **ITSM**: ServiceNow
- **ChatOps**: Slack
- **Project Management**: Jira

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This is a demonstration application for educational purposes.

## Notes

- This application uses only dummy data and does not connect to any real backend
- All API calls are simulated with setTimeout and return mock data
- Authentication and authorization are simulated (no real security implementation)
- The application demonstrates UI/UX patterns for cybersecurity automation management
