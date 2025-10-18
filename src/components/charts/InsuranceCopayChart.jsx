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

const InsuranceCopayChart = ({ plans, animate = true }) => {
  const data = {
    labels: plans.map(plan => plan.tier_name),
    datasets: [
      {
        label: 'Copay Percentage',
        data: plans.map(plan => plan.copay_percentage),
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
        hoverOffset: 30,
        hoverBorderWidth: 5
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      animateRotate: animate,
      animateScale: animate,
      duration: animate ? 2000 : 0,
      easing: 'easeInOutElastic'
    },
    interaction: {
      mode: 'point',
    },
    plugins: {
      legend: {
        position: 'right',
        labels: {
          font: { size: 13, weight: 'bold' },
          padding: 15,
          usePointStyle: true,
          pointStyle: 'circle',
          generateLabels: function(chart) {
            const data = chart.data;
            if (data.labels.length && data.datasets.length) {
              return data.labels.map((label, i) => {
                const dataset = data.datasets[0];
                const value = dataset.data[i];
                return {
                  text: `${label}: ${value}%`,
                  fillStyle: dataset.backgroundColor[i],
                  strokeStyle: dataset.borderColor[i],
                  lineWidth: 2,
                  hidden: false,
                  index: i
                };
              });
            }
            return [];
          }
        }
      },
      title: {
        display: true,
        text: '📊 Copay Percentage Distribution',
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
              `Copay: ${context.parsed}%`,
              `You pay: ${context.parsed}% of costs`,
              `Insurance covers: ${100 - context.parsed}%`
            ];
          },
          footer: function(tooltipItems) {
            const plan = plans[tooltipItems[0].dataIndex];
            return `\nPremium: $${plan.premium_monthly}/mo`;
          }
        }
      }
    },
    onHover: (event, activeElements) => {
      event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
    }
  };

  return (
    <div style={{ height: '400px', marginBottom: '2rem' }}>
      <Doughnut data={data} options={options} />
    </div>
  );
};

export default InsuranceCopayChart;
