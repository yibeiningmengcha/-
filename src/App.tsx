import { useEffect, useState, useRef } from 'react';
import autofit from 'autofit.js';
import ThreeBackground from '@/components/ThreeBackground/ThreeBackground';
import Header from '@/components/Header/Header';
import KPICards from '@/components/KPICards/KPICards';
import Top10BarChart from '@/components/Top10BarChart/Top10BarChart';
import RatingDistribution from '@/components/RatingDistribution/RatingDistribution';
import WorldMap from '@/components/WorldMap/WorldMap';
import ScatterChart from '@/components/ScatterChart/ScatterChart';
import GenrePieChart from '@/components/GenrePieChart/GenrePieChart';
import NewsBar from '@/components/NewsBar/NewsBar';
import { loadDashboardData, invalidateCache } from '@/utils/dataProcessor';
import type { DashboardData } from '@/types';
import './App.less';

/** 数据加载中的空数据占位 */
const EMPTY_DATA: DashboardData = {
  kpiMetrics: { totalMovies: 0, totalBoxOffice: 0, avgRating: 0, topBoxOfficeMovie: '--', topBoxOfficeValue: 0 },
  top10BoxOffice: [{ name: '加载中...', value: 0 }],
  ratingDistribution: [],
  ratingRangeDetails: [],
  countryDistribution: [{ name: '加载中...', value: 0 }],
  scatterData: [],
  genreDistribution: [{ name: '加载中...', value: 0, percent: 0 }],
  allDoubanMovies: [],
};

const App: React.FC = () => {
  const [data, setData] = useState<DashboardData>(EMPTY_DATA);
  const [loading, setLoading] = useState(true);
  const reloadCountRef = useRef(0);

  useEffect(() => {
    // 从两个真实Excel文件加载数据
    loadDashboardData()
      .then((dashboardData) => {
        // 防御性检查：如果ratingRangeDetails缺失但其他数据存在，说明是HMR缓存不一致
        const hasOtherData = dashboardData.ratingDistribution.length > 0
          || dashboardData.kpiMetrics.totalMovies > 0;
        const missingDetails = !dashboardData.ratingRangeDetails
          || dashboardData.ratingRangeDetails.length === 0;

        if (hasOtherData && missingDetails && reloadCountRef.current < 1) {
          reloadCountRef.current++;
          console.warn('[App] 检测到 ratingRangeDetails 缺失，清除缓存重新加载...');
          invalidateCache();
          return loadDashboardData().then((fresh) => {
            setData(fresh);
            setLoading(false);
          });
        }

        setData(dashboardData);
        setLoading(false);
      })
      .catch((err) => {
        console.error('[数据加载] 失败:', err);
        setLoading(false);
      });

    autofit.init({
      dh: 1080,
      dw: 1920,
      el: '.dashboard-container',
      resize: true,
      transition: 0.3,
    });

    return () => {
      autofit.off();
    };
  }, []);

  return (
    <div className="dashboard-container">
      <ThreeBackground />
      <Header />
      <div className="content-wrapper">
        <KPICards data={data.kpiMetrics} loading={loading} />
        <div className="main-content">
        {/* 左侧列 */}
        <div className="main-content__left">
          <Top10BarChart data={data.top10BoxOffice} allDoubanMovies={data.allDoubanMovies} />
          <RatingDistribution
            data={data.ratingDistribution}
            avgRating={data.kpiMetrics.avgRating}
            medianRating={6.9}
            stdDev={1.2}
            rangeDetails={data.ratingRangeDetails}
          />
        </div>

        {/* 中间区域 */}
        <div className="main-content__center">
          <WorldMap data={data.countryDistribution} />
        </div>

        {/* 右侧列 */}
        <div className="main-content__right">
          <ScatterChart data={data.scatterData} />
          <GenrePieChart data={data.genreDistribution} />
        </div>
      </div>
      </div>
      <NewsBar />
    </div>
  );
};

export default App;
