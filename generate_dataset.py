# generate_datasets.py
import csv
import random

# helper lists
industries = ["tech","business","health","education","creative","service","trade","logistics","hospitality","agriculture"]
work_envs = ["office","remote","field","hybrid"]
salary_bands = ["15k-25k","25k-40k","40k-60k","60k+"]

# a big curated list of career titles (short sample here; script expands permutations)
base_jobs = [
    "IT Support Specialist","Junior Web Developer","Frontend Developer","Backend Developer","Fullstack Developer",
    "Data Analyst","Data Scientist","Machine Learning Engineer","QA Engineer","DevOps Engineer",
    "System Administrator","Network Technician","Technical Writer","Digital Marketing Specialist","SEO Specialist",
    "Graphic Designer","UI/UX Designer","Video Editor","Content Creator","Social Media Manager",
    "Accountant","Bookkeeper","HR Coordinator","Customer Service Representative","Sales Associate",
    "Nurse","Medical Technologist","Pharmacy Assistant","Caregiver","Dental Assistant",
    "Electrician","Plumber","Automotive Technician","Welder","Carpenter",
    "Cook","Baker","Restaurant Supervisor","Hotel Front Desk","Housekeeping Supervisor",
    "Teacher (Primary)","Teacher (Secondary)","Guidance Counselor","Education Coordinator","Library Assistant",
    "Logistics Coordinator","Warehouse Staff","Supply Chain Analyst","Procurement Officer","Dispatcher"
]

growth_levels = ["Low","Medium","High"]

def gen_career_rows(n=200):
    rows = []
    job_pool = base_jobs.copy()
    # expand job pool by creating variants
    for j in base_jobs:
        job_pool.append(j + " I")
        job_pool.append("Senior " + j)
        job_pool.append(j + " (Entry Level)")

    while len(rows) < n:
        job = random.choice(job_pool)
        industry = random.choice(industries)
        skills = random.choice(["communication","technical","problem-solving","creative","service","hands-on"])
        salary = random.choice(salary_bands)
        env = random.choice(work_envs)
        growth = random.choice(growth_levels)
        # recommended careers field will contain related titles (comma-separated)
        related = ", ".join(random.sample(job_pool, k=5))
        rows.append([skills, industry, salary, env, job, growth, related])
    return rows

def gen_education_rows(n=120):
    programs = ["STEM Track","ICT Track","ABM Track","HUMSS Track","TVL - Automotive","TVL - ICT","BSIT","BSCS","BSBA","BSEdu","BSN","BSHRM","BSArch","BSCriminology","BSAgri","Diploma - Welding"]
    modalities = ["online","face_to_face","blended","modular"]
    budgets = ["free","low","medium","high"]
    styles = ["visual","reading","hands_on","audio"]
    motivations = ["career_advancement","personal_growth","better_salary","family_support","passion"]
    rows = []
    for _ in range(n):
        prog = random.choice(programs)
        mod = random.choice(modalities)
        bud = random.choice(budgets)
        style = random.choice(styles)
        goal = random.choice(["work in " + random.choice(industries), "become a " + random.choice(["teacher","nurse","engineer","developer","technician"])])
        motivation = random.choice(motivations)
        related = ", ".join(random.sample(programs, k=4))
        rows.append([prog, mod, bud, style, goal, motivation, related])
    return rows

def gen_tesda_rows(n=150):
    courses = [
        "Computer Systems Servicing NC II","Automotive Servicing NC II","Electrical Installation & Maintenance NC II",
        "Shielded Metal Arc Welding NC I","Shielded Metal Arc Welding NC II","Cookery NC II","Bread & Pastry Production NC II",
        "Caregiving NC II","Beauty Care NC II","Hairdressing NC II","Masonry NC I","Carpentry NC II","Plumbing NC II",
        "Welding NC II","Driving NC II","Agricultural Crops Production NC II","Housekeeping NC II","Bartending NC II"
    ]
    budgets = ["free","low","medium","high"]
    times = ["full_time","weekends","evenings","flexible"]
    experiences = ["none","basic","intermediate","advanced"]
    locations = ["Manila","Cebu","Davao","Iloilo","Bacolod","Quezon City","Pasig","Makati","Cagayan de Oro","Baguio"]
    rows = []
    for _ in range(n):
        course = random.choice(courses) + ("" if random.random() > 0.3 else " (Batch)")
        bud = random.choice(budgets)
        time = random.choice(times)
        loc = random.choice(locations)
        exp = random.choice(experiences)
        related = ", ".join(random.sample(courses, k=4))
        rows.append([course, bud, time, loc, exp, related])
    return rows

# write CSVs
with open("career_dataset.csv","w",newline='',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["primary_skills","industry","salary","work_environment","job_title","growth","related_titles"])
    w.writerows(gen_career_rows(250))

with open("education_dataset.csv","w",newline='',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["program_name","modality","budget","learning_style","career_goal","motivation","related_programs"])
    w.writerows(gen_education_rows(140))

with open("tesda_dataset.csv","w",newline='',encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["course_name","budget","time_available","location","experience","related_courses"])
    w.writerows(gen_tesda_rows(180))

print("Datasets generated: career_dataset.csv, education_dataset.csv, tesda_dataset.csv")
