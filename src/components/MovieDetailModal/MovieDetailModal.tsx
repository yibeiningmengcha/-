/**
 * 电影详情二级弹窗 - 散点图点击触发
 *
 * 功能：
 * - 展示电影封面图（优先使用本地素材，失败则显示占位图）
 * - 豆瓣评分 + 星级展示
 * - 5星~1星占比分布条形图
 * - 电影元数据（导演/主演/类型/国家等）
 * - 剧情简介展示区域
 * - 淡入/淡出动画效果
 */

import { useState, useEffect, useCallback } from 'react';
import ReactECharts from 'echarts-for-react';
import * as echarts from 'echarts';
import type { ScatterItem } from '@/types';
import './MovieDetailModal.less';

interface MovieDetailModalProps {
  movie: ScatterItem | null;
  onClose: () => void;
}

/**
 * 本地封面素材文件名列表（public/posters/ 目录下的文件）
 * 匹配逻辑：电影名称与文件名做模糊匹配
 */
const POSTER_FILES = [
  '功夫熊猫3 Kung Fu Panda 3.webp',
  '十万个冷笑话.webp',
  '十万个冷笑话2.webp',
  '哪吒之魔童降世.webp',
  '哪吒闹海.webp',
  '喜羊羊与灰太狼之牛气冲天.webp',
  '大世界.webp',
  '大护法.webp',
  '大闹天宫.webp',
  '大鱼海棠.webp',
  '天书奇谭.webp',
  '妙先生.webp',
  '姜子牙.webp',
  '宝莲灯.webp',
  '小门神.webp',
  '昨日青空.webp',
  '白蛇：缘起.webp',
  '罗小黑战记.webp',
  '西游记之大圣归来.webp',
  '雪人奇缘 Abominable.webp',
  '风语咒.webp',
  '魁拔Ⅲ战神崛起.webp',
  '魁拔之十万火急.webp',
  '魁拔之大战元泱界.webp',
  '麦兜·当当伴我心 麥兜‧噹噹伴我心.webp',
  '麦兜响当当 麥兜響當當.webp',
  '麦兜·我和我妈妈 麥兜‧我和我媽媽.webp',
  // === 票房Top10 系列 ===
  '皇帝的新装之圣诞大明星.webp',
  '魔比斯环 Thru the Moebius Strip.webp',
  '天池水怪.webp',
  '猿创世界之熊孩子部落.webp',
  '少年毛泽东.webp',
  '我是大熊猫之熊猫大侠.webp',
  '梦幻飞琴 The Flying Machine.webp',
  '新年来啦之大闹除夕.webp',
  '大兵金宝历险记.webp',
  '动物狂欢节.webp',
];

/**
 * 精确映射表：电影名称关键词 → 封面文件名
 * 解决繁简体混用、特殊字符(·‧-)差异、编码等问题
 */
const POSTER_KEYWORD_MAP: Record<string, string> = {
  // 麦兜系列（Excel中可能用-代替·，且繁简体不同）
  '麦兜当当伴我心': '麦兜·当当伴我心 麥兜‧噹噹伴我心.webp',
  '麦兜响当当': '麦兜响当当 麥兜響當當.webp',
  '麦兜我和我妈妈': '麦兜·我和我妈妈 麥兜‧我和我媽媽.webp',
  // 其他电影
  '功夫熊猫3': '功夫熊猫3 Kung Fu Panda 3.webp',
  '十万个冷笑话2': '十万个冷笑话2.webp',
  '十万个冷笑话': '十万个冷笑话.webp',
  '哪吒之魔童降世': '哪吒之魔童降世.webp',
  '哪吒闹海': '哪吒闹海.webp',
  '喜羊羊与灰太狼之牛气冲天': '喜羊羊与灰太狼之牛气冲天.webp',
  '大世界': '大世界.webp',
  '大护法': '大护法.webp',
  '大闹天宫': '大闹天宫.webp',
  '大鱼海棠': '大鱼海棠.webp',
  '天书奇谭': '天书奇谭.webp',
  '妙先生': '妙先生.webp',
  '姜子牙': '姜子牙.webp',
  '宝莲灯': '宝莲灯.webp',
  '小门神': '小门神.webp',
  '昨日青空': '昨日青空.webp',
  '白蛇缘起': '白蛇：缘起.webp',
  '白蛇：缘起': '白蛇：缘起.webp',
  '罗小黑战记': '罗小黑战记.webp',
  '西游记之大圣归来': '西游记之大圣归来.webp',
  '大圣归来': '西游记之大圣归来.webp',
  '雪人奇缘': '雪人奇缘 Abominable.webp',
  '风语咒': '风语咒.webp',
  '魁拔Ⅲ战神崛起': '魁拔Ⅲ战神崛起.webp',
  '魁拔3': '魁拔Ⅲ战神崛起.webp',
  '魁拔之十万火急': '魁拔之十万火急.webp',
  '魁拔之大战元泱界': '魁拔之大战元泱界.webp',
  // === 票房Top10 系列 ===
  '皇帝的新装之圣诞大明星': '皇帝的新装之圣诞大明星.webp',
  '魔比斯环3D': '魔比斯环 Thru the Moebius Strip.webp',
  '魔比斯环': '魔比斯环 Thru the Moebius Strip.webp',
  '天池水怪': '天池水怪.webp',
  '猴创世界之熊孩子': '猿创世界之熊孩子部落.webp',
  '猿创世界之熊孩子': '猿创世界之熊孩子部落.webp',
  '少年毛泽东': '少年毛泽东.webp',
  '我是大熊猫之熊猫崛起': '我是大熊猫之熊猫大侠.webp',
  '我是大熊猫': '我是大熊猫之熊猫大侠.webp',
  '梦幻飞琴': '梦幻飞琴 The Flying Machine.webp',
  '新年来啦之大闹除夕': '新年来啦之大闹除夕.webp',
  '新年来啦': '新年来啦之大闹除夕.webp',
  '大兵金宝历险记': '大兵金宝历险记.webp',
  '动物狂欢节': '动物狂欢节.webp',
};

/** 统一特殊字符用于比较（全部移除，避免编码差异） */
function normalizeForMatch(str: string): string {
  return str
    .replace(/[·‧・\-–—]/g, '')   // 去掉所有中间点和连字符
    .replace(/[：:]/g, '')          // 去掉冒号
    .replace(/\s+/g, '')            // 去掉空格
    .trim();
}

/** 根据电影名称匹配本地封面图路径 */
function findLocalPosterUrl(movieName: string): string | null {
  const normalized = normalizeForMatch(movieName);
  console.log(`[MovieDetailModal] 匹配调试: 原始="${movieName}", 归一化="${normalized}"`);

  // ===== 第1级：精确映射表匹配（最可靠） =====
  for (const [keyword, filename] of Object.entries(POSTER_KEYWORD_MAP)) {
    const normKeyword = normalizeForMatch(keyword);
    if (normalized.includes(normKeyword) || normKeyword.includes(normalized)) {
      console.log(`[MovieDetailModal] ✅ 映射表命中: "${movieName}" -> ${filename}`);
      return `/posters/${filename}`; // 不使用encodeURIComponent！
    }
  }

  // ===== 第2级：遍历文件名做归一化包含匹配 =====
  for (const file of POSTER_FILES) {
    const fn = normalizeForMatch(file.replace(/\.webp$/i, ''));
    if (normalized.includes(fn) || fn.includes(normalized)) {
      console.log(`[MovieDetailModal] ✅ 文件名命中: "${movieName}" -> ${file}`);
      return `/posters/${file}`;
    }
  }

  // ===== 第3级：逐字评分匹配 =====
  let maxScore = 0;
  let bestFile = '';
  for (const file of POSTER_FILES) {
    const fileCore = normalizeForMatch(file.replace(/\.webp$/i, '')).replace(/[A-Za-z0-9]/g, '');
    let score = 0;
    for (const ch of normalized.substring(0, 10).replace(/[A-Za-z0-9]/g, '')) {
      if (fileCore.includes(ch)) score++;
    }
    if (normalized[0] && fileCore[0] === normalized[0]) score += 3;
    if (score > maxScore) { maxScore = score; bestFile = file; }
  }
  if (maxScore >= 3) {
    console.log(`[MovieDetailModal] ⚠️ 模糊命中(score=${maxScore}): "${movieName}" -> ${bestFile}`);
    return `/posters/${bestFile}`;
  }

  console.log(`[MovieDetailModal] ❌ 未匹配: "${movieName}"`);
  return null;
}

/** 根据电影名称生成占位图URL（最终降级方案） */
function getPlaceholderUrl(name: string): string {
  const encoded = encodeURIComponent(name);
  return `https://placehold.co/300x450/0a1628/00d4ff?text=${encoded}&font=roboto`;
}

const MovieDetailModal: React.FC<MovieDetailModalProps> = ({ movie, onClose }) => {
  const [visible, setVisible] = useState(false);
  const [imgSrc, setImgSrc] = useState<string>('');
  const [imgLoaded, setImgLoaded] = useState(false);
  const [imgError, setImgError] = useState(false);

  /* ===== 动画控制 ===== */
  useEffect(() => {
    if (!movie) {
      // 关闭：先淡出再通知父组件
      setVisible(false);
      const timer = setTimeout(onClose, 200);
      return () => clearTimeout(timer);
    }
    // 打开：延迟一帧确保DOM挂载后再淡入
    setImgSrc('');
    setImgLoaded(false);
    setImgError(false);
    requestAnimationFrame(() => setVisible(true));
  }, [movie, onClose]);

  if (!movie) return null;

  /* ===== 图片加载（优先本地素材 → 降级占位图） ===== */
  useEffect(() => {
    // 优先从本地素材匹配封面图
    const localUrl = findLocalPosterUrl(movie.name);
    if (localUrl) {
      console.log(`[MovieDetailModal] 匹配到本地封面: ${movie.name} -> ${localUrl}`);
      setImgSrc(localUrl);
    } else {
      console.log(`[MovieDetailModal] 未找到本地封面，使用占位图: ${movie.name}`);
      setImgSrc(getPlaceholderUrl(movie.name));
      setImgError(true); // 标记为已降级，避免重复onError
    }
  }, [movie.name]);

  const handleImgError = useCallback(() => {
    if (!imgError) {
      console.warn(`[MovieDetailModal] 本地封面加载失败，降级为占位图: ${movie.name}`);
      setImgSrc(getPlaceholderUrl(movie.name));
      setImgError(true);
    }
  }, [imgError, movie.name]);

  /* ===== 遮罩点击关闭 ===== */
  const handleMaskClick = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).classList.contains('movie-modal__mask')) {
      setVisible(false);
      setTimeout(onClose, 200);
    }
  };

  /* ===== 星级分布图表配置 ===== */
  const getStarDistOption = () => {
    const sd = movie.starDist || { s5: 20, s4: 35, s3: 30, s2: 10, s1: 5 };
    const labels = ['5星', '4星', '3星', '2星', '1星'];
    const values = [sd.s5, sd.s4, sd.s3, sd.s2, sd.s1];
    const maxVal = Math.max(...values, 1);

    return {
      grid: { left: '0%', right: '12%', top: 5, bottom: 5, containLabel: true },
      xAxis: {
        type: 'value',
        max: Math.ceil(maxVal / 0.8),
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { show: false },
        splitLine: { show: false },
      },
      yAxis: {
        type: 'category',
        data: labels.reverse(),
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#8a9bb3', fontSize: 12, width: 30 },
        inverse: true,
      },
      series: [{
        type: 'bar',
        data: values.reverse().map((v, i) => ({
          value: v,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#f59e0b' },
              { offset: 1, color: '#d97706' },
            ]),
            borderRadius: [0, 3, 3, 0],
          },
        })),
        barWidth: 14,
        label: {
          show: true,
          position: 'right',
          color: '#94a3b8',
          fontSize: 11,
          formatter: '{c}%',
        },
      }],
    } as any;
  };

  /* ===== 渲染星级图标 ===== */
  const renderStars = (rating: number) => {
    const fullStars = Math.floor(rating / 2);
    const halfStar = rating % 2 >= 1 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;
    return (
      <span className="movie-modal__stars">
        {[...Array(fullStars)].map((_, i) => (
          <span key={`f${i}`} className="movie-modal__star movie-modal__star--full">&#9733;</span>
        ))}
        {halfStar === 1 && <span className="movie-modal__star movie-modal__star--half">&#9733;</span>}
        {[...Array(emptyStars)].map((_, i) => (
          <span key={`e${i}`} className="movie-modal__star movie-modal__star--empty">&#9734;</span>
        ))}
      </span>
    );
  };

  return (
    <div
      className={`movie-modal__mask ${visible ? 'movie-modal__mask--visible' : ''}`}
      onClick={handleMaskClick}
    >
      <div className={`movie-modal ${visible ? 'movie-modal--visible' : ''}`}>
        {/* 头部 */}
        <div className="movie-modal__header">
          <h2 className="movie-modal__name">{movie.name}</h2>
          <button className="movie-modal__close" onClick={() => { setVisible(false); setTimeout(onClose, 200); }}>&times;</button>
        </div>

        {/* 主体：左图右信息 */}
        <div className="movie-modal__body">
          {/* 左侧 - 封面图 */}
          <div className="movie-modal__poster-wrap">
            {!imgLoaded && (
              <div className="movie-modal__poster-skeleton">
                <span>加载中...</span>
              </div>
            )}
            <img
              className={`movie-modal__poster ${imgLoaded ? 'movie-modal__poster--loaded' : ''}`}
              src={imgSrc}
              alt={movie.name}
              onError={handleImgError}
              onLoad={() => setImgLoaded(true)}
            />
          </div>

          {/* 右侧 - 详情信息 */}
          <div className="movie-modal__info">
            {/* 评分区域 — 有评分数据时正常展示，无则显示"暂无评分" */}
            {movie.rating > 0 ? (
              <>
                <div className="movie-modal__rating-section">
                  <div className="movie-modal__rating-label">豆瓣评分</div>
                  <div className="movie-modal__rating-value">{movie.rating.toFixed(1)}</div>
                  <div className="movie-modal__rating-stars">{renderStars(movie.rating)}</div>
                  <div className="movie-modal__rating-count">
                    {movie.reviews >= 10000 ? `${(movie.reviews / 10000).toFixed(0)}万` : movie.reviews.toLocaleString()}人评价
                  </div>
                </div>

                {/* 星级分布 */}
                {movie.starDist && (movie.starDist.s5 + movie.starDist.s4 + movie.starDist.s3 + movie.starDist.s2 + movie.starDist.s1) > 0 && (
                  <div className="movie-modal__star-dist">
                    <ReactECharts
                      option={getStarDistOption()}
                      style={{ width: '100%', height: '150px' }}
                      opts={{ renderer: 'canvas' }}
                    />
                  </div>
                )}
              </>
            ) : (
              <div className="movie-modal__rating-section movie-modal__rating-section--empty">
                <div className="movie-modal__rating-label">豆瓣评分</div>
                <div className="movie-modal__rating-value movie-modal__rating-value--empty">暂无评分</div>
                <div className="movie-modal__rating-hint">该影片暂无豆瓣评分数据</div>
              </div>
            )}

            {/* 元数据（基础信息） */}
            <div className="movie-modal__meta">
              {movie.genres && (
                <div className="movie-modal__meta-row">
                  <span className="movie-modal__meta-key">类型：</span>
                  <span className="movie-modal__meta-val">{movie.genres}</span>
                </div>
              )}
              {movie.country && (
                <div className="movie-modal__meta-row">
                  <span className="movie-modal__meta-key">制片国家/地区：</span>
                  <span className="movie-modal__meta-val">{movie.country}</span>
                </div>
              )}
              <div className="movie-modal__meta-row">
                <span className="movie-modal__meta-key">评价人数：</span>
                <span className="movie-modal__meta-val">{movie.reviews.toLocaleString()}人</span>
              </div>
            </div>

            {/* 电影详细信息区块（仿豆瓣详情页） */}
            {(movie.director || movie.writer || movie.cast || movie.language ||
              movie.releaseDate || movie.duration || movie.aka) && (
              <div className="movie-modal__info-block">
                {movie.director && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">导演：</span>
                    <span className="movie-modal__info-text">{movie.director}</span>
                  </div>
                )}
                {movie.writer && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">编剧：</span>
                    <span className="movie-modal__info-text">{movie.writer}</span>
                  </div>
                )}
                {movie.cast && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">主演：</span>
                    <span className="movie-modal__info-text">{movie.cast}</span>
                  </div>
                )}
                {movie.genres && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">类型：</span>
                    <span className="movie-modal__info-text">{movie.genres}</span>
                  </div>
                )}
                {movie.country && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">制片国家/地区：</span>
                    <span className="movie-modal__info-text">{movie.country}</span>
                  </div>
                )}
                {movie.language && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">语言：</span>
                    <span className="movie-modal__info-text">{movie.language}</span>
                  </div>
                )}
                {movie.releaseDate && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">上映日期：</span>
                    <span className="movie-modal__info-text">{movie.releaseDate}</span>
                  </div>
                )}
                {movie.duration && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">片长：</span>
                    <span className="movie-modal__info-text">{movie.duration}</span>
                  </div>
                )}
                {movie.aka && (
                  <div className="movie-modal__info-row">
                    <span className="movie-modal__info-label">又名：</span>
                    <span className="movie-modal__info-text">{movie.aka}</span>
                  </div>
                )}
              </div>
            )}

            {/* 剧情简介展示区域 */}
            {movie.summary ? (
              <div className="movie-modal__summary">
                <h4 className="movie-modal__summary-title">{movie.name}的剧情简介</h4>
                <p className="movie-modal__summary-text">{movie.summary}</p>
              </div>
            ) : (
              <div className="movie-modal__summary movie-modal__summary--empty">
                <p className="movie-modal__summary-empty">暂无剧情简介</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetailModal;
