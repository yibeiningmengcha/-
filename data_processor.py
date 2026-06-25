# -*- coding: utf-8 -*-
"""
数据加载与清洗模块
处理豆瓣电影数据和艺恩票房数据
"""

import pandas as pd
import numpy as np
import os

# 数据文件路径
BASE_DIR = r'e:\数据大屏\豆瓣电影大屏2'
DOUBAN_FILE = os.path.join(BASE_DIR, '豆瓣电影详情参数采集_1.xlsx')
YIEN_FILE = os.path.join(BASE_DIR, '艺恩-数据智能服务商_影片资料库.xlsx')


def load_douban_data():
    """
    4.1 读取豆瓣电影数据集
    使用pandas的read_excel()函数读取豆瓣影视数据文件
    """
    print(f"正在读取豆瓣数据: {DOUBAN_FILE}")
    df = pd.read_excel(DOUBAN_FILE)
    print(f"豆瓣数据读取成功，共 {len(df)} 条记录")
    return df


def load_yien_data():
    """
    4.1 读取艺恩票房数据集
    使用pandas的read_excel()函数读取艺恩票房数据文件
    """
    print(f"正在读取艺恩数据: {YIEN_FILE}")
    df = pd.read_excel(YIEN_FILE)
    print(f"艺恩数据读取成功，共 {len(df)} 条记录")
    return df


def explore_data(df, name="数据集"):
    """
    4.2 初步了解数据特征
    1. 使用info()方法查看数据总行数、列数、每列数据类型、非空值数量
    2. 使用describe()方法查看数值型字段的统计描述信息
    """
    print(f"\n{'='*50}")
    print(f"【{name}】数据探索")
    print(f"{'='*50}")
    
    print("\n--- 基本信息 (info) ---")
    df.info()
    
    print("\n--- 数值型字段统计描述 (describe) ---")
    print(df.describe())
    
    return df


def check_missing_values(df):
    """
    4.3.1 缺失值处理
    1. 使用isnull().sum()检查每列的缺失情况
    返回缺失值统计
    """
    print("\n--- 缺失值检查 ---")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        '缺失数量': missing,
        '缺失比例(%)': missing_pct
    })
    missing_df = missing_df[missing_df['缺失数量'] > 0]
    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("无缺失值")
    return missing_df


def check_duplicates(df):
    """
    4.3.2 重复值处理
    使用duplicated().sum()检查是否存在完全重复的行
    返回去重后的DataFrame和删除的行数
    """
    print("\n--- 重复值检查 ---")
    dup_count = df.duplicated().sum()
    print(f"完全重复行数: {dup_count}")
    if dup_count > 0:
        df_cleaned = df.drop_duplicates()
        print(f"已删除 {dup_count} 行重复数据，剩余 {len(df_cleaned)} 行")
        return df_cleaned, dup_count
    return df, 0


def clean_box_office(value):
    """
    4.3.3 格式标准化 - 票房清洗
    将 "￥503502万" 格式转换为纯数字（万元）
    """
    if pd.isna(value):
        return np.nan
    
    value_str = str(value)
    # 移除￥符号
    value_str = value_str.replace('￥', '').replace(' ', '')
    # 移除"万"并转换为数字
    if '万' in value_str:
        value_str = value_str.replace('万', '')
        try:
            return float(value_str)
        except ValueError:
            return np.nan
    try:
        return float(value_str)
    except ValueError:
        return np.nan


def preprocess_yien_data(df):
    """
    艺恩数据预处理：
    1. 清洗票房字段为纯数字
    2. 处理缺失值
    3. 去重
    """
    print("\n=== 艺恩数据预处理 ===")
    
    # 清洗票房
    df['票房_万元'] = df['电影票房'].apply(clean_box_office)
    df['票房_亿元'] = df['票房_万元'] / 10000
    
    # 检查缺失
    missing = check_missing_values(df)
    
    # 删除票房缺失的数据
    before_count = len(df)
    df = df.dropna(subset=['票房_万元', '电影名称'])
    after_count = len(df)
    if before_count > after_count:
        print(f"删除票房/名称缺失数据 {before_count - after_count} 条")
    
    # 去重
    df, dup_count = check_duplicates(df)
    
    print(f"艺恩数据预处理完成，有效数据 {len(df)} 条")
    return df


def preprocess_douban_data(df):
    """
    豆瓣数据预处理：
    1. 处理缺失值
    2. 去重
    3. 确保关键字段格式正确
    """
    print("\n=== 豆瓣数据预处理 ===")
    
    # 检查缺失
    check_missing_values(df)
    
    # 删除关键字段缺失的数据
    before_count = len(df)
    df = df.dropna(subset=['电影名称', '豆瓣评分'])
    after_count = len(df)
    if before_count > after_count:
        print(f"删除关键缺失数据 {before_count - after_count} 条")
    
    # 去重
    df, dup_count = check_duplicates(df)
    
    # 确保评分为数值类型（使用copy避免SettingWithCopyWarning）
    df = df.copy()
    df['豆瓣评分'] = pd.to_numeric(df['豆瓣评分'], errors='coerce')
    df['评价人数'] = pd.to_numeric(df['评价人数'], errors='coerce')
    
    print(f"豆瓣数据预处理完成，有效数据 {len(df)} 条")
    return df


def load_and_process_all():
    """
    统一的数据加载和清洗函数
    返回清洗后的两个DataFrame
    """
    # 加载数据
    df_douban = load_douban_data()
    df_yien = load_yien_data()
    
    # 探索数据
    explore_data(df_douban, "豆瓣电影数据")
    explore_data(df_yien, "艺恩票房数据")
    
    # 预处理
    df_douban_clean = preprocess_douban_data(df_douban)
    df_yien_clean = preprocess_yien_data(df_yien)
    
    return df_douban_clean, df_yien_clean


# ==================== 图表数据聚合函数 ====================

def get_kpi_metrics(df_douban, df_yien):
    """
    A. 顶部4个KPI指标卡
    - 总电影数：df_douban中去重的电影名称数量
    - 总票房：df_yie清洗后的电影票房求和（单位：亿元）
    - 平均评分：df_douban中豆瓣评分的平均值
    - 最高票房：从df_yie中找到票房最高的电影及数值
    """
    metrics = {}
    
    # 总电影数
    metrics['总电影数'] = df_douban['电影名称'].nunique()
    
    # 总票房（亿元）
    total_box_office = df_yien['票房_亿元'].sum()
    metrics['总票房_亿元'] = round(total_box_office, 2)
    
    # 平均评分
    metrics['平均评分'] = round(df_douban['豆瓣评分'].mean(), 1)
    
    # 最高票房
    if len(df_yien) > 0:
        top_movie_idx = df_yien['票房_万元'].idxmax()
        metrics['最高票房_电影'] = df_yien.loc[top_movie_idx, '电影名称']
        metrics['最高票房_数值'] = round(df_yien.loc[top_movie_idx, '票房_亿元'], 2)
    else:
        metrics['最高票房_电影'] = '暂无数据'
        metrics['最高票房_数值'] = 0
    
    return metrics


def get_top10_box_office(df_yien):
    """
    B. 票房Top10（横向条形图）
    将df_yie的电影票房按从高到低排序，取前10名
    """
    top10 = df_yien.nlargest(10, '票房_万元')[['电影名称', '票房_亿元']].copy()
    top10 = top10.sort_values('票房_亿元', ascending=True)  # 横向条形图需要升序
    return top10


def get_rating_distribution(df_douban):
    """
    C. 豆瓣评分分布（柱状图）
    提取豆瓣评分，划分区间统计每个区间的电影数量
    """
    # 定义评分区间
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    labels = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']
    
    df_douban_copy = df_douban.copy()
    df_douban_copy['评分区间'] = pd.cut(df_douban_copy['豆瓣评分'], bins=bins, labels=labels, include_lowest=True)
    
    distribution = df_douban_copy.groupby('评分区间', observed=True).size().reset_index(name='数量')
    distribution = distribution.dropna()
    
    return distribution


def get_country_distribution(df_douban):
    """
    D. 制片国家/地区热力分布
    提取制片国家_地区，按"/"切割后分别计数统计
    """
    countries = []
    
    for countries_str in df_douban['制片国家_地区'].dropna():
        # 按 "/" 或 " / " 分割
        parts = str(countries_str).replace(' ', '').split('/')
        for part in parts:
            if part.strip():
                countries.append(part.strip())
    
    country_counts = pd.Series(countries).value_counts().reset_index()
    country_counts.columns = ['国家_地区', '数量']
    
    return country_counts


def get_rating_vs_reviews_scatter(df_douban):
    """
    E. 评分与评价人数关系（气泡散点图）
    X轴：豆瓣评分
    Y轴：评价人数
    气泡大小：评价人数
    """
    scatter_data = df_douban[['电影名称', '豆瓣评分', '评价人数']].dropna().copy()
    scatter_data = scatter_data[scatter_data['评价人数'] > 0]
    
    # 对评价人数取对数（因为差异太大）
    scatter_data['评价人数_对数'] = np.log10(scatter_data['评价人数'] + 1)
    
    # 取前100个高评价人数的点避免过于拥挤
    scatter_data = scatter_data.nlargest(100, '评价人数')
    
    return scatter_data


def get_genre_distribution(df_douban):
    """
    F. 电影类型占比（环形饼图）
    提取类型字段，按"/"切割后统计各类型出现频次
    """
    genres = []
    
    for genre_str in df_douban['类型'].dropna():
        parts = str(genre_str).replace(' ', '').split('/')
        for part in parts:
            if part.strip():
                genres.append(part.strip())
    
    genre_counts = pd.Series(genres).value_counts().reset_index()
    genre_counts.columns = ['类型', '数量']
    genre_counts['占比'] = (genre_counts['数量'] / genre_counts['数量'].sum() * 100).round(1)
    
    # 取前8个主要类型，其余合并为"其他"
    if len(genre_counts) > 8:
        top_genres = genre_counts.head(8).copy()
        other_count = genre_counts.iloc[8:]['数量'].sum()
        other_pct = genre_counts.iloc[8:]['占比'].sum()
        top_genres = pd.concat([
            top_genres,
            pd.DataFrame({'类型': ['其他'], '数量': [other_count], '占比': [round(other_pct, 1)]})
        ], ignore_index=True)
        genre_counts = top_genres
    
    return genre_counts


if __name__ == '__main__':
    # 测试数据处理流程
    df_db, df_yi = load_and_process_all()
    
    print("\n\n========== KPI指标测试 ==========")
    kpi = get_kpi_metrics(df_db, df_yi)
    print(kpi)
    
    print("\n\n========== 票房Top10测试 ==========")
    top10 = get_top10_box_office(df_yi)
    print(top10)
    
    print("\n\n========== 评分分布测试 ==========")
    rating_dist = get_rating_distribution(df_db)
    print(rating_dist)
    
    print("\n\n========== 国家分布测试 ==========")
    country_dist = get_country_distribution(df_db)
    print(country_dist.head(15))
    
    print("\n\n========== 类型分布测试 ==========")
    genre_dist = get_genre_distribution(df_db)
    print(genre_dist)
