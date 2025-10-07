import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import AnalyticsPage from "./pages/AnalyticsPage";
import BacktestPage from "./pages/BacktestPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import MarketDataPage from "./pages/MarketDataPage";
import PortfolioPage from "./pages/PortfolioPage";
import RegisterPage from "./pages/RegisterPage";
import SettingsPage from "./pages/SettingsPage";
import StrategyPage from "./pages/StrategyPage";
import TradesPage from "./pages/TradesPage";

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/portfolio" element={<PortfolioPage />} />
          <Route path="/strategy" element={<StrategyPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/market-data" element={<MarketDataPage />} />
          <Route path="/trades" element={<TradesPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/backtest" element={<BacktestPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
