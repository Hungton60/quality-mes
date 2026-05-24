import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

const TOKEN_KEY = 'quality_mes_token'
const USER_KEY = 'quality_mes_user'

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function removeToken() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export function setUser(user: object) {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function getUser(): object | null {
  const data = localStorage.getItem(USER_KEY)
  return data ? JSON.parse(data) : null
}

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      removeToken()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  full_name: string
  role: string
}

export interface UserInfo {
  id: number
  username: string
  email: string
  full_name: string
  role: string
  is_active: boolean
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

export async function login(data: LoginData): Promise<LoginResponse> {
  const res = await api.post<LoginResponse>('/auth/login', data)
  return res.data
}

export async function register(data: RegisterData): Promise<UserInfo> {
  const res = await api.post<UserInfo>('/auth/register', data)
  return res.data
}

export async function getMe(): Promise<UserInfo> {
  const res = await api.get<UserInfo>('/auth/me')
  return res.data
}

export default api
