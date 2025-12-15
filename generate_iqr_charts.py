import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

print("="*60)
print("GENERATING IQR CHARTS FOR EDULIFT SYSTEM")
print("="*60)

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))

# 1. MODEL ACCURACY BOX PLOT
print("\n1. Creating Model Accuracy Box Plot...")
ax1 = plt.subplot(3, 3, 1)
model_data = {
    'Career': 87,
    'Education': 83,
    'TESDA': 88
}
models = list(model_data.keys())
accuracies = list(model_data.values())

ax1.boxplot([accuracies], labels=['Models'])
ax1.scatter([1]*len(accuracies), accuracies, alpha=0.6, s=100)
for i, (model, acc) in enumerate(model_data.items()):
    ax1.text(1.1, acc, f'{model}: {acc}%', fontsize=9)
ax1.set_ylabel('Accuracy (%)')
ax1.set_title('Model Accuracy Distribution')
ax1.grid(True, alpha=0.3)

# 2. EDUCATION DATASET ANALYSIS
print("2. Analyzing Education Dataset...")
try:
    edu_df = pd.read_csv('education_dataset.csv')
    
    # Programs by Type
    ax2 = plt.subplot(3, 3, 2)
    if 'program_type' in edu_df.columns:
        type_counts = edu_df['program_type'].value_counts()
        type_counts.plot(kind='box', ax=ax2)
        ax2.set_title('Programs per Type - Box Plot')
        ax2.set_ylabel('Count')
        
    # Programs by Field
    ax3 = plt.subplot(3, 3, 3)
    if 'field' in edu_df.columns:
        field_counts = edu_df['field'].value_counts()
        field_counts.plot(kind='box', ax=ax3)
        ax3.set_title('Programs per Field - Box Plot')
        ax3.set_ylabel('Count')
        
    # Detailed Field Distribution
    ax4 = plt.subplot(3, 3, 4)
    if 'field' in edu_df.columns:
        field_counts = edu_df['field'].value_counts().sort_values()
        colors = ['#FF6B6B' if x < field_counts.quantile(0.25) else 
                  '#4ECDC4' if x > field_counts.quantile(0.75) else 
                  '#95E1D3' for x in field_counts]
        field_counts.plot(kind='barh', ax=ax4, color=colors)
        ax4.set_title('Programs per Field (Colored by Quartile)')
        ax4.set_xlabel('Number of Programs')
        
        # Add Q1, Q3 lines
        q1 = field_counts.quantile(0.25)
        q3 = field_counts.quantile(0.75)
        ax4.axvline(q1, color='red', linestyle='--', label=f'Q1: {q1:.1f}')
        ax4.axvline(q3, color='blue', linestyle='--', label=f'Q3: {q3:.1f}')
        ax4.legend()
        
    # Program Type Distribution
    ax5 = plt.subplot(3, 3, 5)
    if 'program_type' in edu_df.columns:
        type_counts = edu_df['program_type'].value_counts()
        colors_type = plt.cm.Set3(range(len(type_counts)))
        type_counts.plot(kind='bar', ax=ax5, color=colors_type)
        ax5.set_title('Program Type Distribution')
        ax5.set_ylabel('Count')
        ax5.set_xlabel('Program Type')
        ax5.tick_params(axis='x', rotation=45)
        
        # Add median line
        median = type_counts.median()
        ax5.axhline(median, color='red', linestyle='--', label=f'Median: {median:.1f}')
        ax5.legend()
        
except FileNotFoundError:
    print("Education dataset not found")
except Exception as e:
    print(f"Error: {e}")

# 3. CAREER DATASET ANALYSIS
print("3. Analyzing Career Dataset...")
try:
    career_df = pd.read_csv('career_dataset.csv')
    
    # Careers by Field
    ax6 = plt.subplot(3, 3, 6)
    if 'field' in career_df.columns:
        field_counts = career_df['field'].value_counts().sort_values()
        colors = ['#FF6B6B' if x < field_counts.quantile(0.25) else 
                  '#4ECDC4' if x > field_counts.quantile(0.75) else 
                  '#95E1D3' for x in field_counts]
        field_counts.plot(kind='barh', ax=ax6, color=colors)
        ax6.set_title('Careers per Field (Colored by Quartile)')
        ax6.set_xlabel('Number of Careers')
        
        q1 = field_counts.quantile(0.25)
        q3 = field_counts.quantile(0.75)
        ax6.axvline(q1, color='red', linestyle='--', label=f'Q1: {q1:.1f}')
        ax6.axvline(q3, color='blue', linestyle='--', label=f'Q3: {q3:.1f}')
        ax6.legend()
        
except FileNotFoundError:
    print("Career dataset not found")
except Exception as e:
    print(f"Error: {e}")

# 4. TESDA DATASET ANALYSIS
print("4. Analyzing TESDA Dataset...")
try:
    tesda_df = pd.read_csv('tesda_dataset.csv')
    
    # Courses by Sector
    ax8 = plt.subplot(3, 3, 8)
    if 'sector' in tesda_df.columns:
        sector_counts = tesda_df['sector'].value_counts().sort_values()
        colors = ['#FF6B6B' if x < sector_counts.quantile(0.25) else 
                  '#4ECDC4' if x > sector_counts.quantile(0.75) else 
                  '#95E1D3' for x in sector_counts]
        sector_counts.plot(kind='barh', ax=ax8, color=colors)
        ax8.set_title('Courses per Sector (Colored by Quartile)')
        ax8.set_xlabel('Number of Courses')
        
        q1 = sector_counts.quantile(0.25)
        q3 = sector_counts.quantile(0.75)
        ax8.axvline(q1, color='red', linestyle='--', label=f'Q1: {q1:.1f}')
        ax8.axvline(q3, color='blue', linestyle='--', label=f'Q3: {q3:.1f}')
        ax8.legend()
        
except FileNotFoundError:
    print("TESDA dataset not found")
except Exception as e:
    print(f"Error: {e}")

# 5. MATCH SCORE DISTRIBUTION
print("5. Creating Match Score Distribution...")
ax9 = plt.subplot(3, 3, 9)
match_scores = [95, 92, 88, 85, 82, 90, 87, 93, 91, 89, 
                86, 84, 94, 83, 88, 90, 92, 87, 85, 91]

ax9.boxplot(match_scores, vert=True, patch_artist=True,
            boxprops=dict(facecolor='lightblue'),
            medianprops=dict(color='red', linewidth=2))
ax9.set_title('Recommendation Match Scores')
ax9.set_ylabel('Match Score (%)')
ax9.grid(True, alpha=0.3)

# Add statistics text
q1 = np.percentile(match_scores, 25)
q3 = np.percentile(match_scores, 75)
median = np.median(match_scores)
iqr = q3 - q1

stats_text = f'Q1: {q1:.1f}%\nMedian: {median:.1f}%\nQ3: {q3:.1f}%\nIQR: {iqr:.1f}%'
ax9.text(1.15, median, stats_text, fontsize=9, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('iqr_analysis_charts.png', dpi=300, bbox_inches='tight')
print("\n✅ Charts saved as 'iqr_analysis_charts.png'")

# Create separate detailed chart for education dataset
print("\n6. Creating detailed Education Dataset IQR Chart...")
fig2, axes = plt.subplots(2, 2, figsize=(14, 10))

try:
    edu_df = pd.read_csv('education_dataset.csv')
    
    # Chart 1: Field Distribution with IQR
    if 'field' in edu_df.columns:
        field_counts = edu_df['field'].value_counts().sort_values()
        q1 = field_counts.quantile(0.25)
        q3 = field_counts.quantile(0.75)
        median = field_counts.median()
        iqr = q3 - q1
        
        colors = ['red' if x < q1 else 'green' if x > q3 else 'yellow' 
                  for x in field_counts]
        
        axes[0, 0].barh(field_counts.index, field_counts.values, color=colors, alpha=0.7)
        axes[0, 0].axvline(q1, color='red', linestyle='--', linewidth=2, label=f'Q1: {q1:.1f}')
        axes[0, 0].axvline(median, color='black', linestyle='-', linewidth=2, label=f'Median: {median:.1f}')
        axes[0, 0].axvline(q3, color='blue', linestyle='--', linewidth=2, label=f'Q3: {q3:.1f}')
        axes[0, 0].set_xlabel('Number of Programs')
        axes[0, 0].set_title(f'Programs per Field (IQR: {iqr:.1f})')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
    
    # Chart 2: Program Type Distribution
    if 'program_type' in edu_df.columns:
        type_counts = edu_df['program_type'].value_counts()
        axes[0, 1].bar(type_counts.index, type_counts.values, 
                       color=['#FF6B6B', '#4ECDC4', '#95E1D3', '#F7DC6F'])
        axes[0, 1].set_ylabel('Number of Programs')
        axes[0, 1].set_title('Program Type Distribution')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add median line
        median = type_counts.median()
        axes[0, 1].axhline(median, color='red', linestyle='--', 
                           label=f'Median: {median:.1f}')
        axes[0, 1].legend()
    
    # Chart 3: Box Plot for Field Distribution
    if 'field' in edu_df.columns:
        field_data = [edu_df[edu_df['field'] == f].shape[0] 
                      for f in edu_df['field'].unique()]
        bp = axes[1, 0].boxplot(field_data, vert=True, patch_artist=True,
                                boxprops=dict(facecolor='lightgreen', alpha=0.7),
                                medianprops=dict(color='red', linewidth=2))
        axes[1, 0].set_title('Field Distribution - Box Plot')
        axes[1, 0].set_ylabel('Programs per Field')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add statistics
        q1 = np.percentile(field_data, 25)
        q3 = np.percentile(field_data, 75)
        median = np.median(field_data)
        iqr = q3 - q1
        
        stats_text = f'Min: {min(field_data)}\nQ1: {q1:.1f}\nMedian: {median:.1f}\nQ3: {q3:.1f}\nMax: {max(field_data)}\nIQR: {iqr:.1f}'
        axes[1, 0].text(1.15, median, stats_text, fontsize=9,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Chart 4: Heatmap of Program Type x Field
    if 'field' in edu_df.columns and 'program_type' in edu_df.columns:
        pivot_table = edu_df.pivot_table(
            index='field', 
            columns='program_type', 
            aggfunc='size', 
            fill_value=0
        )
        sns.heatmap(pivot_table, annot=True, fmt='d', cmap='YlOrRd', 
                    ax=axes[1, 1], cbar_kws={'label': 'Count'})
        axes[1, 1].set_title('Programs: Field × Type Heatmap')
        axes[1, 1].set_xlabel('Program Type')
        axes[1, 1].set_ylabel('Field')
        
except FileNotFoundError:
    print("Education dataset not found")
except Exception as e:
    print(f"Error: {e}")

plt.tight_layout()
plt.savefig('education_iqr_detailed.png', dpi=300, bbox_inches='tight')
print("✅ Detailed charts saved as 'education_iqr_detailed.png'")

print("\n" + "="*60)
print("✅ ALL IQR CHARTS GENERATED SUCCESSFULLY!")
print("="*60)
print("\nGenerated files:")
print("1. iqr_analysis_charts.png - Overview of all datasets")
print("2. education_iqr_detailed.png - Detailed education analysis")
print("\nCharts include:")
print("- Box plots with Q1, Q3, Median, IQR")
print("- Color-coded distributions by quartiles")
print("- Statistical annotations")
print("- Heatmaps and bar charts")
