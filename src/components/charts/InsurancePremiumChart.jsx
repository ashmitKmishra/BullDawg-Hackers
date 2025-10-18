// InsurancePremiumChart.jsx - Component for comparing monthly premiums
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const InsurancePremiumChart = ({ plans }) => {
  const data = {
    labels: plans.map(plan => plan.tier_name),
    datasets: [
      {
        label: 'Monthly Premium ($)',
        data: plans.map(plan => plan.premium_monthly),
        backgroundColor: [
          'rgba(205, 127, 50, 0.7)',   // Bronze
          'rgba(192, 192, 192, 0.7)',  // Silver
          'rgba(255, 215, 0, 0.7)',    // Gold
          'rgba(229, 228, 226, 0.7)'   // Platinum
        ],
        borderColor: [
          'rgba(205, 127, 50, 1)',
          'rgba(192, 192, 192, 1)',
          'rgba(255, 215, 0, 1)',
          'rgba(229, 228, 226, 1)'
        ],
        borderWidth: 2
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Monthly Premium Comparison',
        font: {
          size: 18
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Premium: $${context.parsed.y}/month`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return '$' + value;
          }
        }
      }
    }
  };

  return (
    <div style={{ height: '400px', marginBottom: '2rem' }}>
      <Bar data={data} options={options} />
    </div>
  );
};

export default InsurancePremiumChart;
