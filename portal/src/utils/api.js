const API_BASE = '/api/method/institution_erp.api'

export function getSessionUser() {
  return JSON.parse(localStorage.getItem('institution_portal_user') || 'null')
}

export function setSessionUser(data) {
  localStorage.setItem('institution_portal_user', JSON.stringify(data))
}

export function clearSessionUser() {
  localStorage.removeItem('institution_portal_user')
}

export async function callAPI(method, params = {}) {
  const cmd = `institution_erp.api.${method}`
  const url = `/api/method/${cmd}`
  const csrfToken = window.csrf_token || window.frappe?.csrf_token || ''

  const body = new URLSearchParams()
  body.append('cmd', cmd)
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) body.append(k, v)
  }

  const resp = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-Frappe-CSRF-Token': csrfToken,
    },
    body: body.toString(),
    credentials: 'same-origin',
  })

  if (!resp.ok) {
    const text = await resp.text()
    throw new Error(`API error ${resp.status}: ${text}`)
  }

  const data = await resp.json()
  if (data._server_messages) {
    try {
      const msgs = JSON.parse(data._server_messages)
      if (msgs.length) {
        const msg = typeof msgs[0] === 'string' ? JSON.parse(msgs[0]).message || msgs[0] : msgs[0]
        throw new Error(msg)
      }
    } catch (e) {
      if (e.message && !e.message.includes('JSON')) throw e
    }
  }
  if (data.exc_type) {
    throw new Error(data.message || data.exc_type)
  }
  return data.message
}

export async function login(email, password) {
  const resp = await fetch('/api/method/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ usr: email, pwd: password }).toString(),
    credentials: 'same-origin',
  })
  const data = await resp.json()
  if (data.message === 'Logged In' || data.home_page) {
    // Success - desk user or website user
  } else {
    throw new Error(data.message || 'Login failed')
  }
  // Fetch CSRF token after login
  try {
    const cs = await fetch('/api/method/frappe.utils.csrf.get_csrf_token', { credentials: 'same-origin' })
    const csData = await cs.json()
    if (csData.message) window.csrf_token = csData.message
  } catch (e) { /* ignore */ }
  return data
}

export async function logout() {
  await fetch('/api/method/logout', { credentials: 'same-origin' })
  clearSessionUser()
}
