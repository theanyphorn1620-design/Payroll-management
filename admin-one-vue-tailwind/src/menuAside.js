import {
  mdiAccountCircle,
  mdiMonitor,
  mdiAlertCircle,
  mdiAccountMultiple,
  mdiCalendarCheck,
  mdiCurrencyUsd,
  mdiFileDocument,
  mdiChartBar,
  mdiCalendarStar,
  mdiLogout,
} from '@mdi/js'

export const menuAsideMain = [
  {
    to: '/dashboard',
    icon: mdiMonitor,
    label: 'Dashboard',
    adminOnly: true,
  },
  {
    to: '/my-portal',
    icon: mdiMonitor,
    label: 'My Portal',
    employeeOnly: true,
  },
  {
    to: '/employees',
    label: 'Employees',
    icon: mdiAccountMultiple,
    adminOnly: true,
  },
  {
    to: '/attendance',
    label: 'Attendance',
    icon: mdiCalendarCheck,
    adminOnly: true,
  },
  {
    to: '/salary-structures',
    label: 'Salary Structures',
    icon: mdiCurrencyUsd,
    adminOnly: true,
  },
  {
    to: '/payslips',
    label: 'Payslips',
    icon: mdiFileDocument,
    adminOnly: true,
  },
  {
    to: '/reports',
    label: 'Reports',
    icon: mdiChartBar,
    adminOnly: true,
  },
  {
    to: '/holidays',
    label: 'Holidays',
    icon: mdiCalendarStar,
    adminOnly: true,
  },
  {
    to: '/profile',
    label: 'Profile',
    icon: mdiAccountCircle,
  },
  {
    to: '/error',
    label: 'Error',
    icon: mdiAlertCircle,
  },
]

export const menuAsideBottom = [
  {
    label: 'Logout',
    icon: mdiLogout,
    color: 'info',
    isLogout: true,
  },
]
