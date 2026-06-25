import { useState, useCallback, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import type { RatingDistItem, RatingRangeDetail } from '@/types';
import { getRatingDistributionOption } from '@/utils/chartOptions';
import RatingDetailModal from '@/components/RatingDetailModal/RatingDetailModal';
import './RatingDistribution.less';

interface RatingDistributionProps {
  data: RatingDistItem[];
  avgRating: number;
  medianRating: number;
  stdDev: number;
  rangeDetails?: RatingRangeDetail[];
}

const RatingDistribution: React.FC<RatingDistributionProps> = ({
  data,
  avgRating,
  medianRating,
  stdDev,
  rangeDetails = [],
}) => {
  const [selectedRange, setSelectedRange] = useState<RatingRangeDetail | null>(null);

  useEffect(() => {
    if (rangeDetails && rangeDetails.length > 0) {
      console.log('[RatingDistribution] 收到评分区间明细:',
        rangeDetails.filter(d => d.count > 0).map(d => `${d.range}:${d.count}部`));
    } else {
      console.log('[RatingDistribution] ratingRangeDetails 为空或未提供');
    }
  }, [rangeDetails]);

  const handleChartClick = useCallback((params: any) => {
    if (params.componentType === 'series' && params.dataIndex != null) {
      const rangeStr = data[params.dataIndex]?.range;
      if (rangeStr) {
        const detail = rangeDetails.find((d) => d.range === rangeStr);
        setSelectedRange(detail || { range: rangeStr, count: 0, movies: [] });
      }
    }
  }, [data, rangeDetails]);

  return (
    <div className="rating-distribution">
      <div className="rating-distribution__header">
        <span className="rating-distribution__title">豆瓣评分分布</span>
        <span className="rating-distribution__unit">单位：部</span>
      </div>
      <div className="rating-distribution__body">
        <ReactECharts
          option={getRatingDistributionOption(data)}
          style={{ width: '100%', height: '100%' }}
          opts={{ renderer: 'canvas' }}
          onEvents={{ click: handleChartClick }}
        />
      </div>
      <div className="rating-distribution__footer">
        <span>平均评分：<strong>{avgRating}</strong></span>
        <span>中位数：<strong>{medianRating}</strong></span>
        <span>标准差：<strong>{stdDev}</strong></span>
      </div>

      {/* 二级弹窗 */}
      <RatingDetailModal data={selectedRange} onClose={() => setSelectedRange(null)} />
    </div>
  );
};

export default RatingDistribution;
