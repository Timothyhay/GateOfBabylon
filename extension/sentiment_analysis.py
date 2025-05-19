from collections import Counter

import jieba
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, ttest_ind
from snownlp import SnowNLP
from wordcloud import WordCloud
from matplotlib.font_manager import FontProperties

combined_data_path = "../data/notion_combined_data.csv"
combined_data_df = pd.read_csv(combined_data_path)

matplotlib.use('TkAgg')

# 描述性统计
print(combined_data_df.info())  # 检查缺失值和数据类型
print(combined_data_df[['Mood', 'OutsideHour']].describe())


# 设置全局字体和风格
plt.rcParams['font.family'] = 'DengXian'
# plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']  # Arial 优先用于英文，SimHei 用于中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = '#E5E7EB'  # 淡灰色网格线
plt.rcParams['grid.alpha'] = 0.5


# 定义马卡龙色系
MOOD_COLOR = '#A2CFFE'  # 淡蓝色
MOOD_DEEPER_COLOR = '#3D9DDE'
# SCORE_COLOR = '#C3E8BD'  # 柔和薄荷绿（score）
SCORE_COLOR = '#FECDD3'  # 柔和粉色
OUTSIDEHOUR_COLOR = '#B5EAD7'  # 淡绿色
OUTSIDEHOUR_DEEPER_COLOR = '#36C496'
MEAN_COLOR = '#FF9999'  # 粉红色（平均值）
MA_COLOR = '#6B7280'  # 灰蓝色（滑动平均）

# 图1：Mood and OutsideHour Over Weeks（双 Y 轴）
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制 Mood（左 Y 轴，范围 0~5）
ax1.plot(combined_data_df['Week'], combined_data_df['Mood'], label='Mood', marker='o', color=MOOD_COLOR)
ax1.set_xlabel('Week')
ax1.set_ylabel('Mood', color=MOOD_DEEPER_COLOR)
ax1.tick_params(axis='y', labelcolor=MOOD_DEEPER_COLOR)
ax1.set_ylim(0, 5)  # Mood 范围固定为 0~5

# 创建第二个 Y 轴用于 OutsideHour
ax2 = ax1.twinx()
ax2.plot(combined_data_df['Week'], combined_data_df['OutsideHour'], label='OutsideHour', marker='x', color=OUTSIDEHOUR_COLOR)
ax2.set_ylabel('OutsideHour', color=OUTSIDEHOUR_DEEPER_COLOR)
ax2.tick_params(axis='y', labelcolor=OUTSIDEHOUR_DEEPER_COLOR)
ax2.set_ylim(0, combined_data_df['OutsideHour'].max() + 1)

# 添加图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='#F9FAFB')

plt.title('Mood and OutsideHour Over Weeks')
plt.tight_layout()
plt.show()

# 图2：Mood & OutsideHour Distribution（标注平均值）
plt.figure(figsize=(12, 5))

# Mood 分布
plt.subplot(1, 2, 1)
sns.histplot(combined_data_df['Mood'], kde=True, color=MOOD_COLOR)
plt.title('Mood Distribution')
mood_mean = combined_data_df['Mood'].mean()
plt.axvline(mood_mean, color=MEAN_COLOR, linestyle='--', label=f'Mean: {mood_mean:.2f}')
plt.legend(frameon=True, facecolor='#F9FAFB')

# OutsideHour 分布
plt.subplot(1, 2, 2)
sns.histplot(combined_data_df['OutsideHour'], kde=True, color=OUTSIDEHOUR_COLOR)
plt.title('OutsideHour Distribution')
outsidehour_mean = combined_data_df['OutsideHour'].mean()
plt.axvline(outsidehour_mean, color=MEAN_COLOR, linestyle='--', label=f'Mean: {outsidehour_mean:.2f}')
plt.legend(frameon=True, facecolor='#F9FAFB')

plt.tight_layout()
plt.show()

# 图3：Mood Moving Average（更大窗口以更平滑）
window_size = 5  # 窗口大小为 5
combined_data_df['Mood_MA'] = combined_data_df['Mood'].rolling(window=window_size, min_periods=1).mean()
plt.figure(figsize=(10, 6))
plt.plot(combined_data_df['Week'], combined_data_df['Mood_MA'], label='Mood Moving Average', marker='o', color=MA_COLOR)
plt.xlabel('Week')
plt.ylabel('Mood')
plt.title('Mood Moving Average (Window=5)')
plt.legend(frameon=True, facecolor='#F9FAFB')
plt.tight_layout()
plt.show()


# 相关性分析

sns.scatterplot(x='OutsideHour', y='Mood', data=combined_data_df, color=MOOD_COLOR)
plt.title('Mood and OutsideHour Scatter')
plt.show()

# 图4：相关系数热图（Pearson 和 Spearman）
plt.figure(figsize=(8, 6))
# 计算 Pearson 相关系数
pearson_corr = combined_data_df[['Week', 'Mood', 'Score', 'OutsideHour']].corr(method='pearson')
# 创建自定义马卡龙色系渐变
colors = sns.color_palette([MOOD_COLOR, '#F9FAFB', OUTSIDEHOUR_COLOR])
cmap = sns.blend_palette(colors, as_cmap=True)
sns.heatmap(pearson_corr, annot=True, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, cbar_kws={'label': 'Pearson Correlation'})
plt.title('Pearson Correlation Matrix')
plt.tight_layout()
plt.show()
print('Pearson Correlation Matrix')
print(pearson_corr)

# 打印 Spearman 相关系数（供参考）
plt.figure(figsize=(8, 6))
spearman_corr, _ = spearmanr(combined_data_df[['Week', 'Mood', 'OutsideHour']])
spearman_df = pd.DataFrame(
    spearman_corr,
    columns=['Week', 'Mood', 'OutsideHour'],
    index=['Week', 'Mood', 'OutsideHour']
)
sns.heatmap(spearman_df, annot=True, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, cbar_kws={'label': 'Spearman Correlation'})
plt.title('Spearman Correlation Matrix')
plt.tight_layout()
plt.show()

# 打印 Spearman 相关系数（供参考）
print("Spearman Correlation Matrix:")
print(spearman_df)



# 图6：关键字频率（柱状图）
words = [word for desc in combined_data_df['Description'] for word in jieba.cut(desc) if len(word) > 1]
word_counts = Counter(words).most_common(10)
words, counts = zip(*word_counts)
plt.figure(figsize=(10, 6))
sns.barplot(x=list(counts), y=list(words), color=MOOD_COLOR)
plt.title('Top 10 Keywords in Description')
plt.xlabel('Frequency')
plt.ylabel('Keyword')
plt.tight_layout()
plt.show()

# 图7：关键字词云
stopwords = {'今天', '感觉', '还是', '没有', '这种', '一下', '这么', '这个'}
words = [word for desc in combined_data_df['Description'] for word in jieba.cut(desc) if len(word) > 1 and word not in stopwords]
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white', max_words=30, min_font_size=2,
                     colormap='Blues').generate(' '.join(words))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Description Word Cloud')
plt.tight_layout()
plt.show()

# 图8：Sentiment vs. Mood 散点图（基于 SnowNLP）
combined_data_df['Sentiment'] = combined_data_df['Description'].apply(lambda x: SnowNLP(x).sentiments)
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Sentiment', y='Mood', data=combined_data_df, color=MOOD_COLOR)
plt.title('SnowNLP Sentiment vs. Mood')
plt.xlabel('SnowNLP Sentiment (0–1)')
plt.ylabel('Mood (0–5)')
plt.tight_layout()
plt.show()

# 图9：Mood by Weather
weather_keywords = ['雨', '晴', '阴', '雪']
activity_keywords = ['散步', '运动', '工作', '学习']
combined_data_df['Weather'] = combined_data_df['Description'].apply(
    lambda x: next((w for w in weather_keywords if w in x), 'Other'))
plt.figure(figsize=(10, 6))
sns.boxplot(x='Weather', y='Mood', data=combined_data_df, palette=[MOOD_COLOR, OUTSIDEHOUR_COLOR, MEAN_COLOR, MA_COLOR])
plt.title('Mood by Weather Keywords')
plt.tight_layout()
plt.show()

# 图10：Mood by Activity
combined_data_df['Activity'] = combined_data_df['Description'].apply(
    lambda x: next((a for a in activity_keywords if a in x), 'Other'))
plt.figure(figsize=(10, 6))
sns.boxplot(x='Activity', y='Mood', data=combined_data_df, palette=[MOOD_COLOR, OUTSIDEHOUR_COLOR, MEAN_COLOR, MA_COLOR])
plt.title('Mood by Activity Keywords')
plt.tight_layout()
plt.show()

# 图11：Score vs. Mood 散点图
plt.figure(figsize=(8, 6))
sns.regplot(x='Score', y='Mood', data=combined_data_df, color=SCORE_COLOR, line_kws={'color': MEAN_COLOR, 'label': 'Regression'})
plt.plot([0, 5], [0, 5], color=MEAN_COLOR, linestyle='--', label='Perfect Agreement')
# 计算回归方程
slope, intercept = np.polyfit(combined_data_df['Score'], combined_data_df['Mood'], 1)
plt.text(0.5, 4.5, f'y = {slope:.2f}x + {intercept:.2f}', color=MEAN_COLOR)
plt.title('Score vs. Mood')
plt.xlabel('Score (0–5)')
plt.ylabel('Mood (0–5)')
plt.legend(frameon=True, facecolor='#F9FAFB')
plt.tight_layout()
plt.show()


# 图12：Bland-Altman 散点图
combined_data_df['Score_Mood_Diff'] = combined_data_df['Score'] - combined_data_df['Mood']
mean_diff = combined_data_df['Score_Mood_Diff'].mean()
std_diff = combined_data_df['Score_Mood_Diff'].std()
plt.figure(figsize=(8, 6))
sns.scatterplot(x=(combined_data_df['Score'] + combined_data_df['Mood'])/2, y=combined_data_df['Score_Mood_Diff'], color=SCORE_COLOR)
plt.axhline(mean_diff, color=MEAN_COLOR, linestyle='--', label=f'Mean Diff: {mean_diff:.2f}')
plt.axhline(mean_diff + 1.96*std_diff, color=MEAN_COLOR, linestyle=':', label='±1.96 SD')
plt.axhline(mean_diff - 1.96*std_diff, color=MEAN_COLOR, linestyle=':')
plt.title('Bland-Altman Plot: Score vs. Mood')
plt.xlabel('Mean of Score and Mood')
plt.ylabel('Score - Mood')
plt.legend(frameon=True, facecolor='#F9FAFB')
plt.tight_layout()
plt.show()

# 图13：Score 和 Mood 分布对比
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.histplot(combined_data_df['Mood'], kde=True, color=MOOD_COLOR)
plt.title('Mood Distribution')
plt.axvline(mood_mean, color=MEAN_COLOR, linestyle='--', label=f'Mean: {mood_mean:.2f}')
plt.legend(frameon=True, facecolor='#F9FAFB')
plt.subplot(1, 2, 2)
sns.histplot(combined_data_df['Score'], kde=True, color=SCORE_COLOR)
plt.title('Score Distribution')
score_mean = combined_data_df['Score'].mean()
plt.axvline(score_mean, color=MEAN_COLOR, linestyle='--', label=f'Mean: {score_mean:.2f}')
plt.legend(frameon=True, facecolor='#F9FAFB')
plt.tight_layout()
plt.show()

# 图14：Score 和 Mood 随 Record 趋势
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(combined_data_df['Record'], combined_data_df['Mood'], label='Mood', marker='o', color=MOOD_COLOR)
ax1.set_xlabel('Record')
ax1.set_ylabel('Mood', color=MOOD_COLOR)
ax1.tick_params(axis='y', labelcolor=MOOD_COLOR)
ax1.set_ylim(0, 5)
ax2 = ax1.twinx()
ax2.plot(combined_data_df['Record'], combined_data_df['Score'], label='Score', marker='x', color=SCORE_COLOR)
ax2.set_ylabel('Score', color=SCORE_COLOR)
ax2.tick_params(axis='y', labelcolor=SCORE_COLOR)
ax2.set_ylim(0, 5)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='#F9FAFB')
plt.title('Mood and Score Over Records')
plt.tight_layout()
plt.show()

'''
Challenge: There’s no ground-truth mood value in the dataset (Week, Mood, OutsideHour, Description, score). Mood is a subjective self-reported score (0–5), and score is an algorithm-derived sentiment score (0–5) from Description.
Proposed Method: Use OutsideHour and Description keywords as proxies for contextual factors influencing mood, and compare how well Mood and score correlate with these factors. The variable with stronger, more consistent relationships to context is likely a better mood indicator.
Rationale:
OutsideHour likely influences mood (e.g., more outdoor time may improve mood), as shown by prior correlations (Pearson: 0.587, Spearman: 0.446 for Mood vs. OutsideHour).
Description keywords (e.g., “下雨,” “工作”) capture situational factors. We can analyze how Mood and score vary with positive (e.g., “晴,” “散步”) vs. negative (e.g., “雨,” “压力”) keywords.
'''

# 图15：Mood 和 Score 按关键词情感分类
positive_keywords = ['散步', '朋友', '休息', '摸鱼', '开心', '快乐']
negative_keywords = ['压力', '疲惫', '工作', '难受', '难过', '伤心']
combined_data_df['Sentiment_Category'] = combined_data_df['Description'].apply(
    lambda x: 'positive' if any(kw in x for kw in positive_keywords) else ('negative' if any(kw in x for kw in negative_keywords) else 'neutral'))
plt.figure(figsize=(10, 6))
melted_df = pd.melt(combined_data_df, id_vars=['Sentiment_Category'], value_vars=['Mood', 'Score'],
                    var_name='Metric', value_name='Value')
sns.boxplot(x='Sentiment_Category', y='Value', hue='Metric', data=melted_df,
            palette={'Mood': MOOD_COLOR, 'Score': SCORE_COLOR})
plt.title('Sentiment Group by Keywords')
plt.xlabel('Sentiment')
plt.ylabel('Value (0–5)')
plt.legend(frameon=True, facecolor='#F9FAFB')
plt.tight_layout()
plt.show()

# 比较 Mood 和 Score 谁更能反映心情
print("\n=== Mood vs. Score: Which Better Reflects Mood? ===")
# 相关性分析
mood_outside_pearson = combined_data_df['Mood'].corr(combined_data_df['OutsideHour'], method='pearson')
score_outside_pearson = combined_data_df['Score'].corr(combined_data_df['OutsideHour'], method='pearson')
mood_outside_spearman, _ = spearmanr(combined_data_df['Mood'], combined_data_df['OutsideHour'])
score_outside_spearman, _ = spearmanr(combined_data_df['Score'], combined_data_df['OutsideHour'])
print("Correlation with OutsideHour:")
print(f"Mood - Pearson: {mood_outside_pearson:.3f}, Spearman: {mood_outside_spearman:.3f}")
print(f"Score - Pearson: {score_outside_pearson:.3f}, Spearman: {score_outside_spearman:.3f}")

# t-test 比较正负关键词
positive_mood = combined_data_df[combined_data_df['Sentiment_Category'] == 'positive']['Mood']
positive_score = combined_data_df[combined_data_df['Sentiment_Category'] == 'positive']['Score']
negative_mood = combined_data_df[combined_data_df['Sentiment_Category'] == 'negative']['Mood']
negative_score = combined_data_df[combined_data_df['Sentiment_Category'] == 'negative']['Score']
mood_ttest = ttest_ind(positive_mood, negative_mood, equal_var=False)
score_ttest = ttest_ind(positive_score, negative_score, equal_var=False)
print("\nT-test (Positive vs. Negative Keywords):")
print(f"Mood - t-statistic: {mood_ttest.statistic:.3f}, p-value: {mood_ttest.pvalue:.3f}")
print(f"Score - t-statistic: {score_ttest.statistic:.3f}, p-value: {score_ttest.pvalue:.3f}")

# 总结
print("\nSummary:")
if abs(mood_outside_pearson) > abs(score_outside_pearson) and abs(mood_outside_spearman) > abs(score_outside_spearman):
    print("Mood 可能更能反映心情，因其与户外时间有更强的相关性。")
elif abs(score_outside_pearson) > abs(mood_outside_pearson) and abs(score_outside_spearman) > abs(mood_outside_spearman):
    print("Score 可能更能反映心情，因其与户外时间有更强的相关性。")
else:
    print("Mood 和 Score 与户外时间的相关性相似，需进一步分析。")
if mood_ttest.pvalue < score_ttest.pvalue:
    print("Mood 在正负关键词间差异更显著，可能更敏感地反映心情变化。")
elif score_ttest.pvalue < mood_ttest.pvalue:
    print("Score 在正负关键词间差异更显著，可能更敏感地反映心情变化。")
else:
    print("Mood 和 Score 在正负关键词间差异相似，需结合其他因素判断。")

# 打印相关系数
print("Correlation with Score (Pearson):")
print(pearson_corr)
print("\nCorrelation with Score (Spearman):")
print(spearman_df)

# Discrepancy Analysis
combined_data_df['Discrepancy'] = abs(combined_data_df['Score'] - combined_data_df['Mood'])
discrepant_records = combined_data_df[combined_data_df['Discrepancy'] > 1][['Week', 'Mood', 'Score', 'Description']]
print("\nRecords with |Score - Mood| > 1:")
print(discrepant_records)

# 关键词分析 for 差异记录
discrepant_words = [word for desc in discrepant_records['Description'] for word in jieba.cut(desc) if len(word) > 1]
discrepant_word_counts = Counter(discrepant_words).most_common(10)
print("\nTop 10 Keywords in Discrepant Records:")
print(discrepant_word_counts)