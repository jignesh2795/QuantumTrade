import Dashboard from "../components/Dashboard";

const DashboardPage = () => {
  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1 className="text-3xl font-bold mb-2">QuantumTrade Dashboard</h1>
        <p className="text-gray-600 mb-6">
          Real-time trading analytics and portfolio management
        </p>
      </div>

      <div className="dashboard-layout">
        {/* Main dashboard */}
        <div className="dashboard-section main-dashboard">
          <Dashboard />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
