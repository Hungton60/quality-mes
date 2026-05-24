import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import viVN from 'antd/locale/vi_VN'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import AppLayout from './components/AppLayout'
import LoginPage from './pages/Login'
import DashboardPage from './pages/Dashboard'
import IQCPage from './pages/IQC'
import OQCPage from './pages/OQC'
import IPQCPage from './pages/IPQC'
import SPCPage from './pages/SPC'
import NCRPage from './pages/NCR'
import UsersPage from './pages/Users'
import EquipmentPage from './pages/Equipment'
import ActivityLogPage from './pages/ActivityLog'

function AppRoutes() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg text-gray-500">Dang tai...</div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" /> : <LoginPage />} />
      <Route element={user ? <AppLayout /> : <Navigate to="/login" />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/iqc" element={<IQCPage />} />
        <Route path="/oqc" element={<OQCPage />} />
        <Route path="/ipqc" element={<IPQCPage />} />
        <Route path="/spc" element={<SPCPage />} />
        <Route path="/ncr" element={<NCRPage />} />
        <Route path="/users" element={<UsersPage />} />
        <Route path="/equipment" element={<EquipmentPage />} />
        <Route path="/activity" element={<ActivityLogPage />} />
      </Route>
    </Routes>
  )
}

export default function App() {
  return (
    <ConfigProvider
      locale={viVN}
      theme={{
        token: {
          colorPrimary: '#1677ff',
          borderRadius: 6,
        },
      }}
    >
      <BrowserRouter>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </BrowserRouter>
    </ConfigProvider>
  )
}
