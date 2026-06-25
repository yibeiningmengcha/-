import { useState, useEffect } from 'react';
import './Header.less';

const Header: React.FC = () => {
  const [currentTime, setCurrentTime] = useState<string>('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      setCurrentTime(`${year}-${month}-${day} ${hours}:${minutes}:${seconds}`);
    };

    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="header">
      <h1 className="header__title">中国动画电影市场全景洞察大屏</h1>
      <div className="header__time">{currentTime}</div>
    </header>
  );
};

export default Header;
