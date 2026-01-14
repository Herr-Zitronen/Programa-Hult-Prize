"use client";

import { useState, useEffect } from 'react';
import { fetchRankings, uploadCV } from '../lib/api';

interface Candidate {
    id: number;
    filename: string;
    score: number;
    matched_skills: string[];
}

export default function CandidateRanker({ roleId }: { roleId: number }) {
    const [candidates, setCandidates] = useState<Candidate[]>([]);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (roleId) loadCandidates();
    }, [roleId]);

    async function loadCandidates() {
        try {
            const data = await fetchRankings(roleId);
            setCandidates(data);
        } catch (err) {
            console.error(err);
        }
    }

    async function handleFileUpload(e: React.ChangeEvent<HTMLInputElement>) {
        if (!e.target.files?.length) return;

        const files = Array.from(e.target.files);
        setUploading(true);
        setError('');

        try {
            // Process all files
            for (const file of files) {
                await uploadCV(roleId, file);
            }
            await loadCandidates();
        } catch (err: any) {
            setError(err.message || 'Fallo en la subida de algunos archivos');
        } finally {
            setUploading(false);
            e.target.value = '';
        }
    }

    function getScoreColor(score: number): string {
        if (score >= 80) return 'text-emerald-700 bg-emerald-100 ring-emerald-500/30';
        if (score >= 50) return 'text-amber-700 bg-amber-100 ring-amber-500/30';
        return 'text-rose-700 bg-rose-100 ring-rose-500/30';
    }

    return (
        <div className="p-8 bg-white rounded-2xl shadow-xl border border-gray-100 ring-1 ring-black/5">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 tracking-tight">
                2. Análisis y Ranking de Candidatos
            </h2>

            {/* Upload Zone */}
            <div className="mb-10">
                <label className={`flex flex-col items-center justify-center w-full h-40 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-300 group
          ${uploading ? 'bg-gray-50 border-gray-300' : 'bg-gray-50 border-gray-300 hover:bg-indigo-50 hover:border-indigo-400'}`}>

                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        {!uploading ? (
                            <>
                                <svg className="w-12 h-12 mb-4 text-gray-400 group-hover:text-indigo-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                                <p className="mb-2 text-lg text-gray-600 font-medium">Arrastra y suelta tu CV aquí</p>
                                <p className="text-sm text-gray-500">(Formatos soportados: PDF o DOCX)</p>
                            </>
                        ) : (
                            <div className="flex flex-col items-center animate-pulse">
                                <svg className="animate-spin mb-3 h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <span className="text-indigo-600 font-semibold text-lg">Analizando perfil con IA...</span>
                            </div>
                        )}
                    </div>
                    <input type="file" className="hidden" onChange={handleFileUpload} accept=".pdf,.docx" disabled={uploading} multiple />
                </label>
                {error && (
                    <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
                        <span className="text-red-500 font-bold">⚠️</span>
                        <p className="text-sm text-red-700 font-medium">{error}</p>
                    </div>
                )}
            </div>

            {/* Results Table */}
            <div className="overflow-hidden rounded-xl border border-gray-200 shadow-sm">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50/80 border-b border-gray-200">
                        <tr>
                            <th scope="col" className="px-6 py-4 font-bold tracking-wider"># Posición</th>
                            <th scope="col" className="px-6 py-4 font-bold tracking-wider">Compatibilidad</th>
                            <th scope="col" className="px-6 py-4 font-bold tracking-wider">Candidato</th>
                            <th scope="col" className="px-6 py-4 font-bold tracking-wider">Habilidades Detectadas</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                        {candidates.map((cand, index) => (
                            <tr key={cand.id} className="bg-white hover:bg-gray-50 transition-colors duration-150">
                                <td className="px-6 py-4">
                                    <span className={`flex items-center justify-center w-8 h-8 rounded-full font-bold text-white shadow-sm
                    ${index === 0 ? 'bg-amber-400 ring-2 ring-amber-200' :
                                            index === 1 ? 'bg-slate-400 ring-2 ring-slate-200' :
                                                index === 2 ? 'bg-orange-400 ring-2 ring-orange-200' : 'bg-gray-200 text-gray-600'}`}>
                                        {index + 1}
                                    </span>
                                </td>
                                <td className="px-6 py-4">
                                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-bold shadow-sm ring-1 ${getScoreColor(cand.score)}`}>
                                        {cand.score}%
                                    </div>
                                </td>
                                <td className="px-6 py-4 font-semibold text-gray-900 text-base">
                                    {cand.filename}
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex flex-wrap gap-2">
                                        {cand.matched_skills.map(skill => (
                                            <span key={skill} className="bg-indigo-100 text-indigo-800 font-semibold px-3 py-1 rounded-full text-sm mr-2 mb-2 inline-block shadow-sm">
                                                {skill}
                                            </span>
                                        ))}
                                        {cand.matched_skills.length === 0 && <span className="text-gray-400 italic text-xs">Sin coincidencias clave</span>}
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {candidates.length === 0 && !uploading && (
                            <tr>
                                <td colSpan={4} className="px-6 py-16 text-center text-gray-400">
                                    <div className="flex flex-col items-center">
                                        <span className="text-4xl mb-2">📂</span>
                                        <p className="text-lg font-medium">No hay candidatos aún.</p>
                                        <p className="text-sm">Sube un CV arriba para comenzar el ranking.</p>
                                    </div>
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
