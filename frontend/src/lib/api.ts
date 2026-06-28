import type { SchemeSymbol, Connection, Sheet, Project } from './types'

const API_BASE = '/api'

export async function fetchProject(): Promise<Project> {
  const res = await fetch(`${API_BASE}/project`)
  if (!res.ok) throw new Error(`GET /api/project failed: ${res.status}`)
  return res.json()
}

export async function saveProject(project: Project): Promise<void> {
  const res = await fetch(`${API_BASE}/project`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(project),
  })
  if (!res.ok) throw new Error(`PUT /api/project failed: ${res.status}`)
}
