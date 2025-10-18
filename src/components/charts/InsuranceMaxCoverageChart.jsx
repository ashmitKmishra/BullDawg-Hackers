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

const InsuranceMaxCoverageChart = ({ plans, animate = true }) => {
  const data = {
    labels: plans.map(plan => plan.tier_name),
    datasets: [
      {
        label: 'Maximum Coverage ($)',
        data: plans.map(plan => plan.coverage_max),
        fill: true,
        backgroundColor: 'rgba(16, 185, 129, 0.3)',  // Emerald green
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 4,
        tension: 0.4,
        pointRadius: 8,
        pointHoverRadius: 12,
        pointBackgroundColor: 'rgba(16, 185, 129, 1)',
        pointBorderColor: '#fff',
        pointBorderWidth: 3,
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(16, 185, 129, 1)',
        pointHoverBorderWidth: 4
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: animate ? 2000 : 0,
      easing: 'easeInOutCubic',
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
        text: '🛡️ Maximum Coverage Comparison',
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
              `Max Coverage: $${context.parsed.y.toLocaleString()}`,
              `Monthly Premium: $${plan.premium_monthly}`,
              `Deductible: $${plan.deductible_annual.toLocaleString()}`
            ];
          },
          footer: function(tooltipItems) {
            const plan = plans[tooltipItems[0].dataIndex];
            return `\n✨ ${plan.family_coverage ? 'Includes Family Coverage' : 'Individual Only'}`;
          }
        }
      },
      filler: {
        propagate: true
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(16, 185, 129, 0.1)',
          lineWidth: 1
        },
        ticks: {
          font: { size: 12 },
          callback: function(value) {
            return '$' + (value / 1000000).toFixed(1) + 'M';
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
      <Line data={data} options={options} />
    </div>
  );
};

export default InsuranceMaxCoverageChart;
