import { Routes, Route, Navigate } from 'react-router-dom';
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

      {/* Legacy redirects */}
      <Route path='/dashboard' element={<Navigate to='/game-dashboard' replace />} />

      {/* No match → home */}
      <Route path='*' element={<Navigate to='/' replace />} />
    </Routes>
  );
}
