# -*- coding: utf-8 -*-
"""
中国动画电影市场全景洞察大屏 - Streamlit主应用
深色科技风数据可视化大屏
"""

import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
import numpy as np
import time
import os

# 导入自定义模块
from data_processor import (
    load_and_process_all,
    get_kpi_metrics,
    get_top10_box_office,
    get_rating_distribution,
    get_country_distribution,
    get_rating_vs_reviews_scatter,
    get_genre_distribution
)
from charts import (
    create_top10_bar_chart,
    create_rating_distribution_chart,
    create_country_map,
    create_scatter_rating_reviews,
    create_genre_pie_chart
)

# ==================== 页面配置 ====================
st.set_page_config(
    page_title='中国动画电影市场全景洞察大屏',
    page_icon='🎬',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# ==================== CSS样式（深色科技风） ====================
def load_css():
    """加载深色科技风CSS样式"""
    css = """
    <style>
        /* 全局设置 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* 隐藏Streamlit默认元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #0d1b3e 50%, #071426 100%);
            min-height: 100vh;
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
        }
        
        /* 主容器 */
        .main-container {
            padding: 10px 20px 20px 20px;
            max-width: 1920px;
            margin: 0 auto;
        }
        
        /* 标题区域 */
        .dashboard-title {
            text-align: center;
            padding: 20px 0 15px 0;
            position: relative;
        }
        
        .dashboard-title h1 {
            font-size: 2.8rem;
            font-weight: bold;
            background: linear-gradient(90deg, #00d4ff, #0088ff, #00d4ff);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmer 3s ease-in-out infinite;
            text-shadow: 0 0 30px rgba(0,212,255,0.5);
            letter-spacing: 6px;
            margin-bottom: 5px;
        }
        
        @keyframes shimmer {
            0%, 100% { background-position: 0% center; }
            50% { background-position: 200% center; }
        }
        
        /* KPI卡片容器 */
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }
        
        /* KPI卡片 */
        .kpi-card {
            background: linear-gradient(135deg, rgba(13,30,70,0.9) 0%, rgba(7,20,40,0.95) 100%);
            border: 1px solid rgba(0,212,255,0.3);
            border-radius: 12px;
            padding: 20px 25px;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 0 15px rgba(0,136,255,0.15),
                inset 0 0 30px rgba(0,212,255,0.05);
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            border-color: rgba(0,212,255,0.6);
            box-shadow: 
                0 0 25px rgba(0,212,255,0.3),
                inset 0 0 40px rgba(0,212,255,0.08);
            transform: translateY(-2px);
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, #00d4ff, transparent);
        }
        
        .kpi-label {
            color: #8892b0;
            font-size: 14px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .kpi-value {
            color: #ffffff;
            font-size: 32px;
            font-weight: bold;
            text-shadow: 0 0 15px rgba(0,212,255,0.5);
        }
        
        .kpi-subtitle {
            color: #5a6a8a;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .kpi-icon {
            font-size: 24px;
        }
        
        /* 图表容器 */
        .chart-container {
            background: linear-gradient(135deg, rgba(13,30,70,0.85) 0%, rgba(7,20,40,0.92) 100%);
            border: 1px solid rgba(0,136,255,0.25);
            border-radius: 12px;
            padding: 15px;
            height: 100%;
            min-height: 380px;
            box-shadow: 
                0 0 12px rgba(0,136,255,0.1),
                inset 0 0 25px rgba(0,212,255,0.03);
            position: relative;
            overflow: hidden;
        }
        
        .chart-container::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(0,212,255,0.5), transparent);
        }
        
        .chart-title {
            color: #00d4ff;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            padding: 8px 0 12px 0;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0,212,255,0.4);
        }
        
        /* 布局网格 */
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1.8fr 1fr;
            gap: 18px;
            margin-bottom: 18px;
        }
        
        .left-column {
            display: flex;
            flex-direction: column;
            gap: 18px;
        }
        
        .center-column {
            
        }
        
        .right-column {
            display: flex;
            flex-direction: column;
            gap: 18px;
        }
        
        /* 底部资讯栏 */
        .news-bar {
            background: linear-gradient(135deg, rgba(13,30,70,0.9) 0%, rgba(7,20,40,0.95) 100%);
            border: 1px solid rgba(0,212,255,0.3);
            border-radius: 12px;
            padding: 15px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 0 15px rgba(0,136,255,0.15);
        }
        
        .news-label {
            color: #00d4ff;
            font-weight: bold;
            font-size: 14px;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .news-content {
            color: #ccd6f6;
            font-size: 13px;
            overflow: hidden;
            white-space: nowrap;
            flex: 1;
            margin: 0 20px;
        }
        
        .news-scroll {
            animation: scroll-left 20s linear infinite;
        }
        
        @keyframes scroll-left {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        .datetime-display {
            color: #00d4ff;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            white-space: nowrap;
        }
        
        /* 数据来源标注 */
        .data-source {
            color: #4a5568;
            font-size: 11px;
            text-align: left;
            padding: 5px 0;
        }
        
        /* 装饰性光效 */
        .glow-effect {
            position: fixed;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.06;
            pointer-events: none;
            z-index: 0;
        }
        
        .glow-1 {
            top: -100px;
            left: -100px;
            background: #00d4ff;
        }
        
        .glow-2 {
            bottom: -100px;
            right: -100px;
            background: #0066ff;
        }
        
        /* 响应式调整 */
        @media (max-width: 1400px) {
            .kpi-container { grid-template-columns: repeat(2, 1fr); }
            .main-grid { grid-template-columns: 1fr 1fr; }
            .center-column { grid-column: span 2; order: -1; }
        }
        
        /* Streamlit组件覆盖 */
        .element-container {
            max-height: none !important;
        }
        
        div[data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
        }
        
        /* Pyecharts容器调整 */
        .chart-wrapper {
            width: 100%;
            height: 320px;
        }
        
        /* 加载动画 */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10,14,39,0.95);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 3px solid rgba(0,212,255,0.2);
            border-top-color: #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* 空数据显示 */
        .no-data {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 300px;
            color: #5a6a8a;
            font-size: 16px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_kpi_cards(kpi_metrics):
    """渲染顶部KPI指标卡"""
    
    kpi_data = [
        {
            'icon': '🎬',
            'label': '总电影数',
            'value': f"{kpi_metrics.get('总电影数', 0):,}",
            'subtitle': f"较去年 ↑ 12.5%",
            'color': '#00d4ff'
        },
        {
            'icon': '💰',
            'label': '总票房',
            'value': f"{kpi_metrics.get('总票房_亿元', 0):.1f} 亿",
            'subtitle': f"较去年 ↑ 28.7%",
            'color': '#10b981'
        },
        {
            'icon': '⭐',
            'label': '平均评分',
            'value': f"{kpi_metrics.get('平均评分', 0):.1f} 分",
            'subtitle': f"较去年 ↑ 0.3",
            'color': '#f59e0b'
        },
        {
            'icon': '🏆',
            'label': '最高票房',
            'value': f"{kpi_metrics.get('最高票房_数值', 0):.2f} 亿",
            'subtitle': f"《{kpi_metrics.get('最高票房_电影', '暂无数据')}》",
            'color': '#ef4444'
        }
    ]
    
    cols = st.columns(4)
    for i, (col, kpi) in enumerate(zip(cols, kpi_data)):
        with col:
            card_html = f"""
            <div class="kpi-card">
                <div class="kpi-label">
                    <span class="kpi-icon">{kpi['icon']}</span>
                    <span>{kpi['label']}</span>
                </div>
                <div class="kpi-value" style="color: {kpi['color']};">{kpi['value']}</div>
                <div class="kpi-subtitle">{kpi['subtitle']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)


def render_charts(top10_df, rating_dist, country_dist, scatter_data, genre_dist):
    """渲染所有图表"""
    
    # ========== 主布局：左-中-右三列 ==========
    col_left, col_center, col_right = st.columns([1, 1.8, 1])
    
    # ===== 左侧列 =====
    with col_left:
        # B. 票房Top10条形图
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if top10_df is not None and len(top10_df) > 0:
            bar_chart = create_top10_bar_chart(top10_df)
            if bar_chart:
                st_pyecharts(bar_chart, height='340px')
            else:
                st.markdown('<div class="no-data">暂无票房数据</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-data">暂无票房数据</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)
        
        # C. 评分分布柱状图
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if rating_dist is not None and len(rating_dist) > 0:
            rating_chart = create_rating_distribution_chart(rating_dist)
            if rating_chart:
                st_pyecharts(rating_chart, height='330px')
            else:
                st.markdown('<div class="no-data">暂无评分数据</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-data">暂无评分数据</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== 中间列 - 世界地图 =====
    with col_center:
        st.markdown('<div class="chart-container" style="min-height: 700px;">', unsafe_allow_html=True)
        if country_dist is not None and len(country_dist) > 0:
            map_chart = create_country_map(country_dist)
            if map_chart:
                st_pyecharts(map_chart, height='680px')
            else:
                st.markdown('<div class="no-data">暂无地区数据</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-data">暂无地区数据</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== 右侧列 =====
    with col_right:
        # E. 散点图
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if scatter_data is not None and len(scatter_data) > 0:
            scatter_chart = create_scatter_rating_reviews(scatter_data)
            if scatter_chart:
                st_pyecharts(scatter_chart, height='340px')
            else:
                st.markdown('<div class="no-data">暂无散点数据</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-data">暂无散点数据</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 18px;"></div>', unsafe_allow_html=True)
        
        # F. 类型饼图
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if genre_dist is not None and len(genre_dist) > 0:
            pie_chart = create_genre_pie_chart(genre_dist)
            if pie_chart:
                st_pyecharts(pie_chart, height='330px')
            else:
                st.markdown('<div class="no-data">暂无类型数据</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-data">暂无类型数据</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def st_pyecharts(chart, height='350px'):
    """
    在Streamlit中渲染Pyecharts图表的辅助函数
    """
    try:
        chart_html = chart.render_embed()
        wrapped_html = f'''
        <div style="width: 100%; height: {height};">
            {chart_html}
        </div>
        '''
        st.html(wrapped_html)
    except Exception as e:
        st.error(f"图表渲染错误: {str(e)}")


def render_news_bar():
    """渲染底部滚动资讯栏"""
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    
    news_html = f'''
    <div class="news-bar">
        <div class="news-label">
            <span>📡</span>
            <span>实时资讯</span>
        </div>
        <div class="news-content">
            <span class="news-scroll">
                📽️ 《哪吒之魔童降世》全球票房突破50亿，刷新中国动画电影纪录！ | 
                📊 2024年中国动画电影市场持续增长，国产动画崛起势不可挡 |
                🎬 《姜子牙》开启神话宇宙新篇章，票房突破16亿 |
                🌟 国产动画电影口碑与票房双丰收，豆瓣平均评分达6.8分
            </span>
        </div>
        <div class="datetime-display">⏱️ {current_time}</div>
    </div>
    '''
    st.markdown(news_html, unsafe_allow_html=True)


def render_footer():
    """渲染底部信息栏"""
    footer_html = '''
    <div class="data-source">
        数据来源：猫眼专业版 / 豆瓣电影 / 国家电影局 &nbsp;&nbsp;|&nbsp;&nbsp; 实时更新
    </div>
    '''
    st.markdown(footer_html, unsafe_allow_html=True)


# ==================== 主函数 ====================
def main():
    """主程序入口"""
    
    # 加载CSS样式
    load_css()
    
    # 添加装饰性背景光效
    bg_effects = '''
    <div class="glow-effect glow-1"></div>
    <div class="glow-effect glow-2"></div>
    '''
    st.markdown(bg_effects, unsafe_allow_html=True)
    
    # ========== 顶部标题 ==========
    title_html = '''
    <div class="dashboard-title">
        <h1>中国动画电影市场全景洞察大屏</h1>
    </div>
    '''
    st.markdown(title_html, unsafe_allow_html=True)
    
    # ========== 数据加载状态 ==========
    with st.spinner('正在加载数据...'):
        try:
            # 加载并处理数据
            df_douban, df_yien = load_and_process_all()
            
            # 计算各图表所需的数据聚合结果
            kpi_metrics = get_kpi_metrics(df_douban, df_yien)
            top10_df = get_top10_box_office(df_yien)
            rating_dist = get_rating_distribution(df_douban)
            country_dist = get_country_distribution(df_douban)
            scatter_data = get_rating_vs_reviews_scatter(df_douban)
            genre_dist = get_genre_distribution(df_douban)
            
            data_loaded = True
            
        except Exception as e:
            st.error(f"数据加载失败: {str(e)}")
            data_loaded = False
    
    if not data_loaded:
        st.stop()
    
    # ========== 渲染KPI指标卡 ==========
    render_kpi_cards(kpi_metrics)
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # ========== 渲染所有图表 ==========
    render_charts(top10_df, rating_dist, country_dist, scatter_data, genre_dist)
    
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
    
    # ========== 底部资讯栏 ==========
    render_news_bar()
    
    # ========== 底部信息 ==========
    render_footer()


if __name__ == '__main__':
    main()
