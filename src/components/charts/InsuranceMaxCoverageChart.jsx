// InsuranceMaxCoverageChart.jsx - Component for comparing maximum coverage
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const InsuranceMaxCoverageChart = ({ plans }) => {
  const data = {
    labels: plans.map(plan => plan.tier_name),
    datasets: [
      {
        label: 'Maximum Coverage ($)',
        data: plans.map(plan => plan.coverage_max),
        fill: true,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 3,
        tension: 0.4,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBackgroundColor: 'rgba(75, 192, 192, 1)'
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
        text: 'Maximum Coverage Comparison',
        font: {
          size: 18
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Max Coverage: $${context.parsed.y.toLocaleString()}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return '$' + (value / 1000000).toFixed(1) + 'M';
          }
        }
      }
    }
  };

  return (
    <div style={{ height: '400px', marginBottom: '2rem' }}>
      <Line data={data} options={options} />
    </div>
  );
};

export default InsuranceMaxCoverageChart;
