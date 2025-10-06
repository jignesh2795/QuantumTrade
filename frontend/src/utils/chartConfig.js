export const portfolioChartConfig = {
  type: 'pie',
  data: {
    labels: [],
    datasets: [{
      data: [],
      backgroundColor: [
        '#3b82f6',
        '#10b981',
        '#f59e0b',
        '#ef4444',
        '#8b5cf6'
      ]
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'right'
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.label}: $${context.raw.toFixed(2)}`;
          }
        }
      }
    }
  }
};

export const performanceChartConfig = {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Portfolio Value',
      data: [],
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.1,
      fill: true
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function(value) {
            return '$' + value.toFixed(2);
          }
        }
      }
    }
  }
};
