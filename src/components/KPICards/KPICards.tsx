import type { KPIMetrics } from '@/types';
import './KPICards.less';

interface KPICardsProps {
  data: KPIMetrics;
  loading?: boolean;
}

const KPICards: React.FC<KPICardsProps> = ({ data, loading = false }) => {
  const displayVal = (val: string | number) => loading ? '--' : val;
  // 固定位置的卡片
  const leftFixed = {    icon: '🎬', label: '总电影数',
    value: displayVal(data.totalMovies), unit: '部',
    subText: `较去年 ↑ 12.5%`, color: '#00d4ff',
  };
  const rightFixed = {
    icon: '🏆', label: '最高票房',
    value: displayVal(data.topBoxOfficeValue.toFixed(2)), unit: '亿',
    subText: loading ? '' : `《${data.topBoxOfficeMovie}》`, color: '#ff6b6b',
  };

  // 悬浮在地球上方的卡片
  const floatingLeft = {    icon: '💰', label: '总票房',
    value: displayVal(data.totalBoxOffice.toFixed(1)), unit: '亿',
    subText: `较去年 ↑ 28.7%`, color: '#00ff88',
  };  const floatingRight = {
    icon: '⭐', label: '平均评分',
    value: displayVal(data.avgRating.toFixed(1)), unit: '分',
    subText: `较去年 ↑ 0.3`, color: '#ffd93d',
  };

  const renderCard = (card: typeof leftFixed, index: number) => (
    <div className="kpi-card" key={index}>
      <div className="kpi-card__icon" style={{ color: card.color }}>{card.icon}</div>
      <div className="kpi-card__content">
        <div className="kpi-card__label">{card.label}</div>
        <div className="kpi-card__value">
          <span className="kpi-card__number" style={{ color: card.color }}>{card.value}</span>
          <span className="kpi-card__unit">{card.unit}</span>
        </div>
        <div className="kpi-card__sub">{card.subText}</div>
      </div>
      <div className="kpi-card__glow" style={{ boxShadow: `inset 0 0 20px ${card.color}15` }} />
    </div>
  );

  return (
    <div className="kpi-cards">
      {/* 左侧固定：总电影数 */}
      <div className="kpi-cards__left">
        {renderCard(leftFixed, 0)}
      </div>

      {/* 中间区域：总票房(左) + 空间 + 平均评分(右)，对齐下方地球仪 */}
      <div className="kpi-cards__center">
        <div className="kpi-cards__center-left">
          {renderCard(floatingLeft, 1)}
        </div>
        <div className="kpi-cards__center-right">
          {renderCard(floatingRight, 2)}
        </div>
      </div>

      {/* 右侧固定：最高票房 */}
      <div className="kpi-cards__right">
        {renderCard(rightFixed, 3)}
      </div>
    </div>
  );
};

export default KPICards;
