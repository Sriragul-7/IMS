import LoginPage from './pages/LoginPage.vue'
import DashboardPage from './pages/DashboardPage.vue'
import ProfilePage from './pages/ProfilePage.vue'
import AttendancePage from './pages/AttendancePage.vue'
import ResultsPage from './pages/ResultsPage.vue'
import FeesPage from './pages/FeesPage.vue'
import NoticesPage from './pages/NoticesPage.vue'
import LibraryPage from './pages/LibraryPage.vue'
import FeedbackPage from './pages/FeedbackPage.vue'
import InstructorCockpit from './pages/InstructorCockpit.vue'
import FeeManagerCockpit from './pages/FeeManagerCockpit.vue'
import FacilityManagerCockpit from './pages/FacilityManagerCockpit.vue'
import CommunicationCockpit from './pages/CommunicationCockpit.vue'
import AdmissionsCockpit from './pages/AdmissionsCockpit.vue'
import AcademicHeadCockpit from './pages/AcademicHeadCockpit.vue'
import AdminCockpit from './pages/AdminCockpit.vue'

export const routes = [
  { name: 'login', path: '/login', component: LoginPage, meta: { requiresAuth: false } },
  { name: 'dashboard', path: '/', component: DashboardPage, meta: { requiresAuth: true } },
  { name: 'profile', path: '/profile', component: ProfilePage, meta: { requiresAuth: true } },
  { name: 'attendance', path: '/attendance', component: AttendancePage, meta: { requiresAuth: true } },
  { name: 'results', path: '/results', component: ResultsPage, meta: { requiresAuth: true } },
  { name: 'fees', path: '/fees', component: FeesPage, meta: { requiresAuth: true } },
  { name: 'notices', path: '/notices', component: NoticesPage, meta: { requiresAuth: true } },
  { name: 'library', path: '/library', component: LibraryPage, meta: { requiresAuth: true } },
  { name: 'feedback', path: '/feedback', component: FeedbackPage, meta: { requiresAuth: true } },
  { name: 'instructor-cockpit', path: '/instructor', component: InstructorCockpit, meta: { requiresAuth: true } },
  { name: 'feemanager-cockpit', path: '/fees-manager', component: FeeManagerCockpit, meta: { requiresAuth: true } },
  { name: 'facilitymanager-cockpit', path: '/facility-manager', component: FacilityManagerCockpit, meta: { requiresAuth: true } },
  { name: 'communication-cockpit', path: '/communication', component: CommunicationCockpit, meta: { requiresAuth: true } },
  { name: 'admissions-cockpit', path: '/admissions', component: AdmissionsCockpit, meta: { requiresAuth: true } },
  { name: 'academichead-cockpit', path: '/academic-head', component: AcademicHeadCockpit, meta: { requiresAuth: true } },
  { name: 'admin-cockpit', path: '/admin', component: AdminCockpit, meta: { requiresAuth: true } },
]
