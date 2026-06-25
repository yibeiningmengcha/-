import ReactECharts from 'echarts-for-react';
import type { GenreItem } from '@/types';
import { getGenrePieChartOption } from '@/utils/chartOptions';
import './GenrePieChart.less';

interface GenrePieChartProps {
  data: GenreItem[];
}

const GenrePieChart: React.FC<GenrePieChartProps> = ({ data }) => {
  return (
    <div className="genre-pie-chart">
      <div className="genre-pie-chart__header">
        <span className="genre-pie-chart__title">电影类型占比</span>
      </div>
      <div className="genre-pie-chart__body">
        <ReactECharts
          option={getGenrePieChartOption(data)}
          style={{ width: '100%', height: '100%' }}
          opts={{ renderer: 'canvas' }}
        />
      </div>
    </div>
  );
};

export default GenrePieChart;
