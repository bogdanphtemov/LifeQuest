import { Routes, Route, Navigate } from 'react-router-dom';
import { CharacterDashboardPage } from '@/pages/CharacterDashboard';
import { StartGamePage } from '@/pages/StartGame';
import { GameDashboardPage } from '@/pages/GameDashboard';
import { CharacterCreationPage } from '@/pages/CharacterCreation';

export function AppRouter() {
  return (
    <Routes>
      {/* Entry point — animated Start Screen */}
      <Route path='/' element={<StartGamePage />} />

      {/* Game dashboard — requires existing character */}
      <Route path='/game-dashboard' element={<GameDashboardPage />} />

      {/* Character creation — for new players */}
      <Route path='/character-creation' element={<CharacterCreationPage />} />

      {/* Legacy dashboard path */}
      <Route path='/dashboard' element={<CharacterDashboardPage />} />

      {/* No match → home */}
      <Route path='*' element={<Navigate to='/' replace />} />
    </Routes>
  );
}
