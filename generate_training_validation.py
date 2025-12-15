import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import joblib

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

print("="*70)
print("GENERATING TRAINING & VALIDATION CHARTS FOR EDULIFT SYSTEM")
print("="*70)

# Create main figure
fig = plt.figure(figsize=(18, 14))

# ============= CAREER MODEL VALIDATION =============
print("\n1. Training and Validating Career Model...")
try:
    career_df = pd.read_csv('career_dataset.csv')
    
    # Prepare features and target
    feature_cols = ["primary_skills", "industry", "salary", "work_environment"]
    X = career_df[feature_cols].copy()
    y = career_df['career_title']
    
    # Encode features
    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("").astype(str)
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
    
    # Encode target
    y_le = LabelEncoder()
    y_enc = y_le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=400, random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"   Career Model - Train Accuracy: {train_accuracy:.4f}")
    print(f"   Career Model - Test Accuracy: {test_accuracy:.4f}")
    
    # Plot 1: Training vs Test Accuracy
    ax1 = plt.subplot(3, 4, 1)
    accuracies = [train_accuracy * 100, test_accuracy * 100]
    bars = ax1.bar(['Training', 'Test'], accuracies, color=['#4CAF50', '#2196F3'])
    ax1.set_ylabel('Accuracy (%)')
    ax1.set_title('Career Model: Train vs Test Accuracy')
    ax1.set_ylim([0, 100])
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{accuracies[i]:.2f}%', ha='center', va='bottom')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Feature Importance
    ax2 = plt.subplot(3, 4, 2)
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    ax2.barh([feature_cols[i] for i in indices], importances[indices], color='#FF9800')
    ax2.set_xlabel('Importance')
    ax2.set_title('Career Model: Feature Importance')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Cross-validation scores
    ax3 = plt.subplot(3, 4, 3)
    cv_scores = cross_val_score(model, X, y_enc, cv=5)
    ax3.plot(range(1, 6), cv_scores * 100, marker='o', linewidth=2, markersize=8)
    ax3.axhline(cv_scores.mean() * 100, color='red', linestyle='--', 
                label=f'Mean: {cv_scores.mean()*100:.2f}%')
    ax3.set_xlabel('Fold')
    ax3.set_ylabel('Accuracy (%)')
    ax3.set_title('Career Model: 5-Fold Cross-Validation')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Learning Curve
    ax4 = plt.subplot(3, 4, 4)
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y_enc, cv=5, n_jobs=-1, 
        train_sizes=np.linspace(0.1, 1.0, 10), random_state=42)
    
    train_mean = np.mean(train_scores, axis=1) * 100
    train_std = np.std(train_scores, axis=1) * 100
    val_mean = np.mean(val_scores, axis=1) * 100
    val_std = np.std(val_scores, axis=1) * 100
    
    ax4.plot(train_sizes, train_mean, label='Training score', color='blue', marker='o')
    ax4.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    ax4.plot(train_sizes, val_mean, label='Validation score', color='red', marker='s')
    ax4.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='red')
    ax4.set_xlabel('Training Examples')
    ax4.set_ylabel('Accuracy (%)')
    ax4.set_title('Career Model: Learning Curve')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
except Exception as e:
    print(f"Error with Career Model: {e}")

# ============= EDUCATION MODEL VALIDATION =============
print("\n2. Training and Validating Education Model...")
try:
    edu_df = pd.read_csv('education_dataset.csv')
    
    # Prepare features and target
    feature_cols = ["modality", "budget", "learning_style", "motivation", "field"]
    X = edu_df[feature_cols].copy()
    y = edu_df['program_name']
    
    # Encode features
    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("").astype(str)
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
    
    # Encode target
    y_le = LabelEncoder()
    y_enc = y_le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=400, random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"   Education Model - Train Accuracy: {train_accuracy:.4f}")
    print(f"   Education Model - Test Accuracy: {test_accuracy:.4f}")
    
    # Plot 5: Training vs Test Accuracy
    ax5 = plt.subplot(3, 4, 5)
    accuracies = [train_accuracy * 100, test_accuracy * 100]
    bars = ax5.bar(['Training', 'Test'], accuracies, color=['#4CAF50', '#2196F3'])
    ax5.set_ylabel('Accuracy (%)')
    ax5.set_title('Education Model: Train vs Test Accuracy')
    ax5.set_ylim([0, 100])
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{accuracies[i]:.2f}%', ha='center', va='bottom')
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Feature Importance
    ax6 = plt.subplot(3, 4, 6)
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    ax6.barh([feature_cols[i] for i in indices], importances[indices], color='#9C27B0')
    ax6.set_xlabel('Importance')
    ax6.set_title('Education Model: Feature Importance')
    ax6.grid(True, alpha=0.3)
    
    # Plot 7: Cross-validation scores
    ax7 = plt.subplot(3, 4, 7)
    cv_scores = cross_val_score(model, X, y_enc, cv=5)
    ax7.plot(range(1, 6), cv_scores * 100, marker='o', linewidth=2, markersize=8, color='purple')
    ax7.axhline(cv_scores.mean() * 100, color='red', linestyle='--', 
                label=f'Mean: {cv_scores.mean()*100:.2f}%')
    ax7.set_xlabel('Fold')
    ax7.set_ylabel('Accuracy (%)')
    ax7.set_title('Education Model: 5-Fold Cross-Validation')
    ax7.legend()
    ax7.grid(True, alpha=0.3)
    
    # Plot 8: Learning Curve
    ax8 = plt.subplot(3, 4, 8)
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y_enc, cv=5, n_jobs=-1, 
        train_sizes=np.linspace(0.1, 1.0, 10), random_state=42)
    
    train_mean = np.mean(train_scores, axis=1) * 100
    train_std = np.std(train_scores, axis=1) * 100
    val_mean = np.mean(val_scores, axis=1) * 100
    val_std = np.std(val_scores, axis=1) * 100
    
    ax8.plot(train_sizes, train_mean, label='Training score', color='blue', marker='o')
    ax8.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    ax8.plot(train_sizes, val_mean, label='Validation score', color='red', marker='s')
    ax8.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='red')
    ax8.set_xlabel('Training Examples')
    ax8.set_ylabel('Accuracy (%)')
    ax8.set_title('Education Model: Learning Curve')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    
except Exception as e:
    print(f"Error with Education Model: {e}")

# ============= TESDA MODEL VALIDATION =============
print("\n3. Training and Validating TESDA Model...")
try:
    tesda_df = pd.read_csv('tesda_dataset.csv')
    
    # Prepare features and target
    feature_cols = ["budget", "time_available", "location", "experience"]
    X = tesda_df[feature_cols].copy()
    y = tesda_df['course_title']
    
    # Encode features
    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("").astype(str)
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
    
    # Encode target
    y_le = LabelEncoder()
    y_enc = y_le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=400, random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"   TESDA Model - Train Accuracy: {train_accuracy:.4f}")
    print(f"   TESDA Model - Test Accuracy: {test_accuracy:.4f}")
    
    # Plot 9: Training vs Test Accuracy
    ax9 = plt.subplot(3, 4, 9)
    accuracies = [train_accuracy * 100, test_accuracy * 100]
    bars = ax9.bar(['Training', 'Test'], accuracies, color=['#4CAF50', '#2196F3'])
    ax9.set_ylabel('Accuracy (%)')
    ax9.set_title('TESDA Model: Train vs Test Accuracy')
    ax9.set_ylim([0, 100])
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax9.text(bar.get_x() + bar.get_width()/2., height,
                f'{accuracies[i]:.2f}%', ha='center', va='bottom')
    ax9.grid(True, alpha=0.3)
    
    # Plot 10: Feature Importance
    ax10 = plt.subplot(3, 4, 10)
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    ax10.barh([feature_cols[i] for i in indices], importances[indices], color='#FF5722')
    ax10.set_xlabel('Importance')
    ax10.set_title('TESDA Model: Feature Importance')
    ax10.grid(True, alpha=0.3)
    
    # Plot 11: Cross-validation scores
    ax11 = plt.subplot(3, 4, 11)
    cv_scores = cross_val_score(model, X, y_enc, cv=5)
    ax11.plot(range(1, 6), cv_scores * 100, marker='o', linewidth=2, markersize=8, color='orange')
    ax11.axhline(cv_scores.mean() * 100, color='red', linestyle='--', 
                 label=f'Mean: {cv_scores.mean()*100:.2f}%')
    ax11.set_xlabel('Fold')
    ax11.set_ylabel('Accuracy (%)')
    ax11.set_title('TESDA Model: 5-Fold Cross-Validation')
    ax11.legend()
    ax11.grid(True, alpha=0.3)
    
    # Plot 12: Learning Curve
    ax12 = plt.subplot(3, 4, 12)
    train_sizes, train_scores, val_scores = learning_curve(
        model, X, y_enc, cv=5, n_jobs=-1, 
        train_sizes=np.linspace(0.1, 1.0, 10), random_state=42)
    
    train_mean = np.mean(train_scores, axis=1) * 100
    train_std = np.std(train_scores, axis=1) * 100
    val_mean = np.mean(val_scores, axis=1) * 100
    val_std = np.std(val_scores, axis=1) * 100
    
    ax12.plot(train_sizes, train_mean, label='Training score', color='blue', marker='o')
    ax12.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    ax12.plot(train_sizes, val_mean, label='Validation score', color='red', marker='s')
    ax12.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='red')
    ax12.set_xlabel('Training Examples')
    ax12.set_ylabel('Accuracy (%)')
    ax12.set_title('TESDA Model: Learning Curve')
    ax12.legend()
    ax12.grid(True, alpha=0.3)
    
except Exception as e:
    print(f"Error with TESDA Model: {e}")

plt.suptitle('EduLift ML Models - Training & Validation Analysis', fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.savefig('training_validation_charts.png', dpi=300, bbox_inches='tight')
print("\n✅ Main chart saved as 'training_validation_charts.png'")

# ============= DETAILED COMPARISON CHART =============
print("\n4. Creating Detailed Comparison Chart...")
fig2, axes = plt.subplots(2, 2, figsize=(14, 10))

# Collect all model metrics
models_summary = []

try:
    # Career Model Metrics
    career_df = pd.read_csv('career_dataset.csv')
    feature_cols = ["primary_skills", "industry", "salary", "work_environment"]
    X = career_df[feature_cols].copy()
    y = career_df['career_title']
    
    for col in X.columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("").astype(str)
        X[col] = le.fit_transform(X[col])
    
    y_le = LabelEncoder()
    y_enc = y_le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=400, random_state=42)
    model.fit(X_train, y_train)
    
    cv_scores = cross_val_score(model, X, y_enc, cv=5)
    
    models_summary.append({
        'Model': 'Career',
        'Train Acc': model.score(X_train, y_train) * 100,
        'Test Acc': model.score(X_test, y_test) * 100,
        'CV Mean': cv_scores.mean() * 100,
        'CV Std': cv_scores.std() * 100
    })
except:
    pass

try:
    # Education Model Metrics
    edu_df = pd.read_csv('education_dataset.csv')
    feature_cols = ["modality", "budget", "learning_style", "motivation", "field"]
    X = edu_df[feature_cols].copy()
    y = edu_df['program_name']
    
    for col in X.columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("").astype(str)
        X[col] = le.fit_transform(X[col])
    
    y_le = LabelEncoder()
    y_enc = y_le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=400, random_state=42)
    model.fit(X_train, y_train)
    
    cv_scores = cross_val_score(model, X, y_enc, cv=5)
    
    models_summary.append({
        'Model': 'Education',
        'Train Acc': model.score(X_train, y_train) * 100,
        'Test Acc': model.score(X_test, y_test) * 100,
        'CV Mean': cv_scores.mean() * 100,
        'CV Std': cv_scores.std() * 100
    })
except:
    pass

try:
    # TESDA Model Metrics
    tesda_df = pd.read_csv('tesda_dataset.csv')
    feature_cols = ["budget", "time_available", "location", "experience"]
    X = tesda_df[feature_cols].copy()
    y = tesda_df['course_title']
    
    for col in X.columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("").astype(str)
        X[col] = le.fit_transform(X[col])
    
    y_le = LabelEncoder()
    y_enc = y_le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=400, random_state=42)
    model.fit(X_train, y_train)
    
    cv_scores = cross_val_score(model, X, y_enc, cv=5)
    
    models_summary.append({
        'Model': 'TESDA',
        'Train Acc': model.score(X_train, y_train) * 100,
        'Test Acc': model.score(X_test, y_test) * 100,
        'CV Mean': cv_scores.mean() * 100,
        'CV Std': cv_scores.std() * 100
    })
except:
    pass

if models_summary:
    df_summary = pd.DataFrame(models_summary)
    
    # Chart 1: Train vs Test Accuracy Comparison
    x = np.arange(len(df_summary))
    width = 0.35
    
    axes[0, 0].bar(x - width/2, df_summary['Train Acc'], width, label='Training', color='#4CAF50')
    axes[0, 0].bar(x + width/2, df_summary['Test Acc'], width, label='Test', color='#2196F3')
    axes[0, 0].set_ylabel('Accuracy (%)')
    axes[0, 0].set_title('All Models: Training vs Test Accuracy')
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(df_summary['Model'])
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_ylim([0, 100])
    
    # Chart 2: Cross-Validation Mean Accuracy
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']
    axes[0, 1].bar(df_summary['Model'], df_summary['CV Mean'], color=colors)
    axes[0, 1].errorbar(df_summary['Model'], df_summary['CV Mean'], 
                        yerr=df_summary['CV Std'], fmt='none', color='black', capsize=5)
    axes[0, 1].set_ylabel('Accuracy (%)')
    axes[0, 1].set_title('Cross-Validation Mean Accuracy (± Std)')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].set_ylim([0, 100])
    
    # Chart 3: Overfitting Analysis
    overfit = df_summary['Train Acc'] - df_summary['Test Acc']
    colors_overfit = ['red' if x > 5 else 'orange' if x > 2 else 'green' for x in overfit]
    axes[1, 0].bar(df_summary['Model'], overfit, color=colors_overfit)
    axes[1, 0].axhline(5, color='red', linestyle='--', label='High Overfitting (>5%)')
    axes[1, 0].axhline(2, color='orange', linestyle='--', label='Moderate (>2%)')
    axes[1, 0].set_ylabel('Train Acc - Test Acc (%)')
    axes[1, 0].set_title('Overfitting Analysis')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Chart 4: Summary Table
    axes[1, 1].axis('tight')
    axes[1, 1].axis('off')
    
    table_data = []
    for _, row in df_summary.iterrows():
        table_data.append([
            row['Model'],
            f"{row['Train Acc']:.2f}%",
            f"{row['Test Acc']:.2f}%",
            f"{row['CV Mean']:.2f}% ± {row['CV Std']:.2f}%"
        ])
    
    table = axes[1, 1].table(cellText=table_data,
                            colLabels=['Model', 'Train Acc', 'Test Acc', 'CV Score'],
                            cellLoc='center',
                            loc='center',
                            colColours=['#f0f0f0']*4)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    axes[1, 1].set_title('Model Performance Summary', pad=20)

plt.tight_layout()
plt.savefig('model_comparison_detailed.png', dpi=300, bbox_inches='tight')
print("✅ Comparison chart saved as 'model_comparison_detailed.png'")

print("\n" + "="*70)
print("✅ ALL TRAINING & VALIDATION CHARTS GENERATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated files:")
print("1. training_validation_charts.png - 12-panel training analysis")
print("2. model_comparison_detailed.png - Model comparison summary")
print("\nCharts include:")
print("- Training vs Test accuracy")
print("- Feature importance")
print("- 5-fold cross-validation scores")
print("- Learning curves")
print("- Overfitting analysis")
print("- Model comparison table")
