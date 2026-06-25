# -*- coding: utf-8 -*-
"""
可视化图表模块
使用Pyecharts生成所有大屏图表
适配 Pyecharts 2.x 版本
"""

from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Scatter, Map
from pyecharts.globals import ThemeType
import pandas as pd
import numpy as np

# 主题色配置 - 深色科技风
COLORS = {
    'primary': '#00d4ff',      # 青色主色
    'secondary': '#0088ff',    # 蓝色辅助
    'accent': '#ff6b35',       # 橙色强调
    'purple': '#a855f7',       # 紫色
    'green': '#10b981',        # 绿色
}


def create_top10_bar_chart(top10_df):
    """
    B. 票房Top10横向条形图
    """
    if top10_df is None or len(top10_df) == 0:
        return None
    
    movies = top10_df['电影名称'].tolist()[::-1]  # 反转使最高票房在顶部
    box_office = [round(x, 2) for x in top10_df['票房_亿元'].tolist()[::-1]]
    
    bar = (
        Bar(init_opts=opts.InitOpts(
            theme=ThemeType.DARK,
            bg_color='transparent',
            width='100%',
            height='100%'
        ))
        .add_xaxis(movies)
        .add_yaxis(
            '',
            box_office,
            itemstyle_opts=opts.ItemStyleOpts(
                color='#00d4ff',
                opacity=0.8,
                border_color='#00d4ff',
                border_width=1
            ),
            label_opts=opts.LabelOpts(
                is_show=True,
                position='right',
                formatter='{c} 亿',
                color='#ffffff',
                font_size=11
            ),
            bar_width='60%'
        )
        .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_='average', name='平均值')]
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='票房Top10',
                pos_left='center',
                title_textstyle_opts=opts.TextStyleOpts(
                    color=COLORS['primary'],
                    font_size=16,
                    font_weight='bold'
                )
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    color='#8892b0',
                    rotate=30,
                    font_size=10
                ),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#233554')
                )
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(color='#8892b0'),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#233554')
                ),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#1e3a5f')
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger='axis',
                axis_pointer_type='shadow',
                background_color='rgba(0,20,40,0.9)',
                border_color=COLORS['primary'],
                textstyle_opts=opts.TextStyleOpts(color='#ffffff')
            )
        )
        .reversal_axis()
    )
    
    return bar


def create_rating_distribution_chart(rating_dist):
    """
    C. 豆瓣评分分布柱状图
    """
    if rating_dist is None or len(rating_dist) == 0:
        return None
    
    intervals = [str(x) for x in rating_dist['评分区间'].tolist()]
    counts = rating_dist['数量'].tolist()
    
    bar = (
        Bar(init_opts=opts.InitOpts(
            theme=ThemeType.DARK,
            bg_color='transparent',
            width='100%',
            height='100%'
        ))
        .add_xaxis(intervals)
        .add_yaxis(
            '电影数量',
            counts,
            itemstyle_opts=opts.ItemStyleOpts(
                color='#0088ff',
                opacity=0.85,
                border_color='#00d4ff',
                border_width=1
            ),
            label_opts=opts.LabelOpts(
                is_show=True,
                position='top',
                color='#ffffff',
                font_size=11
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='豆瓣评分分布',
                pos_left='center',
                title_textstyle_opts=opts.TextStyleOpts(
                    color=COLORS['primary'],
                    font_size=16,
                    font_weight='bold'
                )
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                name='评分区间',
                name_textstyle_opts=opts.TextStyleOpts(color='#8892b0'),
                axislabel_opts=opts.LabelOpts(color='#8892b0', font_size=10),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#233554')
                )
            ),
            yaxis_opts=opts.AxisOpts(
                name='数量',
                name_textstyle_opts=opts.TextStyleOpts(color='#8892b0'),
                axislabel_opts=opts.LabelOpts(color='#8892b0'),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#233554')
                ),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#1e3a5f')
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger='axis',
                background_color='rgba(0,20,40,0.9)',
                border_color=COLORS['primary'],
                textstyle_opts=opts.TextStyleOpts(color='#ffffff')
            )
        )
    )
    
    return bar


def create_country_map(country_dist):
    """
    D. 制片国家/地区世界地图热力分布
    使用Map展示世界地图上的影片分布
    """
    if country_dist is None or len(country_dist) == 0:
        return None
    
    # 国家名称映射到英文（pyecharts需要英文名称）
    country_name_map = {
        '中国大陆': 'China',
        '中国香港': 'China',
        '中国台湾': 'Taiwan',
        '美国': 'United States of America',
        '日本': 'Japan',
        '韩国': 'Korea',
        '法国': 'France',
        '英国': 'United Kingdom',
        '德国': 'Germany',
        '意大利': 'Italy',
        '西班牙': 'Spain',
        '加拿大': 'Canada',
        '澳大利亚': 'Australia',
        '俄罗斯': 'Russia',
        '印度': 'India',
        '巴西': 'Brazil',
        '墨西哥': 'Mexico',
        '泰国': 'Thailand',
        '新加坡': 'Singapore',
        '马来西亚': 'Malaysia',
        '印尼': 'Indonesia',
        '爱尔兰': 'Ireland',
        '比利时': 'Belgium',
        '荷兰': 'Netherlands',
        '瑞典': 'Sweden',
        '丹麦': 'Denmark',
        '挪威': 'Norway',
        '芬兰': 'Finland',
        '瑞士': 'Switzerland',
        '奥地利': 'Austria',
        '波兰': 'Poland',
        '捷克': 'Czech Republic',
        '匈牙利': 'Hungary',
        '新西兰': 'New Zealand',
        '阿根廷': 'Argentina',
        '南非': 'South Africa',
        '阿联酋': 'United Arab Emirates',
        '以色列': 'Israel',
        '土耳其': 'Turkey',
        '伊朗': 'Iran',
        '越南': 'Vietnam',
        '菲律宾': 'Philippines',
        '柬埔寨': 'Cambodia',
        '老挝': 'Laos',
        '缅甸': 'Myanmar',
    }
    
    data = []
    for _, row in country_dist.iterrows():
        country_cn = row['国家_地区']
        count = int(row['数量'])
        country_en = country_name_map.get(country_cn, country_cn)
        if country_en:  # 只添加能映射的国家
            data.append((country_en, count))
    
    if not data:
        return None
    
    # 创建地图（使用简化版API）
    map_chart = (
        Map(init_opts=opts.InitOpts(
            theme=ThemeType.DARK,
            bg_color='transparent',
            width='100%',
            height='100%'
        ))
        .add(
            '影片数量',
            data,
            'world',
            is_map_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='制片国家/地区热力分布',
                pos_left='center',
                pos_top='10',
                title_textstyle_opts=opts.TextStyleOpts(
                    color=COLORS['primary'],
                    font_size=18,
                    font_weight='bold'
                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                min_=int(min([d[1] for d in data])),
                max_=int(max([d[1] for d in data])),
                range_text=['高', '低'],
                range_color=[COLORS['secondary'], COLORS['primary'], '#ff6b6b'],
                textstyle_opts=opts.TextStyleOpts(color='#fff'),
                pos_left='left',
                pos_bottom='5%'
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger='item',
                background_color='rgba(0,20,40,0.95)',
                border_color=COLORS['primary'],
                formatter='{b}: {c} 部影片',
                textstyle_opts=opts.TextStyleOpts(color='#ffffff')
            )
        )
    )
    
    return map_chart


def create_scatter_rating_reviews(scatter_data):
    """
    E. 评分与评价人数关系气泡散点图
    """
    if scatter_data is None or len(scatter_data) == 0:
        return None
    
    # 准备散点数据 [[x, y], ...]
    scatter_xy = []
    for _, row in scatter_data.iterrows():
        scatter_xy.append([row['豆瓣评分'], row['评价人数_对数']])
    
    scatter = (
        Scatter(init_opts=opts.InitOpts(
            theme=ThemeType.DARK,
            bg_color='transparent',
            width='100%',
            height='100%'
        ))
        .add_xaxis(axis_opts=opts.AxisOpts(
            name='豆瓣评分（分）',
            name_textstyle_opts=opts.TextStyleOpts(color='#8892b0'),
            axislabel_opts=opts.LabelOpts(color='#8892b0'),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color='#233554')
            ),
            splitline_opts=opts.SplitLineOpts(
                linestyle_opts=opts.LineStyleOpts(color='#1e3a5f')
            )
        ))
        .add_yaxis(
            '',
            scatter_xy,
            symbol_size=12,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color='#a855f7',
                opacity=0.7,
                border_color='#a855f7',
                border_width=1
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='评分与评价人数关系',
                pos_left='center',
                title_textstyle_opts=opts.TextStyleOpts(
                    color=COLORS['primary'],
                    font_size=16,
                    font_weight='bold'
                )
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(
                trigger='item',
                background_color='rgba(0,20,40,0.95)',
                border_color=COLORS['purple'],
                textstyle_opts=opts.TextStyleOpts(color='#ffffff')
            ),
            yaxis_opts=opts.AxisOpts(
                name='评价人数（对数）',
                name_textstyle_opts=opts.TextStyleOpts(color='#8892b0'),
                axislabel_opts=opts.LabelOpts(color='#8892b0'),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#233554')
                ),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color='#1e3a5f')
                )
            )
        )
    )
    
    return scatter


def create_genre_pie_chart(genre_dist):
    """
    F. 电影类型占比环形饼图
    """
    if genre_dist is None or len(genre_dist) == 0:
        return None
    
    genres = genre_dist['类型'].tolist()
    counts = genre_dist['数量'].tolist()
    
    pie_colors = [
        '#00d4ff', '#0088ff', '#a855f7', '#ff6b6b',
        '#f59e0b', '#10b981', '#ec4899', '#06b6d4', '#8b5cf6'
    ]
    
    pie = (
        Pie(init_opts=opts.InitOpts(
            theme=ThemeType.DARK,
            bg_color='transparent',
            width='100%',
            height='100%'
        ))
        .add(
            '',
            [list(z) for z in zip(genres, counts)],
            radius=['35%', '65%'],
            center=['50%', '55%'],
            label_opts=opts.LabelOpts(
                formatter='{b}\n{d}%',
                color='#ffffff',
                font_size=11
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                border_color='#0a1628',
                border_width=2
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title='电影类型占比',
                pos_left='center',
                title_textstyle_opts=opts.TextStyleOpts(
                    color=COLORS['primary'],
                    font_size=16,
                    font_weight='bold'
                )
            ),
            legend_opts=opts.LegendOpts(
                orient='vertical',
                pos_right='5%',
                pos_top='center',
                textstyle_opts=opts.TextStyleOpts(color='#8892b0', font_size=10),
                item_gap=8
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger='item',
                background_color='rgba(0,20,40,0.95)',
                border_color=COLORS['primary'],
                formatter='<b>{b}</b>: {c}部 ({d}%)',
                textstyle_opts=opts.TextStyleOpts(color='#ffffff')
            )
        )
        .set_series_opts(
            itemstyle_opts=opts.ItemStyleOpts(opacity=0.85)
        )
    )
    
    return pie
