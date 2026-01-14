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
        const file = e.target.files[0];
        setUploading(true);
        setError('');

        try {
            await uploadCV(roleId, file);
            // Reload rankings after successful analysis
            await loadCandidates();
        } catch (err: any) {
            setError(err.message || 'Upload failed');
        } finally {
            setUploading(false);
            // Clear input
            e.target.value = '';
        }
    }

    function getScoreColor(score: number): string {
        if (score >= 80) return 'text-green-600 bg-green-50 ring-green-500';
        if (score >= 50) return 'text-yellow-600 bg-yellow-50 ring-yellow-500';
        return 'text-red-600 bg-red-50 ring-red-500';
    }

    return (
        <div className="p-6 bg-white rounded-xl shadow-lg border border-gray-100">
            <h2 className="text-xl font-bold text-gray-800 mb-6">2. Upload & Rank CVs</h2>

            {/* Upload Zone */}
            <div className="mb-8">
                <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <svg aria-hidden="true" className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                        <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload CV</span> (PDF or DOCX)</p>
                    </div>
                    <input type="file" className="hidden" onChange={handleFileUpload} accept=".pdf,.docx" disabled={uploading} />
                </label>
                {uploading && (
                    <div className="mt-4 flex items-center justify-center text-blue-600 animate-pulse">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Analizando CV con IA...
                    </div>
                )}
                {error && <p className="mt-2 text-sm text-red-600 font-medium">{error}</p>}
            </div>

            {/* Results Table */}
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-gray-500">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                        <tr>
                            <th scope="col" className="px-6 py-3">Rank</th>
                            <th scope="col" className="px-6 py-3">Score</th>
                            <th scope="col" className="px-6 py-3">Candidate</th>
                            <th scope="col" className="px-6 py-3">Matched Skills</th>
                        </tr>
                    </thead>
                    <tbody>
                        {candidates.map((cand, index) => (
                            <tr key={cand.id} className="bg-white border-b hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 font-bold text-gray-900">#{index + 1}</td>
                                <td className="px-6 py-4">
                                    <div className={`relative w-12 h-12 flex items-center justify-center rounded-full ring-4 font-bold text-sm ${getScoreColor(cand.score)}`}>
                                        {cand.score}
                                    </div>
                                </td>
                                <td className="px-6 py-4 font-medium text-gray-900">
                                    {cand.filename}
                                </td>
                                <td className="px-6 py-4">
                                    <div className="flex flex-wrap gap-2">
                                        {cand.matched_skills.map(skill => (
                                            <span key={skill} className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded border border-blue-200 uppercase">
                                                {skill}
                                            </span>
                                        ))}
                                        {cand.matched_skills.length === 0 && <span className="text-gray-400 italic">No specific matches</span>}
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {candidates.length === 0 && !uploading && (
                            <tr>
                                <td colSpan={4} className="px-6 py-10 text-center text-gray-400">
                                    No CVs uploaded yet.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
