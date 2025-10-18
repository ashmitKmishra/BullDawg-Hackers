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

const InsurancePremiumChart = ({ plans, animate = true }) => {
  const data = {
    labels: plans.map(plan => plan.tier_name),
    datasets: [
      {
        label: 'Monthly Premium ($)',
        data: plans.map(plan => plan.premium_monthly),
        backgroundColor: [
          'rgba(251, 146, 60, 0.8)',   // Orange
          'rgba(59, 130, 246, 0.8)',   // Blue
          'rgba(234, 179, 8, 0.8)',    // Yellow
          'rgba(168, 85, 247, 0.8)'    // Purple
        ],
        borderColor: [
          'rgba(251, 146, 60, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(234, 179, 8, 1)',
          'rgba(168, 85, 247, 1)'
        ],
        borderWidth: 3,
        borderRadius: 8,
        hoverBackgroundColor: [
          'rgba(251, 146, 60, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(234, 179, 8, 1)',
          'rgba(168, 85, 247, 1)'
        ],
        hoverBorderWidth: 4
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: animate ? 1500 : 0,
      easing: 'easeInOutQuart',
      delay: (context) => {
        let delay = 0;
        if (context.type === 'data' && context.mode === 'default') {
          delay = context.dataIndex * 200;
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
        text: '💰 Monthly Premium Comparison',
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
            const plan = plans[context.dataIndex];
            return [
              `Premium: $${context.parsed.y}/month`,
              `Annual Cost: $${(context.parsed.y * 12).toLocaleString()}`,
              `Network: ${plan.network_type}`
            ];
          },
          afterLabel: function(context) {
            return '\n💡 Hover to see more details';
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
            return '$' + value;
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

export default InsurancePremiumChart;
