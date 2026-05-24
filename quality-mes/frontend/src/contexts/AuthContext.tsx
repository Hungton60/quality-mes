import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import { login as apiLogin, register as apiRegister, getMe, setToken, removeToken, setUser, getToken, type LoginData, type RegisterData, type UserInfo } from '../services/api'

interface AuthContextType {
  user: UserInfo | null
  loading: boolean
  login: (data: LoginData) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  isAdmin: boolean
  isQCManager: boolean
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setStateUser] = useState<UserInfo | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    if (token) {
      getMe()
        .then((userData) => setStateUser(userData))
        .catch(() => removeToken())
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const handleLogin = async (data: LoginData) => {
    const res = await apiLogin(data)
    setToken(res.access_token)
    setUser(res.user)
    setStateUser(res.user)
  }

  const handleRegister = async (data: RegisterData) => {
    await apiRegister(data)
  }

  const handleLogout = () => {
    removeToken()
    setStateUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login: handleLogin,
        register: handleRegister,
        logout: handleLogout,
        isAdmin: user?.role === 'admin',
        isQCManager: user?.role === 'admin' || user?.role === 'qc_manager',
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
