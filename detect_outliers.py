import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("OUTLIER DETECTION SA EDULIFT DATASETS")
print("="*70)

def detect_outliers_iqr(data, column_name):
    """Detect outliers using IQR method"""
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_fence = Q1 - 1.5 * IQR
    upper_fence = Q3 + 1.5 * IQR
    
    outliers = data[(data < lower_fence) | (data > upper_fence)]
    
    return {
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'lower_fence': lower_fence,
        'upper_fence': upper_fence,
        'outliers': outliers,
        'outlier_count': len(outliers),
        'outlier_percentage': (len(outliers) / len(data)) * 100
    }

# 1. EDUCATION DATASET
print("\n1. EDUCATION DATASET OUTLIERS")
print("-" * 70)

try:
    edu_df = pd.read_csv('education_dataset.csv')
    
    # Check programs per field
    if 'field' in edu_df.columns:
        field_counts = edu_df['field'].value_counts()
        
        result = detect_outliers_iqr(field_counts, 'field')
        
        print(f"Programs per Field Statistics:")
        print(f"  Q1: {result['Q1']:.2f}")
        print(f"  Q3: {result['Q3']:.2f}")
        print(f"  IQR: {result['IQR']:.2f}")
        print(f"  Lower Fence: {result['lower_fence']:.2f}")
        print(f"  Upper Fence: {result['upper_fence']:.2f}")
        print(f"\n  Outliers Found: {result['outlier_count']}")
        print(f"  Outlier %: {result['outlier_percentage']:.1f}%")
        
        if result['outlier_count'] > 0:
            print(f"\n  📊 Outlier Fields:")
            for field, count in result['outliers'].items():
                if count < result['lower_fence']:
                    print(f"    ❌ {field}: {count} programs (TOO LOW)")
                else:
                    print(f"    ⭐ {field}: {count} programs (TOO HIGH)")
        else:
            print(f"\n  ✅ No outliers detected!")
    
    # Check programs per type
    if 'program_type' in edu_df.columns:
        type_counts = edu_df['program_type'].value_counts()
        
        result = detect_outliers_iqr(type_counts, 'program_type')
        
        print(f"\nPrograms per Type Statistics:")
        print(f"  Outliers Found: {result['outlier_count']}")
        
        if result['outlier_count'] > 0:
            print(f"\n  📊 Outlier Types:")
            for ptype, count in result['outliers'].items():
                print(f"    ⭐ {ptype}: {count} programs")
                
except FileNotFoundError:
    print("Education dataset not found")

# 2. CAREER DATASET
print("\n2. CAREER DATASET OUTLIERS")
print("-" * 70)

try:
    career_df = pd.read_csv('career_dataset.csv')
    
    # Check careers per field
    if 'field' in career_df.columns:
        field_counts = career_df['field'].value_counts()
        
        result = detect_outliers_iqr(field_counts, 'field')
        
        print(f"Careers per Field Statistics:")
        print(f"  IQR: {result['IQR']:.2f}")
        print(f"  Outliers Found: {result['outlier_count']}")
        
        if result['outlier_count'] > 0:
            print(f"\n  📊 Outlier Fields:")
            for field, count in result['outliers'].items():
                if count < result['lower_fence']:
                    print(f"    ❌ {field}: {count} careers (TOO LOW)")
                else:
                    print(f"    ⭐ {field}: {count} careers (TOO HIGH)")
    
    # Check salary outliers
    if 'salary_min' in career_df.columns:
        salaries = career_df['salary_min'].dropna()
        
        result = detect_outliers_iqr(salaries, 'salary')
        
        print(f"\nSalary Outliers:")
        print(f"  Q1: ₱{result['Q1']:,.0f}")
        print(f"  Q3: ₱{result['Q3']:,.0f}")
        print(f"  IQR: ₱{result['IQR']:,.0f}")
        print(f"  Lower Fence: ₱{result['lower_fence']:,.0f}")
        print(f"  Upper Fence: ₱{result['upper_fence']:,.0f}")
        print(f"\n  Outliers Found: {result['outlier_count']}")
        
        if result['outlier_count'] > 0:
            print(f"\n  💰 Salary Outliers:")
            for idx, salary in result['outliers'].items():
                career_name = career_df.loc[idx, 'career_title']
                if salary < result['lower_fence']:
                    print(f"    ❌ {career_name}: ₱{salary:,.0f} (TOO LOW)")
                else:
                    print(f"    ⭐ {career_name}: ₱{salary:,.0f} (TOO HIGH)")
                    
except FileNotFoundError:
    print("Career dataset not found")

# 3. TESDA DATASET
print("\n3. TESDA DATASET OUTLIERS")
print("-" * 70)

try:
    tesda_df = pd.read_csv('tesda_dataset.csv')
    
    # Check courses per sector
    if 'sector' in tesda_df.columns:
        sector_counts = tesda_df['sector'].value_counts()
        
        result = detect_outliers_iqr(sector_counts, 'sector')
        
        print(f"Courses per Sector Statistics:")
        print(f"  IQR: {result['IQR']:.2f}")
        print(f"  Outliers Found: {result['outlier_count']}")
        
        if result['outlier_count'] > 0:
            print(f"\n  📊 Outlier Sectors:")
            for sector, count in result['outliers'].items():
                if count < result['lower_fence']:
                    print(f"    ❌ {sector}: {count} courses (TOO LOW)")
                else:
                    print(f"    ⭐ {sector}: {count} courses (TOO HIGH)")
                    
except FileNotFoundError:
    print("TESDA dataset not found")

# 4. MODEL ACCURACY OUTLIERS
print("\n4. MODEL ACCURACY OUTLIERS")
print("-" * 70)

accuracies = np.array([87, 83, 88])  # Career, Education, TESDA

Q1 = np.percentile(accuracies, 25)
Q3 = np.percentile(accuracies, 75)
IQR = Q3 - Q1

lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR

print(f"Model Accuracy Statistics:")
print(f"  Q1: {Q1:.1f}%")
print(f"  Q3: {Q3:.1f}%")
print(f"  IQR: {IQR:.1f}%")
print(f"  Lower Fence: {lower_fence:.1f}%")
print(f"  Upper Fence: {upper_fence:.1f}%")

outliers = accuracies[(accuracies < lower_fence) | (accuracies > upper_fence)]
if len(outliers) > 0:
    print(f"\n  ⚠️ Outlier Accuracies: {outliers}")
else:
    print(f"\n  ✅ No model accuracy outliers!")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
✅ Good Outliers: Exceptionally high values (e.g., high salary)
❌ Bad Outliers: Unusually low values (e.g., too few programs)

📝 What to do with outliers:
1. INVESTIGATE: Why are they different?
2. VERIFY: Are they real or errors?
3. DECIDE: Keep, remove, or adjust?

⚠️ For ML models:
   • Outliers can improve learning (real variations)
   • Outliers can hurt accuracy (noise/errors)
""")

print("="*70)