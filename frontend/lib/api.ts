const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchRoles() {
    const res = await fetch(`${API_URL}/roles/`);
    if (!res.ok) throw new Error('Failed to fetch roles');
    return res.json();
}

export async function createRole(name: string, description: string) {
    const res = await fetch(`${API_URL}/roles/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, description }),
    });
    if (!res.ok) throw new Error('Failed to create role');
    return res.json();
}

export async function deleteRole(roleId: number) {
    const res = await fetch(`${API_URL}/roles/${roleId}`, {
        method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete role');
    return res.json();
}

export async function fetchRankings(roleId: number) {
    const res = await fetch(`${API_URL}/candidates/${roleId}`);
    if (!res.ok) throw new Error('Failed to fetch rankings');
    return res.json();
}

export async function uploadCV(roleId: number, file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`${API_URL}/candidates/${roleId}`, {
        method: 'POST',
        body: formData,
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to upload CV');
    }
    return res.json();
}
