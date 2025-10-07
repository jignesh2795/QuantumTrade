const DashboardPage = () => {
  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>QuantumTrade Dashboard</h1>
        <p>Real-time trading analytics and portfolio management</p>
      </div>

      <div className="dashboard-layout">
        {/* Top section with price ticker */}
        <div className="dashboard-section ticker-section">
          <PriceTicker />
        </div>

        {/* Main dashboard */}
        <div className="dashboard-section main-dashboard">
          <Dashboard />
        </div>

        {/* Performance metrics */}
        <div className="dashboard-section performance-section">
          <PerformanceMetrics />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
