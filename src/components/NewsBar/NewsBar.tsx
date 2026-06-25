import { useEffect, useRef, useState } from 'react';
import './NewsBar.less';

const newsItems = [
  '《哪吒之魔童降世》全球票房突破 60 亿，刷新中国动画电影新纪录！',
  '国产动画《深海》入围柏林电影节主竞赛单元，展现中国动画新高度',
  '2025年中国动画电影总票房突破200亿大关，同比增长35%',
  '追光动画新作《聊斋：兰若寺》定档暑期，开启东方神话新篇章',
  '光线彩条屋公布三年片单，12部动画作品蓄势待发',
];

const NewsBar: React.FC = () => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const [now, setNow] = useState(new Date());

  // 实时时间更新
  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const scroll = scrollRef.current;
    const content = contentRef.current;
    if (!scroll || !content) return;

    let animationId: number;
    let offset = 0;

    const animate = () => {
      offset -= 0.3;
      if (offset <= -content.scrollWidth / 2) {
        offset = 0;
      }
      if (scroll) {
        scroll.style.transform = `translateX(${offset}px)`;
      }
      animationId = requestAnimationFrame(animate);
    };

    // 复制一份内容实现无缝滚动
    const clone = content.cloneNode(true) as HTMLElement;
    scroll.appendChild(clone);

    animate();

    return () => {
      cancelAnimationFrame(animationId);
      if (clone.parentNode === scroll) {
        scroll.removeChild(clone);
      }
    };
  }, []);

  const timeStr = now.toLocaleString('zh-CN', {
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
  });

  return (
    <div className="news-bar">
      <div className="news-bar__icon">📰</div>
      <span className="news-bar__label">实时资讯</span>
      <div className="news-bar__scroll-wrapper">
        <div className="news-bar__scroll" ref={scrollRef}>
          <div className="news-bar__content" ref={contentRef}>
            {newsItems.map((item, index) => (
              <span className="news-bar__item" key={index}>{item}</span>
            ))}
          </div>
        </div>
      </div>
      <div className="news-bar__source">
        数据来源：和鲸社区 / 艺恩电影 / 国家电影局
      </div>
      {/* 时间在左，箭头在右 */}
      <span className="news-bar__time">{timeStr}</span>
      <span className="news-bar__arrow">→</span>
      <div className="news-bar__refresh">
        实时更新
      </div>
    </div>
  );
};

export default NewsBar;
