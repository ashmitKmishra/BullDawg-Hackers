// InsuranceCoverageChart.jsx - Component for comparing deductibles and out-of-pocket max
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

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const InsuranceCoverageChart = ({ plans, animate = true }) => {
  const data = {
    labels: plans.map(plan => plan.tier_name),
    datasets: [
      {
        label: 'Annual Deductible ($)',
        data: plans.map(plan => plan.deductible_annual),
        backgroundColor: 'rgba(168, 85, 247, 0.8)',  // Purple
        borderColor: 'rgba(168, 85, 247, 1)',
        borderWidth: 3,
        borderRadius: 8,
        hoverBackgroundColor: 'rgba(168, 85, 247, 1)',
        hoverBorderWidth: 4
      },
      {
        label: 'Out-of-Pocket Max ($)',
        data: plans.map(plan => plan.out_of_pocket_max),
        backgroundColor: 'rgba(14, 165, 233, 0.8)',  // Sky Blue
        borderColor: 'rgba(14, 165, 233, 1)',
        borderWidth: 3,
        borderRadius: 8,
        hoverBackgroundColor: 'rgba(14, 165, 233, 1)',
        hoverBorderWidth: 4
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: animate ? 1500 : 0,
      easing: 'easeInOutBounce',
      delay: (context) => {
        let delay = 0;
        if (context.type === 'data' && context.mode === 'default') {
          delay = context.dataIndex * 150 + context.datasetIndex * 100;
        }
        return delay;
      }
    },
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: { size: 14, weight: 'bold' },
          padding: 15,
          usePointStyle: true
        }
      },
      title: {
        display: true,
        text: '🏥 Deductible & Out-of-Pocket Comparison',
        font: {
          size: 20,
          weight: 'bold'
        },
        padding: 20
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(0, 0, 0, 0.9)',
        titleFont: { size: 16, weight: 'bold' },
        bodyFont: { size: 14 },
        padding: 15,
        cornerRadius: 10,
        displayColors: true,
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: $${context.parsed.y.toLocaleString()}`;
          },
          footer: function(tooltipItems) {
            const plan = plans[tooltipItems[0].dataIndex];
            return `\nCopay: ${plan.copay_percentage}%\nNetwork: ${plan.network_type}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
          lineWidth: 1
        },
        ticks: {
          font: { size: 12 },
          callback: function(value) {
            return '$' + value.toLocaleString();
          }
        }
      },
      x: {
        grid: {
          display: false
        },
        ticks: {
          font: { size: 12, weight: 'bold' }
        }
      }
    },
    onHover: (event, activeElements) => {
      event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
    }
  };

  return (
    <div style={{ height: '400px', marginBottom: '2rem' }}>
      <Bar data={data} options={options} />
    </div>
  );
};

export default InsuranceCoverageChart;
