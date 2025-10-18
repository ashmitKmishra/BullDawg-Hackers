// InsuranceCopayChart.jsx - Component for comparing copay percentages
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  Title
);

const InsuranceCopayChart = ({ plans }) => {
  const data = {
    labels: plans.map(plan => plan.tier_name),
    datasets: [
      {
        label: 'Copay Percentage',
        data: plans.map(plan => plan.copay_percentage),
        backgroundColor: [
          'rgba(205, 127, 50, 0.7)',
          'rgba(192, 192, 192, 0.7)',
          'rgba(255, 215, 0, 0.7)',
          'rgba(229, 228, 226, 0.7)'
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
        position: 'right',
      },
      title: {
        display: true,
        text: 'Copay Percentage Distribution',
        font: {
          size: 18
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.label}: ${context.parsed}% copay`;
          }
        }
      }
    }
  };

  return (
    <div style={{ height: '400px', marginBottom: '2rem' }}>
      <Doughnut data={data} options={options} />
    </div>
  );
};

export default InsuranceCopayChart;
