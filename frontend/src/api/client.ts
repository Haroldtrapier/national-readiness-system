const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = {
  getNationalReadiness: async () => {
    const res = await fetch(`${API_BASE}/api/v1/readiness/national`)
    return res.json()
  },
  health: async () => {
    const res = await fetch(`${API_BASE}/health`)
    return res.json()
  }
}
