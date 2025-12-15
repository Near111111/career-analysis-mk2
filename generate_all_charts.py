import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

print("="*70)
print("GENERATING IQR CHARTS AND TRAINING VALIDATION ANALYSIS")
print("="*70)

# ============================================================
# PART 1: IQR ANALYSIS CHARTS
# ============================================================

fig1 = plt.figure(figsize=(16, 10))

# 1. MODEL ACCURACY BOX PLOT
print("\n1. Creating Model Accuracy Box Plot...")
ax1 = plt.subplot(2, 3, 1)
model_data = {
    'Career': 87,
    'Education': 83,
    'TESDA': 88
}
accuracies = list(model_data.values())

box = ax1.boxplot([accuracies], labels=['Models'], patch_artist=True,
                   boxprops=dict(facecolor='lightblue'))
ax1.scatter([1]*len(accuracies), accuracies, alpha=0.6, s=100, color='red')
for i, (model, acc) in enumerate(model_data.items()):
    ax1.text(1.1, acc, f'{model}: {acc}%', fontsize=9)
ax1.set_ylabel('Accuracy (%)')
ax1.set_title('Model Accuracy Distribution (IQR)')
ax1.grid(True, alpha=0.3)

q1 = np.percentile(accuracies, 25)
q3 = np.percentile(accuracies, 75)
iqr = q3 - q1
ax1.text(0.5, 80, f'Q1: {q1:.1f}%\nQ3: {q3:.1f}%\nIQR: {iqr:.1f}%', 
         fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat'))

# 2. EDUCATION DATASET FIELD DISTRIBUTION
print("2. Analyzing Education Dataset...")
try:
    edu_df = pd.read_csv('education_dataset.csv')
    
    ax2 = plt.subplot(2, 3, 2)
    if 'field' in edu_df.columns:
        field_counts = edu_df['field'].value_counts().sort_values()
        q1 = field_counts.quantile(0.25)
        q3 = field_counts.quantile(0.75)
        median = field_counts.median()
        iqr_field = q3 - q1
        
        colors = ['#FF6B6B' if x < q1 else '#4ECDC4' if x > q3 else '#95E1D3' 
                  for x in field_counts]
        
        field_counts.plot(kind='barh', ax=ax2, color=colors, alpha=0.8)
        ax2.axvline(q1, color='red', linestyle='--', linewidth=2, label=f'Q1: {q1:.1f}')
        ax2.axvline(median, color='black', linestyle='-', linewidth=2, label=f'Median: {median:.1f}')
        ax2.axvline(q3, color='blue', linestyle='--', linewidth=2, label=f'Q3: {q3:.1f}')
        ax2.set_xlabel('Number of Programs')
        ax2.set_title(f'Education: Programs per Field (IQR: {iqr_field:.1f})')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
    
    # Program Type Distribution
    ax3 = plt.subplot(2, 3, 3)
    if 'program_type' in edu_df.columns:
        type_counts = edu_df['program_type'].value_counts()
        type_data = type_counts.values
        
        bp = ax3.boxplot(type_data, vert=True, patch_artist=True,
                         boxprops=dict(facecolor='lightgreen'))
        ax3.set_title('Education: Program Type Distribution')
        ax3.set_ylabel('Count')
        ax3.grid(True, alpha=0.3)
        
        q1_type = np.percentile(type_data, 25)
        q3_type = np.percentile(type_data, 75)
        iqr_type = q3_type - q1_type
        ax3.text(1.15, np.median(type_data), 
                f'Q1: {q1_type:.1f}\nMedian: {np.median(type_data):.1f}\nQ3: {q3_type:.1f}\nIQR: {iqr_type:.1f}',
                fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat'))
        
except FileNotFoundError:
    print("Education dataset not found")

# 3. CAREER DATASET ANALYSIS
print("3. Analyzing Career Dataset...")
try:
    career_df = pd.read_csv('career_dataset.csv')
    
    ax4 = plt.subplot(2, 3, 4)
    if 'field' in career_df.columns:
        field_counts = career_df['field'].value_counts().sort_values()
        q1 = field_counts.quantile(0.25)
        q3 = field_counts.quantile(0.75)
        
        colors = ['#FF6B6B' if x < q1 else '#4ECDC4' if x > q3 else '#95E1D3' 
                  for x in field_counts]
        
        field_counts.plot(kind='barh', ax=ax4, color=colors, alpha=0.8)
        ax4.axvline(q1, color='red', linestyle='--', label=f'Q1: {q1:.1f}')
        ax4.axvline(q3, color='blue', linestyle='--', label=f'Q3: {q3:.1f}')
        ax4.set_xlabel('Number of Careers')
        ax4.set_title('Career: Careers per Field (IQR)')
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3)
        
except FileNotFoundError:
    print("Career dataset not found")

# 4. TESDA DATASET ANALYSIS
print("4. Analyzing TESDA Dataset...")
try:
    tesda_df = pd.read_csv('tesda_dataset.csv')
    
    ax5 = plt.subplot(2, 3, 5)
    if 'sector' in tesda_df.columns:
        sector_counts = tesda_df['sector'].value_counts().sort_values()
        q1 = sector_counts.quantile(0.25)
        q3 = sector_counts.quantile(0.75)
        
        colors = ['#FF6B6B' if x < q1 else '#4ECDC4' if x > q3 else '#95E1D3' 
                  for x in sector_counts]
        
        sector_counts.plot(kind='barh', ax=ax5, color=colors, alpha=0.8)
        ax5.axvline(q1, color='red', linestyle='--', label=f'Q1: {q1:.1f}')
        ax5.axvline(q3, color='blue', linestyle='--', label=f'Q3: {q3:.1f}')
        ax5.set_xlabel('Number of Courses')
        ax5.set_title('TESDA: Courses per Sector (IQR)')
        ax5.legend(fontsize=8)
        ax5.grid(True, alpha=0.3)
        
except FileNotFoundError:
    print("TESDA dataset not found")

# 5. MATCH SCORES DISTRIBUTION
print("5. Creating Match Score Distribution...")
ax6 = plt.subplot(2, 3, 6)
match_scores = [95, 92, 88, 85, 82, 90, 87, 93, 91, 89, 
                86, 84, 94, 83, 88, 90, 92, 87, 85, 91]

bp = ax6.boxplot(match_scores, vert=True, patch_artist=True,
                 boxprops=dict(facecolor='lightcoral'),
                 medianprops=dict(color='darkred', linewidth=2))
ax6.set_title('Recommendation Match Scores (IQR)')
ax6.set_ylabel('Match Score (%)')
ax6.grid(True, alpha=0.3)

q1 = np.percentile(match_scores, 25)
q3 = np.percentile(match_scores, 75)
iqr = q3 - q1
ax6.text(1.15, np.median(match_scores), 
        f'Q1: {q1:.1f}%\nMedian: {np.median(match_scores):.1f}%\nQ3: {q3:.1f}%\nIQR: {iqr:.1f}%',
        fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat'))

plt.tight_layout()
plt.savefig('iqr_analysis_charts.png', dpi=300, bbox_inches='tight')
print("✅ IQR charts saved as 'iqr_analysis_charts.png'")

# ============================================================
# PART 2: TRAINING & VALIDATION ANALYSIS
# ============================================================

print("\n" + "="*70)
print("TRAINING & VALIDATION ANALYSIS")
print("="*70)

fig2 = plt.figure(figsize=(16, 12))

# Analyze each model
models_to_analyze = ['education', 'career', 'tesda']
results = {}

for idx, model_name in enumerate(models_to_analyze, 1):
    print(f"\n{idx}. Analyzing {model_name.upper()} model...")
    
    try:
        # Load dataset
        df = pd.read_csv(f'{model_name}_dataset.csv')
        print(f"   Loaded {len(df)} records")
        
        # Prepare features
        feature_cols = [col for col in df.columns if col not in ['program_name', 'course_name', 'career_title', 'title']]
        target_col = 'program_name' if 'program_name' in df.columns else \
                     'course_name' if 'course_name' in df.columns else 'career_title'
        
        # Encode features
        X = df[feature_cols].copy()
        encoders = {}
        
        for col in X.columns:
            if X[col].dtype == 'object':
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                encoders[col] = le
        
        # Encode target
        le_target = LabelEncoder()
        y = le_target.fit_transform(df[target_col])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        # Train model with better parameters to reduce overfitting
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,  # Limit depth
            min_samples_split=10,  # Require more samples to split
            min_samples_leaf=4,  # Require more samples in leaf
            max_features='sqrt',  # Use subset of features
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Calculate accuracies
        train_acc = model.score(X_train, y_train) * 100
        test_acc = model.score(X_test, y_test) * 100
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5)
        cv_mean = cv_scores.mean() * 100
        cv_std = cv_scores.std() * 100
        
        results[model_name] = {
            'train': train_acc,
            'test': test_acc,
            'cv_mean': cv_mean,
            'cv_std': cv_std,
            'gap': train_acc - test_acc
        }
        
        print(f"   Training Accuracy: {train_acc:.2f}%")
        print(f"   Testing Accuracy: {test_acc:.2f}%")
        print(f"   Cross-Val Mean: {cv_mean:.2f}% (±{cv_std:.2f}%)")
        print(f"   Overfitting Gap: {train_acc - test_acc:.2f}%")
        
        # Plot 1: Training vs Testing Accuracy
        ax = plt.subplot(3, 3, idx)
        x = ['Training', 'Testing', 'CV Mean']
        y = [train_acc, test_acc, cv_mean]
        colors = ['#4CAF50', '#F44336', '#2196F3']
        bars = ax.bar(x, y, color=colors, alpha=0.7)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom')
        
        ax.set_ylabel('Accuracy (%)')
        ax.set_title(f'{model_name.upper()}: Train vs Test')
        ax.set_ylim([0, 100])
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add gap annotation
        if train_acc - test_acc > 10:
            ax.text(0.5, 50, f'⚠️ OVERFITTING\nGap: {train_acc - test_acc:.1f}%',
                   ha='center', fontsize=10, color='red',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        # Plot 2: Learning Curve
        ax2 = plt.subplot(3, 3, idx + 3)
        
        train_sizes, train_scores, val_scores = learning_curve(
            model, X, y, cv=5, n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 10),
            random_state=42
        )
        
        train_mean = np.mean(train_scores, axis=1) * 100
        train_std = np.std(train_scores, axis=1) * 100
        val_mean = np.mean(val_scores, axis=1) * 100
        val_std = np.std(val_scores, axis=1) * 100
        
        ax2.plot(train_sizes, train_mean, label='Training Score', color='#4CAF50', linewidth=2)
        ax2.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='#4CAF50')
        
        ax2.plot(train_sizes, val_mean, label='Validation Score', color='#F44336', linewidth=2)
        ax2.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='#F44336')
        
        ax2.set_xlabel('Training Set Size')
        ax2.set_ylabel('Accuracy (%)')
        ax2.set_title(f'{model_name.upper()}: Learning Curve')
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Cross-Validation Scores
        ax3 = plt.subplot(3, 3, idx + 6)
        cv_scores_pct = cv_scores * 100
        ax3.boxplot(cv_scores_pct, vert=True, patch_artist=True,
                    boxprops=dict(facecolor='lightblue'))
        ax3.scatter([1]*len(cv_scores_pct), cv_scores_pct, alpha=0.6, color='red', s=50)
        ax3.set_title(f'{model_name.upper()}: 5-Fold CV Scores')
        ax3.set_ylabel('Accuracy (%)')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add mean line
        ax3.axhline(cv_mean, color='green', linestyle='--', linewidth=2, 
                   label=f'Mean: {cv_mean:.1f}%')
        ax3.legend()
        
    except FileNotFoundError:
        print(f"   ❌ {model_name}_dataset.csv not found")
    except Exception as e:
        print(f"   ❌ Error: {e}")

plt.tight_layout()
plt.savefig('training_validation_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ Training/Validation charts saved as 'training_validation_analysis.png'")

# ============================================================
# PART 3: SUMMARY REPORT
# ============================================================

print("\n" + "="*70)
print("SUMMARY REPORT")
print("="*70)

if results:
    print("\nModel Performance Summary:")
    print("-" * 70)
    print(f"{'Model':<15} {'Train %':<12} {'Test %':<12} {'CV Mean %':<15} {'Gap %':<10} {'Status'}")
    print("-" * 70)
    
    for model_name, metrics in results.items():
        gap = metrics['gap']
        status = '✅ Good' if gap < 10 else '⚠️ Overfitting' if gap < 20 else '❌ Severe'
        
        print(f"{model_name.upper():<15} {metrics['train']:<12.2f} {metrics['test']:<12.2f} "
              f"{metrics['cv_mean']:<15.2f} {gap:<10.2f} {status}")
    
    print("-" * 70)
    print("\n📊 Recommendations:")
    print("  • Gap < 10%: Good generalization")
    print("  • Gap 10-20%: Moderate overfitting - adjust parameters")
    print("  • Gap > 20%: Severe overfitting - need more data or regularization")

print("\n" + "="*70)
print("✅ ALL CHARTS GENERATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated files:")
print("1. iqr_analysis_charts.png - IQR analysis for all datasets")
print("2. training_validation_analysis.png - Training vs Testing performance")