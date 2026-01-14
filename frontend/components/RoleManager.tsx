"use client";

import { useState, useEffect } from 'react';
import { fetchRoles, createRole } from '../lib/api';

interface Role {
    id: number;
    name: string;
    description: string;
}

interface RoleManagerProps {
    selectedRoleId: number | null;
    onRoleSelect: (roleId: number) => void;
}

export default function RoleManager({ selectedRoleId, onRoleSelect }: RoleManagerProps) {
    const [roles, setRoles] = useState<Role[]>([]);
    const [loading, setLoading] = useState(true);
    const [isCreating, setIsCreating] = useState(false);
    const [newName, setNewName] = useState('');
    const [newDesc, setNewDesc] = useState('');

    useEffect(() => {
        loadRoles();
    }, []);

    async function loadRoles() {
        try {
            const data = await fetchRoles();
            setRoles(data);
            if (data.length > 0 && !selectedRoleId) {
                onRoleSelect(data[0].id);
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    }

    async function handleCreate(e: React.FormEvent) {
        e.preventDefault();
        if (!newName || !newDesc) return;
        try {
            const newRole = await createRole(newName, newDesc);
            setRoles([...roles, newRole]);
            onRoleSelect(newRole.id);
            setIsCreating(false);
            setNewName('');
            setNewDesc('');
        } catch (error) {
            alert('Error creating role');
        }
    }

    if (loading) return <div className="text-gray-500 text-sm">Loading roles...</div>;

    return (
        <div className="mb-8 p-6 bg-white rounded-xl shadow-lg border border-gray-100">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-800">1. Select Position</h2>
                <button
                    onClick={() => setIsCreating(!isCreating)}
                    className="text-sm text-blue-600 hover:text-blue-800 font-medium"
                >
                    {isCreating ? 'Cancel' : '+ New Role'}
                </button>
            </div>

            {isCreating && (
                <form onSubmit={handleCreate} className="mb-6 bg-gray-50 p-4 rounded-lg">
                    <input
                        type="text"
                        placeholder="Role Title (e.g. Senior Data Scientist)"
                        className="w-full mb-3 p-2 border rounded"
                        value={newName}
                        onChange={e => setNewName(e.target.value)}
                    />
                    <textarea
                        placeholder="Job Description (Paste the full text here...)"
                        className="w-full mb-3 p-2 border rounded h-24"
                        value={newDesc}
                        onChange={e => setNewDesc(e.target.value)}
                    />
                    <button
                        type="submit"
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
                    >
                        Create Role & Generate AI Profile
                    </button>
                </form>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {roles.map(role => (
                    <div
                        key={role.id}
                        onClick={() => onRoleSelect(role.id)}
                        className={`cursor-pointer p-4 rounded-lg border transition-all ${selectedRoleId === role.id
                                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                                : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
                            }`}
                    >
                        <h3 className="font-semibold text-gray-900">{role.name}</h3>
                        <p className="text-gray-500 text-xs mt-1 truncate">{role.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
