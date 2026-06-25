import ReactECharts from 'echarts-for-react';
import type { EChartsOption } from 'echarts';
import * as echarts from 'echarts';
import type { RatingRangeDetail } from '@/types';
import './RatingDetailModal.less';

interface RatingDetailModalProps {
  data: RatingRangeDetail | null;
  onClose: () => void;
}

/* ---- 左侧：评分排名横向条形图 ---- */
function getRankBarOption(movies: RatingRangeDetail['movies']): EChartsOption {
  const reversed = [...movies].reverse();
  return {
    grid: { left: '3%', right: '10%', top: '4%', bottom: '2%', containLabel: true },
    xAxis: { type: 'value', max: 10, min: 0, interval: 2,
      axisLine: { lineStyle: { color: 'rgba(0,212,255,0.25)' } },
      axisLabel: { color: '#6b8299', fontSize: 10 },
      splitLine: { lineStyle: { color: 'rgba(0,212,255,0.08)' } },
    },
    yAxis: {
      type: 'category', data: reversed.map((m) => m.name),
      axisLine: { lineStyle: { color: 'rgba(0,212,255,0.2)' } },
      axisLabel: { color: '#c0d0e6', fontSize: 11, width: 120, overflow: 'truncate' },
      axisTick: { show: false },
    },
    series: [{
      type: 'bar',
      data: reversed.map((m) => m.rating),
      barWidth: 14,
      itemStyle: {
        borderRadius: [0, 3, 3, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#0066cc' },
          { offset: 1, color: '#00d4ff' },
        ]),
      },
      label: { show: true, position: 'right', color: '#00d4ff', fontSize: 11, fontWeight: 'bold',
        formatter: '{c}' },
      emphasis: { itemStyle: { shadowBlur: 8, shadowColor: 'rgba(0,212,255,0.5)' } },
    }],
    tooltip: {
      trigger: 'axis', backgroundColor: 'rgba(13,27,62,0.95)', borderColor: 'rgba(0,212,255,0.3)',
      textStyle: { color: '#e0e6ed' },
      formatter: (params: any) => {
        const i = params[0];
        const movie = reversed[reversed.length - 1 - i.dataIndex];
        return `${i.name}<br/>豆瓣评分：<b style="color:#00d4ff">${i.value}</b><br/>评价人数：${movie?.reviews || '--'} 人`;
      },
    },
  };
}

/* ---- 右上：类型分布饼图 ---- */
function getGenrePieOption(movies: RatingRangeDetail['movies']): EChartsOption {
  // 统计类型
  const genreMap: Record<string, number> = {};
  for (const m of movies) {
    if (!m.genres) continue;
    for (const g of m.genres.split('/').map((s) => s.trim()).filter(Boolean)) {
      genreMap[g] = (genreMap[g] || 0) + 1;
    }
  }
  const entries = Object.entries(genreMap).sort(([, a], [, b]) => b - a).slice(0, 7);
  if (entries.length === 0) return {};
  const total = entries.reduce((s, [, v]) => s + v, 0);
  const pieColors = ['#00d4ff','#00aaff','#0088cc','#66bbff','#99ccff','#a78bfa','#f472b6'];

  return {
    tooltip: {
      trigger: 'item', backgroundColor: 'rgba(13,27,62,0.95)', borderColor: 'rgba(0,212,255,0.3)',
      textStyle: { color: '#e0e6ed' }, formatter: '{b}: {c}部 ({d}%)',
    },
    legend: { show: false },
    series: [{
      type: 'pie', radius: ['40%', '72%'], center: ['50%', '52%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 4, borderColor: '#0a1628', borderWidth: 2 },
      label: { show: true, color: '#b0c4de', fontSize: 10, formatter: '{b}\n{d}%' },
      data: entries.map(([name, value], i) => ({ name, value, itemStyle: { color: pieColors[i % pieColors.length] } })),
    }],
  };
}

/* ---- 右下：评价人数柱形图（对比各电影热度）---- */
function getReviewsBarOption(movies: RatingRangeDetail['movies']): EChartsOption {
  const names = movies.map((m) => m.name);
  const values = movies.map((m) => m.reviews);
  const maxVal = Math.max(...values, 1);

  return {
    grid: { left: '3%', right: '8%', top: '6%', bottom: '2%', containLabel: true },
    xAxis: {
      type: 'category', data: names,
      axisLine: { lineStyle: { color: 'rgba(0,212,255,0.2)' } },
      axisLabel: { color: '#8a9bb3', fontSize: 9, rotate: 30, width: 60, overflow: 'truncate' },
      axisTick: { show: false },
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: 'rgba(0,212,255,0.15)' } },
      axisLabel: { color: '#6b8299', fontSize: 9, formatter: (v: number) => v >= 10000 ? (v / 10000).toFixed(1) + 'w' : String(v) },
      splitLine: { lineStyle: { color: 'rgba(0,212,255,0.08)' } },
    },
    series: [{
      type: 'bar',
      data: values,
      barWidth: '50%',
      itemStyle: {
        borderRadius: [3, 3, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#f472b6' },
          { offset: 1, color: '#a78bfa' },
        ]),
      },
      tooltip: {
        trigger: 'axis', backgroundColor: 'rgba(13,27,62,0.95)', borderColor: 'rgba(0,212,255,0.3)',
        textStyle: { color: '#e0e6ed' },
        formatter: (params: any) => `${params[0].name}<br/>评价人数：<b style="color:#f472b6">${params[0].value.toLocaleString()}</b> 人`,
      },
    }],
  };
}

const RatingDetailModal: React.FC<RatingDetailModalProps> = ({ data, onClose }) => {
  if (!data) return null;

  const hasMovies = data.movies.length > 0;

  return (
    <div className="rating-modal-overlay" onClick={onClose}>
      <div className="rating-modal" onClick={(e) => e.stopPropagation()}>
        {/* 标题栏 */}
        <div className="rating-modal__header">
          <div className="rating-modal__title-wrap">
            <span className="rating-modal__title">「{data.range}」评分区间 · TOP 电影排行</span>
            <span className="rating-modal__subtitle">共 {data.count} 部电影</span>
          </div>
          <button className="rating-modal__close" onClick={onClose}>&times;</button>
        </div>

        {/* 内容区 */}
        <div className="rating-modal__body">
          {hasMovies ? (
            <>
              {/* 左侧：评分排名条形图 */}
              <div className="rating-modal__chart rating-modal__chart--rank">
                <div className="rating-modal__chart-title">评分排名</div>
                <ReactECharts
                  option={getRankBarOption(data.movies)}
                  style={{ width: '100%', height: '100%' }}
                  opts={{ renderer: 'canvas' }}
                />
              </div>

              {/* 右侧 */}
              <div className="rating-modal__right">
                {/* 右上：类型分布饼图 */}
                <div className="rating-modal__chart rating-modal__chart--pie">
                  <div className="rating-modal__chart-title">类型分布</div>
                  <ReactECharts
                    option={getGenrePieOption(data.movies)}
                    style={{ width: '100%', height: '100%' }}
                    opts={{ renderer: 'canvas' }}
                  />
                </div>

                {/* 右下：评价人数对比 + 电影卡片列表 */}
                <div className="rating-modal__bottom">
                  <div className="rating-modal__chart rating-modal__chart--reviews">
                    <div className="rating-modal__chart-title">评价人数对比</div>
                    <ReactECharts
                      option={getReviewsBarOption(data.movies)}
                      style={{ width: '100%', height: '100%' }}
                      opts={{ renderer: 'canvas' }}
                    />
                  </div>

                  {/* 电影详情卡片 */}
                  <div className="rating-modal__cards">
                    {data.movies.slice(0, 5).map((m, idx) => (
                      <div key={idx} className="rating-modal__card">
                        <span className="rating-modal__card-rank">{idx + 1}</span>
                        <div className="rating-modal__card-info">
                          <div className="rating-modal__card-name">{m.name}</div>
                          <div className="rating-modal__card-meta">
                            <span>{m.rating}分</span>
                            {m.country && <span>{m.country.split('/')[0]}</span>}
                          </div>
                        </div>
                        <div className="rating-modal__card-reviews">{m.reviews > 0 ? m.reviews.toLocaleString() : '-'}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="rating-modal__empty">该评分区间暂无电影数据</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RatingDetailModal;
