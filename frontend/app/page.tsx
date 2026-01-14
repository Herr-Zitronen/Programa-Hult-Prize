"use client";

import { useState } from 'react';
import RoleManager from '../components/RoleManager';
import CandidateRanker from '../components/CandidateRanker';

export default function Home() {
  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight sm:text-5xl">
            AI Recruitment <span className="text-blue-600">Assistant</span>
          </h1>
          <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
            Intelligent candidate screening powered by semantic analysis.
          </p>
        </div>

        <div className="space-y-8">
          <RoleManager
            selectedRoleId={selectedRoleId}
            onRoleSelect={setSelectedRoleId}
          />

          {selectedRoleId ? (
            <CandidateRanker roleId={selectedRoleId} />
          ) : (
            <div className="text-center p-12 bg-white rounded-lg border border-dashed border-gray-300">
              <p className="text-gray-500">Please select or create a role to start ranking candidates.</p>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
