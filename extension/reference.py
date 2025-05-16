import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# 假设你有多个数据条目存储在列表中
data_list = [
    {
        'Week': 1,
        'Title': 'Project Meeting',
        'OutsideHour': 2.5,
        'Mood': 7,
        'Description': 'Discussed project milestones',
        'Created_time': '2025-01-01T10:00:00.000Z'
    },
    {
        'Week': 1,
        'Title': 'Team Lunch',
        'OutsideHour': 1.0,
        'Mood': 8,
        'Description': 'Casual team bonding',
        'Created_time': '2025-01-02T12:30:00.000Z'
    },
    # ... 更多数据
]

# 1. 转换为 DataFrame
df = pd.DataFrame(data_list)

# 2. 数据清洗和预处理
# 转换时间格式
df['Created_time'] = pd.to_datetime(df['Created_time'])

# 提取日期和小时
df['Date'] = df['Created_time'].dt.date
df['Hour'] = df['Created_time'].dt.hour

# 检查缺失值
print("缺失值统计：")
print(df.isnull().sum())

# 3. 基本统计分析
print("\n基本统计信息：")
print(df.describe())

# 4. 分组分析
# 按周统计户外时间和心情
weekly_stats = df.groupby('Week')[['OutsideHour', 'Mood']].agg(['mean', 'sum', 'count'])
print("\n每周统计：")
print(weekly_stats)

# 5. 相关性分析
correlation = df[['OutsideHour', 'Mood']].corr()
print("\n户外时间与心情的相关性：")
print(correlation)

# 6. 可视化
plt.style.use('seaborn')

# 6.1 每周户外时间柱状图
plt.figure(figsize=(10, 6))
df.groupby('Week')['OutsideHour'].sum().plot(kind='bar')
plt.title('Weekly Outside Hours')
plt.xlabel('Week')
plt.ylabel('Total Outside Hours')
plt.tight_layout()
plt.show()

# 6.2 心情与户外时间散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='OutsideHour', y='Mood', hue='Week', size='Week')
plt.title('Mood vs Outside Hours')
plt.xlabel('Outside Hours')
plt.ylabel('Mood Score')
plt.tight_layout()
plt.show()

# 7. 文本分析（Description）
# 简单的情感词频统计
from collections import Counter
words = ' '.join(df['Description']).lower().split()
word_freq = Counter(words)
print("\n描述文本词频统计（前10）：")
print(word_freq.most_common(10))

# 8. 按时间段分析
df['Time_of_Day'] = pd.cut(df['Hour'],
                          bins=[0, 6, 12, 18, 24],
                          labels=['Night', 'Morning', 'Afternoon', 'Evening'])
time_stats = df.groupby('Time_of_Day')[['Mood', 'OutsideHour']].mean()
print("\n按时间段的平均心情和户外时间：")
print(time_stats)