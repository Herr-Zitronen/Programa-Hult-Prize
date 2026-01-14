"use client";

import { useState } from 'react';
import Image from 'next/image';
import RoleManager from '../components/RoleManager';
import CandidateRanker from '../components/CandidateRanker';

export default function Home() {
  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);

  return (
    <main className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-blue-50 py-16 px-4 sm:px-6 lg:px-8 font-sans text-gray-800">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <Image
            src="/logo.jpeg"
            alt="optiTal Logo"
            width={300}
            height={100}
            className="mx-auto mb-8 drop-shadow-md hover:scale-105 transition-transform duration-300"
            priority
          />
          <div className="inline-block px-4 py-1.5 mb-4 bg-indigo-100 text-indigo-700 rounded-full text-sm font-semibold tracking-wide shadow-sm">
            ✨ Hult Prize Edition
          </div>
          <h1 className="text-5xl font-extrabold text-gray-900 tracking-tight sm:text-6xl mb-6 drop-shadow-sm">
            Sistema de Reclutamiento  <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-600">IA</span>
          </h1>
          <p className="mt-4 max-w-2xl text-xl text-gray-600 mx-auto leading-relaxed">
            Optimiza tu selección de talento con inteligencia artificial. Compara perfiles, analiza habilidades y encuentra al candidato ideal en segundos.
          </p>
        </div>

        <div className="space-y-12">
          <RoleManager
            selectedRoleId={selectedRoleId}
            onRoleSelect={setSelectedRoleId}
          />

          <div className="transition-all duration-500 ease-in-out">
            {selectedRoleId ? (
              <CandidateRanker roleId={selectedRoleId} />
            ) : (
              <div className="text-center p-16 bg-white/50 rounded-2xl border-2 border-dashed border-gray-300 backdrop-blur-sm">
                <p className="text-gray-500 text-lg font-medium">👈 Selecciona o crea un perfil arriba para comenzar</p>
              </div>
            )}
          </div>
        </div>

        <footer className="mt-20 text-center text-gray-400 text-sm">
          <p>© 2026 AI Recruitment MVP. Desarrollado para Hult Prize.</p>
        </footer>
      </div>
    </main>
  );
}
