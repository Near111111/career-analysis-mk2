import pandas as pd
import numpy as np

def generate_career_dataset():
    """Generate comprehensive career dataset with more entries"""
    
    careers = []
    
    # Tech Industry
    tech_jobs = [
        ("Software Engineer", "technical", "tech", "60k-80k", "remote", ["programming", "problem-solving", "coding"]),
        ("Data Scientist", "analytical", "tech", "70k-90k", "remote", ["data analysis", "statistics", "python"]),
        ("DevOps Engineer", "technical", "tech", "75k-95k", "hybrid", ["infrastructure", "automation", "coding"]),
        ("Product Manager", "leadership", "tech", "80k-120k", "office", ["leadership", "communication", "strategy"]),
        ("UX Designer", "creative", "tech", "65k-85k", "hybrid", ["design", "creativity", "problem-solving"]),
        ("Frontend Developer", "technical", "tech", "65k-85k", "remote", ["coding", "design", "communication"]),
        ("Backend Developer", "technical", "tech", "70k-90k", "remote", ["coding", "problem-solving", "databases"]),
        ("Mobile Developer", "technical", "tech", "70k-90k", "hybrid", ["coding", "problem-solving", "creativity"]),
        ("Cloud Architect", "technical", "tech", "90k-130k", "hybrid", ["technical", "leadership", "strategy"]),
        ("Security Engineer", "technical", "tech", "80k-110k", "hybrid", ["technical", "problem-solving", "analytical"]),
        ("Machine Learning Engineer", "technical", "tech", "90k-130k", "remote", ["coding", "analytical", "technical"]),
        ("QA Engineer", "analytical", "tech", "60k-80k", "hybrid", ["attention-to-detail", "analytical", "communication"]),
        ("Tech Lead", "leadership", "tech", "85k-120k", "hybrid", ["leadership", "technical", "communication"]),
        ("Solutions Architect", "leadership", "tech", "85k-120k", "hybrid", ["leadership", "technical", "communication"]),
    ]
    
    # Business/Finance
    business_jobs = [
        ("Financial Analyst", "analytical", "business", "60k-80k", "office", ["analytical", "attention-to-detail", "communication"]),
        ("Business Analyst", "analytical", "business", "65k-85k", "hybrid", ["analytical", "communication", "problem-solving"]),
        ("Project Manager", "leadership", "business", "70k-90k", "hybrid", ["leadership", "communication", "organization"]),
        ("Marketing Manager", "creative", "business", "70k-90k", "office", ["communication", "creativity", "leadership"]),
        ("Sales Manager", "leadership", "business", "75k-100k", "office", ["leadership", "communication", "persuasion"]),
        ("Human Resources Manager", "people", "business", "65k-85k", "office", ["communication", "people-skills", "organization"]),
        ("Operations Manager", "leadership", "business", "70k-90k", "office", ["leadership", "organization", "problem-solving"]),
        ("Business Development Manager", "leadership", "business", "75k-110k", "hybrid", ["leadership", "communication", "persuasion"]),
        ("Finance Manager", "analytical", "business", "75k-100k", "office", ["analytical", "attention-to-detail", "leadership"]),
        ("Consultant", "leadership", "business", "80k-120k", "hybrid", ["analytical", "communication", "problem-solving"]),
    ]
    
    # Healthcare
    healthcare_jobs = [
        ("Registered Nurse", "people", "healthcare", "55k-75k", "office", ["people-skills", "attention-to-detail", "problem-solving"]),
        ("Healthcare Administrator", "leadership", "healthcare", "65k-85k", "office", ["leadership", "organization", "communication"]),
        ("Medical Technologist", "analytical", "healthcare", "50k-70k", "office", ["analytical", "attention-to-detail", "technical"]),
        ("Pharmacist", "technical", "healthcare", "90k-120k", "office", ["technical", "attention-to-detail", "communication"]),
        ("Physical Therapist", "people", "healthcare", "75k-95k", "office", ["people-skills", "technical", "problem-solving"]),
        ("Healthcare IT Specialist", "technical", "healthcare", "65k-85k", "hybrid", ["technical", "problem-solving", "communication"]),
        ("Clinical Research Coordinator", "analytical", "healthcare", "55k-75k", "office", ["analytical", "organization", "attention-to-detail"]),
        ("Medical Writer", "creative", "healthcare", "60k-85k", "remote", ["writing", "technical", "communication"]),
    ]
    
    # Education
    education_jobs = [
        ("Teacher", "people", "education", "50k-70k", "office", ["communication", "people-skills", "creativity"]),
        ("Curriculum Developer", "creative", "education", "55k-75k", "hybrid", ["creativity", "organization", "communication"]),
        ("Educational Administrator", "leadership", "education", "65k-85k", "office", ["leadership", "organization", "communication"]),
        ("Instructional Designer", "creative", "education", "60k-80k", "remote", ["creativity", "technical", "communication"]),
        ("Training Specialist", "people", "education", "55k-75k", "hybrid", ["communication", "people-skills", "organization"]),
        ("Academic Advisor", "people", "education", "50k-70k", "office", ["people-skills", "communication", "organization"]),
    ]
    
    # Creative/Arts
    creative_jobs = [
        ("Graphic Designer", "creative", "creative", "50k-70k", "remote", ["design", "creativity", "attention-to-detail"]),
        ("Content Writer", "creative", "creative", "45k-65k", "remote", ["writing", "creativity", "communication"]),
        ("Social Media Manager", "creative", "creative", "50k-70k", "remote", ["communication", "creativity", "analytics"]),
        ("Video Producer", "creative", "creative", "55k-80k", "office", ["creativity", "technical", "problem-solving"]),
        ("UI/UX Designer", "creative", "creative", "65k-85k", "remote", ["design", "creativity", "problem-solving"]),
        ("Copywriter", "creative", "creative", "50k-75k", "remote", ["writing", "creativity", "persuasion"]),
        ("Brand Manager", "creative", "creative", "65k-90k", "office", ["creativity", "communication", "leadership"]),
    ]
    
    # Service Industry
    service_jobs = [
        ("Customer Service Manager", "people", "service", "50k-70k", "office", ["communication", "people-skills", "leadership"]),
        ("Hospitality Manager", "leadership", "service", "45k-65k", "office", ["leadership", "people-skills", "organization"]),
        ("Retail Manager", "leadership", "service", "45k-65k", "office", ["leadership", "communication", "organization"]),
        ("Event Coordinator", "people", "service", "45k-65k", "office", ["organization", "communication", "creativity"]),
        ("Tour Guide", "people", "service", "40k-60k", "office", ["communication", "people-skills", "creativity"]),
    ]
    
    # Skilled Trades
    trade_jobs = [
        ("Construction Manager", "leadership", "trade", "65k-90k", "field", ["leadership", "technical", "problem-solving"]),
        ("Electrician", "technical", "trade", "50k-75k", "field", ["technical", "problem-solving", "attention-to-detail"]),
        ("Plumber", "technical", "trade", "50k-75k", "field", ["technical", "problem-solving", "physical"]),
        ("HVAC Technician", "technical", "trade", "50k-75k", "field", ["technical", "problem-solving", "attention-to-detail"]),
        ("Welder", "technical", "trade", "45k-70k", "field", ["technical", "attention-to-detail", "problem-solving"]),
        ("Carpenter", "technical", "trade", "45k-70k", "field", ["technical", "creativity", "problem-solving"]),
        ("Equipment Operator", "technical", "trade", "50k-75k", "field", ["technical", "attention-to-detail", "safety-conscious"]),
    ]
    
    all_jobs = (tech_jobs + business_jobs + healthcare_jobs + education_jobs + 
                creative_jobs + service_jobs + trade_jobs)
    
    for job_title, skill_type, industry, salary, environment, keywords in all_jobs:
        careers.extend([
            {
                "job_title": job_title,
                "primary_skills": skill,
                "industry": industry,
                "salary": salary,
                "work_environment": environment
            }
            for skill in keywords
        ])
    
    df = pd.DataFrame(careers)
    return df

def generate_education_dataset():
    """Generate comprehensive education dataset"""
    
    programs = []
    
    # Senior High School Programs
    shs_programs = [
        ("STEM Track SHS", "shs", "full_time", "low", "kinesthetic", "career-focused"),
        ("Humanities Track SHS", "shs", "full_time", "low", "visual", "career-focused"),
        ("ABM Track SHS", "shs", "full_time", "low", "auditory", "career-focused"),
        ("Sports Science SHS", "shs", "full_time", "medium", "kinesthetic", "interest-based"),
        ("Arts Track SHS", "shs", "full_time", "medium", "visual", "interest-based"),
    ]
    
    # College Programs - Technology / ICT
    tech_college = [
        ("Bachelor of Science in Computer Science", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Information Technology", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Computer Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Data Science", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Cybersecurity", "college", "full_time", "high", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Business / Management
    business_college = [
        ("Bachelor of Science in Business Administration", "college", "full_time", "high", "auditory", "career-focused"),
        ("Bachelor of Science in Accountancy", "college", "full_time", "high", "auditory", "career-focused"),
        ("Bachelor of Science in Management", "college", "full_time", "high", "auditory", "career-focused"),
        ("Bachelor of Science in Finance", "college", "full_time", "high", "auditory", "career-focused"),
        ("Bachelor of Science in Economics", "college", "full_time", "high", "auditory", "career-focused"),
    ]
    
    # College Programs - Healthcare / Medical
    healthcare_college = [
        ("Bachelor of Science in Nursing", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Pharmacy", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Medical Technology", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Health Sciences", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Physical Therapy", "college", "full_time", "high", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Engineering
    engineering_college = [
        ("Bachelor of Science in Civil Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Mechanical Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Electrical Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Electronics Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Chemical Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Creative / Design
    creative_college = [
        ("Bachelor of Fine Arts", "college", "full_time", "high", "visual", "interest-based"),
        ("Bachelor of Arts in Graphic Design", "college", "full_time", "medium", "visual", "interest-based"),
        ("Bachelor of Arts in Interior Design", "college", "full_time", "medium", "visual", "interest-based"),
        ("Bachelor of Arts in Fashion Design", "college", "full_time", "medium", "visual", "interest-based"),
        ("Bachelor of Arts in Film and Video Production", "college", "full_time", "high", "visual", "interest-based"),
    ]
    
    # College Programs - Education / Teaching
    education_college = [
        ("Bachelor of Arts in Education", "college", "full_time", "medium", "auditory", "career-focused"),
        ("Bachelor of Science in Education - STEM", "college", "full_time", "medium", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Education - Mathematics", "college", "full_time", "medium", "auditory", "career-focused"),
        ("Bachelor of Science in Education - English", "college", "full_time", "medium", "visual", "career-focused"),
        ("Bachelor of Science in Education - Science", "college", "full_time", "medium", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Culinary / Food Service
    culinary_college = [
        ("Bachelor of Science in Culinary Arts", "college", "full_time", "medium", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Food Technology", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Diploma in Culinary Arts", "college", "full_time", "medium", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Construction / Trades
    construction_college = [
        ("Bachelor of Science in Architecture", "college", "full_time", "high", "visual", "career-focused"),
        ("Bachelor of Science in Civil Engineering - Construction", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Certificate in Construction Management", "college", "full_time", "medium", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Agriculture
    agriculture_college = [
        ("Bachelor of Science in Agriculture", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Agronomy", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Agricultural Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Bachelor of Science in Horticulture", "college", "full_time", "medium", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Tourism / Hospitality
    tourism_college = [
        ("Bachelor of Science in Hospitality Management", "college", "full_time", "medium", "auditory", "career-focused"),
        ("Bachelor of Science in Tourism Management", "college", "full_time", "medium", "visual", "career-focused"),
        ("Bachelor of Science in Hotel and Restaurant Management", "college", "full_time", "medium", "auditory", "career-focused"),
        ("Bachelor of Science in Tourism", "college", "full_time", "medium", "visual", "interest-based"),
    ]
    
    # College Programs - Beauty / Wellness
    beauty_college = [
        ("Bachelor of Science in Beauty and Wellness", "college", "full_time", "medium", "kinesthetic", "career-focused"),
        ("Certificate in Cosmetology", "college", "full_time", "medium", "kinesthetic", "career-focused"),
        ("Diploma in Spa and Wellness Management", "college", "full_time", "medium", "auditory", "career-focused"),
    ]
    
    # College Programs - Automotive
    automotive_college = [
        ("Bachelor of Science in Automotive Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Diploma in Automotive Technology", "college", "full_time", "medium", "kinesthetic", "career-focused"),
    ]
    
    # College Programs - Electronics
    electronics_college = [
        ("Bachelor of Science in Electronics Engineering", "college", "full_time", "high", "kinesthetic", "career-focused"),
        ("Diploma in Electronics Technology", "college", "full_time", "medium", "kinesthetic", "career-focused"),
    ]
    
    # Combine all college programs
    college_programs = (tech_college + business_college + healthcare_college + 
                       engineering_college + creative_college + education_college +
                       culinary_college + construction_college + agriculture_college +
                       tourism_college + beauty_college + automotive_college + electronics_college)
    
    # Alternative Learning System (ALS)
    als_programs = [
        ("ALS Accreditation and Equivalency (A&E)", "als", "part_time", "low", "visual", "career-focused"),
        ("ALS Professional Development", "als", "part_time", "medium", "auditory", "career-focused"),
        ("ALS Entrepreneurship", "als", "part_time", "low", "kinesthetic", "interest-based"),
        ("ALS Tech Skills", "als", "part_time", "medium", "kinesthetic", "career-focused"),
        ("ALS Business Skills", "als", "part_time", "medium", "auditory", "career-focused"),
        ("ALS Healthcare Basics", "als", "part_time", "medium", "kinesthetic", "career-focused"),
    ]
    
    # Graduate Programs
    graduate_programs = [
        ("Master of Business Administration (MBA)", "graduate", "full_time", "high", "auditory", "career-focused"),
        ("Master of Science in Computer Science", "graduate", "full_time", "high", "kinesthetic", "career-focused"),
        ("Master of Science in Engineering", "graduate", "full_time", "high", "kinesthetic", "career-focused"),
        ("Master of Science in Information Technology", "graduate", "full_time", "high", "kinesthetic", "career-focused"),
        ("Master of Arts in Education", "graduate", "full_time", "high", "auditory", "career-focused"),
        ("Master of Science in Data Science", "graduate", "full_time", "high", "kinesthetic", "career-focused"),
        ("Master of Science in Nursing", "graduate", "full_time", "high", "kinesthetic", "career-focused"),
        ("Master of Arts in Communication", "graduate", "full_time", "high", "auditory", "interest-based"),
        ("Doctor of Philosophy (PhD) - Technology", "graduate", "full_time", "high", "kinesthetic", "interest-based"),
        ("Doctor of Philosophy (PhD) - Business", "graduate", "full_time", "high", "auditory", "interest-based"),
    ]
    
    all_programs = shs_programs + college_programs + als_programs + graduate_programs
    
    programs_list = []
    for program_name, program_type, modality, budget, learning_style, motivation in all_programs:
        # Create multiple entries to vary the data
        for _ in range(2):
            programs_list.append({
                "program_name": program_name,
                "program_type": program_type,
                "modality": modality,
                "budget": budget,
                "learning_style": learning_style,
                "motivation": motivation
            })
    
    df = pd.DataFrame(programs_list)
    return df

def generate_tesda_dataset():
    """Generate comprehensive TESDA course dataset"""
    
    courses = []
    
    # ICT Courses
    ict_courses = [
        ("Computer Systems Servicing NC II", "ict", "free", "part_time", "makati", "beginner"),
        ("Computer Systems Servicing NC III", "ict", "free", "part_time", "manila", "intermediate"),
        ("Computer Aided Design NC II", "ict", "paid", "full_time", "quezon_city", "intermediate"),
        ("Information and Communications Technology Fundamentals", "ict", "free", "part_time", "manila", "beginner"),
        ("Web Development NC II", "ict", "paid", "full_time", "makati", "intermediate"),
        ("Mobile App Development", "ict", "paid", "part_time", "manila", "intermediate"),
        ("Database Management NC II", "ict", "paid", "full_time", "quezon_city", "intermediate"),
        ("IT Support Services", "ict", "free", "part_time", "manila", "beginner"),
        ("Cybersecurity Fundamentals", "ict", "paid", "full_time", "makati", "intermediate"),
        ("Cloud Computing Basics", "ict", "paid", "part_time", "manila", "intermediate"),
    ]
    
    # Automotive Courses
    automotive_courses = [
        ("Automotive Servicing NC II", "automotive", "free", "full_time", "manila", "beginner"),
        ("Automotive Servicing NC III", "automotive", "paid", "full_time", "makati", "intermediate"),
        ("Automotive Electrical Systems", "automotive", "free", "part_time", "manila", "intermediate"),
        ("Diesel Engine Mechanics", "automotive", "free", "full_time", "quezon_city", "beginner"),
        ("Motorcycle Servicing", "automotive", "free", "part_time", "manila", "beginner"),
    ]
    
    # Construction Courses
    construction_courses = [
        ("Masonry NC II", "construction", "free", "full_time", "manila", "beginner"),
        ("Carpentry NC II", "construction", "free", "full_time", "quezon_city", "beginner"),
        ("Welding NC II", "construction", "free", "full_time", "manila", "beginner"),
        ("Plumbing NC II", "construction", "free", "full_time", "makati", "beginner"),
        ("Heavy Equipment Operation", "construction", "paid", "part_time", "manila", "intermediate"),
    ]
    
    # Electrical Courses
    electrical_courses = [
        ("Electrical Installation NC II", "electrical", "free", "full_time", "manila", "beginner"),
        ("Electrical Installation NC III", "electrical", "paid", "full_time", "quezon_city", "intermediate"),
        ("Solar Photovoltaic Installation", "electrical", "paid", "part_time", "manila", "intermediate"),
        ("Power Distribution Systems", "electrical", "free", "part_time", "makati", "intermediate"),
    ]
    
    # Electronics Courses
    electronics_courses = [
        ("Electronics Assembly and Servicing NC II", "electronics", "free", "full_time", "manila", "beginner"),
        ("Refrigeration and Airconditioning NC II", "electronics", "free", "full_time", "quezon_city", "beginner"),
        ("Electronics Servicing NC III", "electronics", "paid", "full_time", "manila", "intermediate"),
        ("TV and Radio Servicing", "electronics", "free", "part_time", "makati", "beginner"),
    ]
    
    # Food Service Courses
    food_courses = [
        ("Food and Beverage Service NC II", "food", "free", "full_time", "manila", "beginner"),
        ("Bread and Pastry Production NC II", "food", "free", "full_time", "quezon_city", "beginner"),
        ("Commercial Cooking NC II", "food", "free", "full_time", "makati", "beginner"),
        ("Bartending", "food", "paid", "part_time", "manila", "beginner"),
        ("Catering Management", "food", "paid", "part_time", "manila", "intermediate"),
    ]
    
    # Healthcare Courses
    healthcare_courses = [
        ("Health Care Services NC II", "healthcare", "free", "full_time", "manila", "beginner"),
        ("Caregiving NC II", "healthcare", "free", "full_time", "quezon_city", "beginner"),
        ("Nursing Care NC III", "healthcare", "paid", "full_time", "manila", "intermediate"),
        ("Midwifery Orientation", "healthcare", "free", "part_time", "makati", "beginner"),
        ("Medical Massage Therapy", "healthcare", "paid", "part_time", "manila", "intermediate"),
    ]
    
    # Beauty and Personal Care
    beauty_courses = [
        ("Beauty Care NC II", "beauty", "free", "full_time", "manila", "beginner"),
        ("Hairdressing NC II", "beauty", "free", "full_time", "makati", "beginner"),
        ("Nail Care Services", "beauty", "free", "part_time", "manila", "beginner"),
        ("Makeup Artistry", "beauty", "paid", "part_time", "quezon_city", "intermediate"),
        ("Spa and Wellness Services", "beauty", "paid", "full_time", "manila", "intermediate"),
    ]
    
    # Agriculture Courses
    agriculture_courses = [
        ("Agriculture Training NC II", "agriculture", "free", "full_time", "manila", "beginner"),
        ("Horticulture NC II", "agriculture", "free", "full_time", "quezon_city", "beginner"),
        ("Livestock Production", "agriculture", "free", "part_time", "manila", "beginner"),
        ("Organic Farming", "agriculture", "paid", "part_time", "makati", "intermediate"),
        ("Aquaculture Basics", "agriculture", "free", "part_time", "manila", "beginner"),
    ]
    
    all_courses = (ict_courses + automotive_courses + construction_courses + 
                   electrical_courses + electronics_courses + food_courses + 
                   healthcare_courses + beauty_courses + agriculture_courses)
    
    for course_name, interest, budget, time, location, exp in all_courses:
        for _ in range(2):  # Duplicate for more variety
            courses.append({
                "course_name": course_name,
                "course_interest": interest,
                "budget": budget,
                "time_available": time,
                "location": location,
                "experience": exp
            })
    
    df = pd.DataFrame(courses)
    return df

if __name__ == "__main__":
    print("Generating expanded datasets...")
    
    # Generate career dataset
    career_df = generate_career_dataset()
    career_df.to_csv('career_dataset.csv', index=False)
    print(f"✅ Career dataset: {len(career_df)} entries")
    
    # Generate education dataset
    education_df = generate_education_dataset()
    education_df.to_csv('education_dataset.csv', index=False)
    print(f"✅ Education dataset: {len(education_df)} entries")
    
    # Generate TESDA dataset
    tesda_df = generate_tesda_dataset()
    tesda_df.to_csv('tesda_dataset.csv', index=False)
    print(f"✅ TESDA dataset: {len(tesda_df)} entries")
    
    print("\n✨ All datasets generated successfully!")
    print("Run: python train_model.py")
