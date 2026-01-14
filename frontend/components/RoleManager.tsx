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
    // State para selección visual robusta (evita fantasmas por duplicados)
    const [selectedIndex, setSelectedIndex] = useState<number>(0);

    useEffect(() => {
        loadRoles();
    }, []);

    async function loadRoles() {
        try {
            const data = await fetchRoles();
            setRoles(data);
            if (data.length > 0) {
                // Seleccionar índice 0 por defecto visualmente
                setSelectedIndex(0);
                // Notificar ID al padre
                if (!selectedRoleId) {
                    onRoleSelect(data[0].id);
                }
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
            const updatedRoles = [...roles, newRole];
            setRoles(updatedRoles);

            // Seleccionar el nuevo (último)
            const newIndex = updatedRoles.length - 1;
            setSelectedIndex(newIndex);
            onRoleSelect(newRole.id);

            setIsCreating(false);
            setNewName('');
            setNewDesc('');
        } catch (error) {
            alert('Error creando el perfil');
        }
    }

    if (loading) return <div className="text-gray-500 text-sm animate-pulse">Cargando perfiles...</div>;

    return (
        <div className="mb-8 p-8 bg-white rounded-2xl shadow-xl border border-gray-100 ring-1 ring-black/5 transition-all duration-300 hover:shadow-2xl">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900 tracking-tight">
                    1. Gestión de Perfiles
                </h2>
                <button
                    onClick={() => setIsCreating(!isCreating)}
                    className="text-sm font-semibold text-indigo-600 hover:text-indigo-800 transition-colors bg-indigo-50 px-4 py-2 rounded-lg hover:bg-indigo-100"
                >
                    {isCreating ? 'Cancelar' : '+ Nuevo Perfil'}
                </button>
            </div>

            {isCreating && (
                <form onSubmit={handleCreate} className="mb-8 bg-gray-50 p-6 rounded-xl border border-gray-200 shadow-inner">
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-1">Título del Puesto</label>
                        <input
                            type="text"
                            placeholder="Ej: Data Scientist Senior"
                            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all shadow-sm"
                            value={newName}
                            onChange={e => setNewName(e.target.value)}
                        />
                    </div>

                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-1">Descripción del Puesto</label>
                        <textarea
                            placeholder="Pega aquí la descripción completa de la vacante..."
                            className="w-full p-3 border border-gray-300 rounded-lg h-32 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all shadow-sm"
                            value={newDesc}
                            onChange={e => setNewDesc(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-indigo-600 text-white font-semibold px-4 py-3 rounded-lg hover:bg-indigo-700 transition-all shadow-md active:scale-[0.99]"
                    >
                        Guardar Perfil y Generar Modelo IA
                    </button>
                </form>
            )}

            {roles.length === 0 && !isCreating ? (
                <div className="text-center py-8 text-gray-500 italic">
                    No hay perfiles creados. ¡Crea el primero arriba!
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {roles.map((role, index) => (
                        <div
                            key={index} // Usar Index como Key para estabilidad visual
                            onClick={() => {
                                setSelectedIndex(index);
                                onRoleSelect(role.id);
                            }}
                            className={`cursor-pointer p-5 rounded-xl border transition-all duration-200 relative overflow-hidden group ${index === selectedIndex
                                ? 'border-indigo-500 bg-indigo-50/50 ring-2 ring-indigo-500 shadow-md'
                                : 'border-gray-200 bg-gray-50 hover:bg-white hover:border-gray-300 hover:shadow-lg hover:-translate-y-1'
                                }`}
                        >
                            {index === selectedIndex && (
                                <div className="absolute top-0 right-0 bg-indigo-500 text-white text-xs px-2 py-1 rounded-bl-lg font-bold">
                                    ACTIVO
                                </div>
                            )}
                            <h3 className={`font-bold text-lg mb-2 ${index === selectedIndex ? 'text-indigo-900' : 'text-gray-900'}`}>{role.name}</h3>
                            <p className="text-gray-600 text-sm line-clamp-3 leading-relaxed">
                                {role.description}
                            </p>

                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    if (confirm('¿Seguro que quieres borrar este perfil?')) {
                                        import('../lib/api').then(api => {
                                            api.deleteRole(role.id).then(() => {
                                                const newRoles = roles.filter(r => r.id !== role.id);
                                                setRoles(newRoles);
                                                if (newRoles.length > 0) {
                                                    setSelectedIndex(0);
                                                    onRoleSelect(newRoles[0].id);
                                                } else {
                                                    onRoleSelect(0); // Assuming 0 or null handles empty state
                                                }
                                            });
                                        });
                                    }
                                }}
                                className="absolute top-2 right-2 p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors opacity-0 group-hover:opacity-100"
                                title="Eliminar perfil"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
