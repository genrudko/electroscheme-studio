import type { Connection, Project, SchemeSymbol, SymbolLibrary } from './types'

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

export async function fetchSymbolLibrary(): Promise<SymbolLibrary> {
  const res = await fetch(`${API_BASE}/symbols?t=${Date.now()}`)
  if (!res.ok) throw new Error(`GET /api/symbols failed: ${res.status}`)
  return res.json()
}

export async function addSymbol(symbol: SchemeSymbol): Promise<void> {
  const res = await fetch(`${API_BASE}/project/symbols`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(symbol),
  })
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`POST /api/project/symbols failed: ${res.status} ${detail}`)
  }
}

export async function removeSymbol(symbolId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/project/symbols/${encodeURIComponent(symbolId)}`, {
    method: 'DELETE',
  })
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`DELETE /api/project/symbols/${symbolId} failed: ${res.status} ${detail}`)
  }
}

export async function addConnection(connection: Connection): Promise<void> {
  const res = await fetch(`${API_BASE}/project/connections`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(connection),
  })
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`POST /api/project/connections failed: ${res.status} ${detail}`)
  }
}

export async function updateConnection(connection: Connection): Promise<void> {
  const res = await fetch(
    `${API_BASE}/project/connections/${encodeURIComponent(connection.id)}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(connection),
    },
  )
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`PUT /api/project/connections/${connection.id} failed: ${res.status} ${detail}`)
  }
}

export async function removeConnection(connectionId: string): Promise<void> {
  const res = await fetch(
    `${API_BASE}/project/connections/${encodeURIComponent(connectionId)}`,
    { method: 'DELETE' },
  )
  if (!res.ok) {
    const detail = await res.text()
    throw new Error(`DELETE /api/project/connections/${connectionId} failed: ${res.status} ${detail}`)
  }
}
