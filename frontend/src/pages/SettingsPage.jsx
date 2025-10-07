import axios from "axios";
import { useEffect, useState } from "react";

const SettingsPage = () => {
  const [configurations, setConfigurations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  useEffect(() => {
    fetchConfigurations();
  }, []);

  const fetchConfigurations = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/api/config");
      setConfigurations(response.data.configurations || []);
    } catch (err) {
      setError("Failed to fetch configurations");
      console.error("Error fetching configurations:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleConfigChange = (id, newValue) => {
    setConfigurations(
      configurations.map((config) =>
        config.id === id ? { ...config, value: newValue } : config
      )
    );
  };

  const saveConfigurations = async () => {
    try {
      setSaving(true);
      setSuccess(null);
      setError(null);

      // Send updated configurations to backend
      for (const config of configurations) {
        await axios.put(`/api/config/${config.key}`, {
          value: config.value,
          description: config.description,
        });
      }

      setSuccess("Configurations saved successfully!");
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError("Failed to save configurations");
      console.error("Error saving configurations:", err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="settings-page">Loading configurations...</div>;
  }

  return (
    <div className="settings-page">
      <div className="page-header">
        <h1>Settings</h1>
        <p>Configure trading strategies and system parameters</p>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="settings-section">
        <h2>Trading Configuration</h2>
        <div className="config-grid">
          {configurations.map((config) => (
            <div key={config.id} className="config-item">
              <label>
                <strong>{config.key}</strong>
                <span className="config-description">{config.description}</span>
              </label>
              <input
                type="text"
                value={config.value}
                onChange={(e) => handleConfigChange(config.id, e.target.value)}
                className="config-input"
              />
            </div>
          ))}
        </div>

        <div className="settings-actions">
          <button
            onClick={saveConfigurations}
            disabled={saving}
            className="save-button"
          >
            {saving ? "Saving..." : "Save Configurations"}
          </button>
        </div>
      </div>

      <div className="settings-section">
        <h2>Strategy Management</h2>
        <div className="strategy-controls">
          <button className="strategy-button">Backtest Strategy</button>
          <button className="strategy-button">Optimize Parameters</button>
          <button className="strategy-button">Export Strategy</button>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
