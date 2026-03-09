"""
Locale-specific reference data for employment, national IDs,
payment methods, phone carriers, and more.
"""

from __future__ import annotations

# --- Job titles by industry ---
JOB_TITLES: dict[str, list[str]] = {
    "tech": [
        "Software Engineer", "Senior Developer", "Tech Lead", "CTO", "DevOps Engineer",
        "Data Scientist", "Product Manager", "UX Designer", "QA Engineer", "System Architect",
        "Frontend Developer", "Backend Developer", "ML Engineer", "Security Analyst",
        "Cloud Engineer", "Mobile Developer", "Engineering Manager", "Scrum Master",
        "Database Administrator", "Site Reliability Engineer",
    ],
    "finance": [
        "Financial Analyst", "Investment Banker", "Portfolio Manager", "Risk Analyst",
        "Compliance Officer", "Auditor", "CFO", "Accountant", "Tax Advisor", "Trader",
        "Credit Analyst", "Wealth Manager", "Fund Manager", "Actuary", "Treasury Analyst",
        "Loan Officer", "Controller", "Financial Planner", "Underwriter", "Claims Adjuster",
    ],
    "health": [
        "Doctor", "Nurse", "Pharmacist", "Lab Technician", "Surgeon", "Dentist",
        "Radiologist", "Physical Therapist", "Anesthesiologist", "Paramedic",
        "Clinical Research Associate", "Hospital Administrator", "Dietician",
        "Optometrist", "Psychiatrist", "Veterinarian", "Biomedical Engineer",
        "Public Health Analyst", "Medical Coder", "Nursing Assistant",
    ],
    "retail": [
        "Store Manager", "Sales Associate", "Visual Merchandiser", "Buyer",
        "Inventory Manager", "District Manager", "Cashier", "Loss Prevention Officer",
        "E-commerce Manager", "Supply Chain Analyst", "Brand Manager",
        "Customer Service Representative", "Warehouse Manager", "Logistics Coordinator",
        "Retail Analyst", "Category Manager", "Area Sales Manager", "Floor Supervisor",
        "Personal Shopper", "Procurement Specialist",
    ],
    "food": [
        "Head Chef", "Sous Chef", "Line Cook", "Restaurant Manager", "Pastry Chef",
        "Food Safety Inspector", "Sommelier", "Barista", "Nutritionist",
        "Food Scientist", "Kitchen Manager", "Catering Manager", "Bartender",
        "Food Photographer", "Menu Developer", "Quality Control Manager",
        "Supply Chain Manager", "Brand Ambassador", "Franchise Manager", "Baker",
    ],
    "manufacturing": [
        "Production Manager", "Quality Engineer", "Plant Manager", "Process Engineer",
        "Mechanical Engineer", "Safety Manager", "Operations Director", "Maintenance Technician",
        "Supply Chain Manager", "Industrial Designer", "Tooling Engineer",
        "Production Planner", "Assembly Line Supervisor", "Welder", "CNC Operator",
        "Automation Engineer", "Lean Specialist", "Materials Manager",
        "Environmental Health Officer", "Electrical Engineer",
    ],
}

# General / cross-industry titles
JOB_TITLES["general"] = [
    "CEO", "COO", "VP Operations", "HR Manager", "Marketing Director",
    "Office Manager", "Executive Assistant", "Receptionist", "Legal Counsel",
    "Business Analyst", "Project Manager", "Communications Director",
    "Administrative Assistant", "Consultant", "Intern", "Freelancer",
    "Sales Director", "Training Manager", "IT Support", "Janitor",
]

# --- Department names ---
DEPARTMENTS = [
    "Engineering", "Finance", "Human Resources", "Marketing", "Sales",
    "Operations", "Legal", "Customer Support", "Research & Development",
    "Quality Assurance", "Product", "Design", "IT", "Procurement",
    "Administration", "Strategy", "Business Development", "Compliance",
]

# --- Salary ranges by locale (annual, in local currency) ---
SALARY_RANGES: dict[str, tuple[float, float, float]] = {
    # (low, median, high)
    "US": (35000, 65000, 200000),
    "JP": (3000000, 5500000, 15000000),
    "DE": (30000, 52000, 140000),
    "BR": (24000, 60000, 240000),
    "IN": (300000, 800000, 3500000),
    "GB": (25000, 42000, 130000),
    "FR": (28000, 45000, 120000),
    "KR": (30000000, 50000000, 120000000),
    "ES": (20000, 33000, 90000),
    "SA": (60000, 144000, 480000),
    "NG": (1200000, 4800000, 18000000),
}

# --- National ID formats ---
# '#' = digit, '?' = letter, '*' = alphanumeric
NATIONAL_ID_FORMATS: dict[str, dict[str, str]] = {
    "US": {"name": "SSN", "format": "###-##-####"},
    "JP": {"name": "My Number", "format": "#### #### ####"},
    "DE": {"name": "Personalausweis", "format": "?#########"},
    "BR": {"name": "CPF", "format": "###.###.###-##"},
    "IN": {"name": "Aadhaar", "format": "#### #### ####"},
    "GB": {"name": "NI Number", "format": "?? ## ## ## ?"},
    "FR": {"name": "INSEE", "format": "# ## ## ?? ### ###"},
    "KR": {"name": "RRN", "format": "######-#######"},
    "ES": {"name": "DNI", "format": "########?"},
    "SA": {"name": "National ID", "format": "##########"},
    "NG": {"name": "NIN", "format": "###########"},
}

# --- Payment methods by locale ---
PAYMENT_METHODS: dict[str, list[tuple[str, float]]] = {
    # (method_name, weight)
    "US": [("Credit Card", 40), ("Debit Card", 25), ("Zelle", 12), ("Venmo", 8), ("PayPal", 10), ("Cash", 5)],
    "JP": [("Credit Card", 30), ("Cash", 25), ("PayPay", 15), ("Suica/IC Card", 12), ("Debit Card", 8), ("Bank Transfer", 10)],
    "DE": [("Bank Transfer", 30), ("Cash", 20), ("EC Card", 20), ("PayPal", 15), ("Credit Card", 10), ("Klarna", 5)],
    "BR": [("Pix", 40), ("Credit Card", 25), ("Debit Card", 15), ("Boleto", 12), ("Cash", 8)],
    "IN": [("UPI", 45), ("Debit Card", 15), ("Credit Card", 12), ("Net Banking", 10), ("Cash", 10), ("Wallet", 8)],
    "GB": [("Debit Card", 35), ("Credit Card", 25), ("Bank Transfer", 15), ("Apple Pay", 10), ("PayPal", 10), ("Cash", 5)],
    "FR": [("Credit Card", 35), ("Bank Transfer", 20), ("Cash", 15), ("PayPal", 12), ("Cheque", 10), ("Apple Pay", 8)],
    "KR": [("Credit Card", 40), ("Samsung Pay", 15), ("Kakao Pay", 15), ("Bank Transfer", 12), ("Naver Pay", 10), ("Cash", 8)],
    "ES": [("Credit Card", 30), ("Debit Card", 25), ("Bank Transfer", 20), ("Bizum", 12), ("Cash", 8), ("PayPal", 5)],
    "SA": [("Mada Card", 35), ("Credit Card", 25), ("STC Pay", 15), ("Bank Transfer", 15), ("Cash", 10)],
    "NG": [("Bank Transfer", 30), ("POS/Debit Card", 20), ("Cash", 20), ("Opay", 12), ("Mobile Money", 10), ("USSD", 8)],
}

# --- Phone carriers by locale ---
PHONE_CARRIERS: dict[str, list[str]] = {
    "US": ["Verizon", "AT&T", "T-Mobile", "Mint Mobile", "Cricket", "Visible"],
    "JP": ["NTT Docomo", "au (KDDI)", "SoftBank", "Rakuten Mobile", "Y!mobile", "UQ Mobile"],
    "DE": ["Telekom", "Vodafone", "O2", "1&1", "Congstar", "ALDI TALK"],
    "BR": ["Vivo", "Claro", "TIM", "Oi", "Algar Telecom"],
    "IN": ["Jio", "Airtel", "Vi (Vodafone Idea)", "BSNL", "MTNL"],
    "GB": ["EE", "Vodafone UK", "Three", "O2 UK", "Sky Mobile", "Tesco Mobile"],
    "FR": ["Orange", "SFR", "Bouygues Telecom", "Free Mobile", "La Poste Mobile"],
    "KR": ["SK Telecom", "KT", "LG U+"],
    "ES": ["Movistar", "Vodafone", "Orange", "MásMóvil", "Yoigo"],
    "SA": ["STC", "Mobily", "Zain", "Virgin Mobile SA"],
    "NG": ["MTN Nigeria", "Airtel Nigeria", "Glo", "9mobile"],
}

# --- Tax ID formats (company) ---
TAX_ID_FORMATS: dict[str, dict[str, str]] = {
    "US": {"name": "EIN", "format": "##-#######"},
    "JP": {"name": "Corporate Number", "format": "#############"},
    "DE": {"name": "USt-IdNr", "format": "DE#########"},
    "BR": {"name": "CNPJ", "format": "##.###.###/####-##"},
    "IN": {"name": "GSTIN", "format": "##?????####?#??"},
    "GB": {"name": "VAT Number", "format": "GB### #### ##"},
    "FR": {"name": "SIRET", "format": "### ### ### #####"},
    "KR": {"name": "BRN", "format": "###-##-#####"},
    "ES": {"name": "NIF", "format": "?########"},
    "SA": {"name": "Tax Number", "format": "###############"},
    "NG": {"name": "TIN", "format": "##########-####"},
}

# --- Credit card preferences by locale ---
CREDIT_CARD_TYPES: dict[str, list[tuple[str, float]]] = {
    "US": [("Visa", 40), ("Mastercard", 30), ("Amex", 15), ("Discover", 10), ("Other", 5)],
    "JP": [("JCB", 35), ("Visa", 30), ("Mastercard", 20), ("Amex", 10), ("Diners", 5)],
    "DE": [("Visa", 35), ("Mastercard", 35), ("Girocard", 20), ("Amex", 10)],
    "BR": [("Visa", 35), ("Mastercard", 30), ("Elo", 25), ("Amex", 5), ("Hipercard", 5)],
    "IN": [("Visa", 30), ("Mastercard", 25), ("RuPay", 35), ("Amex", 5), ("Diners", 5)],
    "GB": [("Visa", 45), ("Mastercard", 40), ("Amex", 10), ("Other", 5)],
    "FR": [("Visa", 45), ("Mastercard", 35), ("Carte Bancaire", 10), ("Amex", 10)],
    "KR": [("Samsung Card", 20), ("Shinhan Card", 20), ("KB Card", 20), ("Visa", 15), ("Mastercard", 15), ("Amex", 10)],
    "ES": [("Visa", 45), ("Mastercard", 40), ("Amex", 10), ("Other", 5)],
    "SA": [("Visa", 35), ("Mastercard", 35), ("Mada", 25), ("Amex", 5)],
    "NG": [("Visa", 40), ("Mastercard", 35), ("Verve", 20), ("Amex", 5)],
}

# --- Height/Weight ranges by locale (cm, kg) ---
BIOMETRICS: dict[str, dict[str, tuple[float, float, float]]] = {
    # (low, mean, high) for each
    "US": {"height_m": (165, 177, 193), "height_f": (152, 163, 175), "weight_m": (65, 90, 120), "weight_f": (50, 75, 105)},
    "JP": {"height_m": (160, 172, 184), "height_f": (148, 158, 170), "weight_m": (55, 70, 90), "weight_f": (42, 55, 72)},
    "DE": {"height_m": (170, 180, 195), "height_f": (158, 167, 180), "weight_m": (68, 85, 110), "weight_f": (52, 70, 95)},
    "BR": {"height_m": (163, 174, 188), "height_f": (152, 161, 174), "weight_m": (60, 78, 100), "weight_f": (48, 65, 88)},
    "IN": {"height_m": (158, 170, 183), "height_f": (148, 157, 168), "weight_m": (52, 70, 92), "weight_f": (42, 58, 78)},
    "GB": {"height_m": (168, 178, 192), "height_f": (155, 164, 176), "weight_m": (65, 84, 110), "weight_f": (50, 72, 98)},
    "FR": {"height_m": (168, 178, 190), "height_f": (155, 165, 176), "weight_m": (63, 80, 105), "weight_f": (48, 65, 88)},
    "KR": {"height_m": (165, 175, 187), "height_f": (153, 162, 173), "weight_m": (58, 73, 95), "weight_f": (44, 57, 75)},
    "ES": {"height_m": (165, 176, 190), "height_f": (155, 163, 176), "weight_m": (62, 80, 105), "weight_f": (48, 65, 88)},
    "SA": {"height_m": (163, 174, 188), "height_f": (150, 160, 172), "weight_m": (60, 82, 110), "weight_f": (48, 68, 95)},
    "NG": {"height_m": (162, 172, 186), "height_f": (150, 160, 172), "weight_m": (55, 73, 98), "weight_f": (45, 65, 90)},
}

# --- University names by locale ---
UNIVERSITIES: dict[str, list[str]] = {
    "US": [
        "MIT", "Stanford", "Harvard", "UC Berkeley", "Georgia Tech", "UT Austin",
        "University of Michigan", "UCLA", "Columbia", "NYU", "Ohio State",
        "Penn State", "University of Florida", "University of Washington",
        "Carnegie Mellon", "Duke", "Caltech", "Northwestern", "USC", "Purdue",
    ],
    "JP": [
        "東京大学", "京都大学", "大阪大学", "東北大学", "名古屋大学", "九州大学",
        "北海道大学", "早稲田大学", "慶應義塾大学", "東京工業大学", "筑波大学",
        "一橋大学", "上智大学", "明治大学", "同志社大学", "立命館大学",
    ],
    "DE": [
        "TU München", "LMU München", "Heidelberg", "Humboldt Berlin", "TU Berlin",
        "RWTH Aachen", "Universität Freiburg", "Universität Hamburg", "TU Dresden",
        "Universität Bonn", "Universität Göttingen", "Universität Köln",
    ],
    "BR": [
        "USP", "UNICAMP", "UFRJ", "UFMG", "UFRGS", "UnB", "UFPE", "UFSC",
        "PUC-Rio", "FGV", "Insper", "UFPR", "UFC", "UNESP", "UFBA",
    ],
    "IN": [
        "IIT Bombay", "IIT Delhi", "IIT Madras", "IIT Kanpur", "IISc Bangalore",
        "BITS Pilani", "IIT Kharagpur", "IIT Roorkee", "NIT Trichy", "Delhi University",
        "JNU", "Anna University", "Jadavpur University", "VIT", "Manipal",
        "Amity University", "Symbiosis", "Christ University", "SRM", "KIIT",
    ],
    "GB": [
        "Oxford", "Cambridge", "Imperial College", "UCL", "Edinburgh", "Manchester",
        "King's College London", "LSE", "Bristol", "Warwick", "Glasgow", "Leeds",
        "Durham", "Birmingham", "Nottingham", "Sheffield", "Southampton", "Exeter",
    ],
    "FR": [
        "Sorbonne", "École Polytechnique", "ENS Paris", "HEC Paris", "Sciences Po",
        "INSEAD", "Université Paris-Saclay", "Université de Lyon", "Université de Strasbourg",
        "Université de Bordeaux", "Centrale Paris", "ESSEC", "EDHEC",
    ],
    "KR": [
        "서울대학교", "KAIST", "연세대학교", "고려대학교", "포항공과대학교",
        "성균관대학교", "한양대학교", "서강대학교", "중앙대학교", "경희대학교",
        "이화여자대학교", "건국대학교", "동국대학교", "홍익대학교",
    ],
    "ES": [
        "Universidad Complutense", "Universidad de Barcelona", "Universidad Autónoma de Madrid",
        "Universidad de Salamanca", "Universidad de Valencia", "Universidad de Sevilla",
        "Universidad de Granada", "IE University", "ESADE", "Universidad Carlos III",
    ],
    "SA": [
        "King Saud University", "KAUST", "King Abdulaziz University",
        "King Fahd University", "Imam Muhammad University", "Princess Nourah University",
        "Umm Al-Qura University", "Taibah University", "King Khalid University",
    ],
    "NG": [
        "University of Lagos", "University of Ibadan", "Obafemi Awolowo University",
        "University of Nigeria Nsukka", "Ahmadu Bello University", "Covenant University",
        "University of Benin", "Lagos State University", "University of Ilorin",
        "Babcock University", "University of Port Harcourt", "FUTA",
    ],
}

DEGREE_TYPES = [
    ("Bachelor's", 55), ("Master's", 25), ("PhD", 5), ("Associate's", 10), ("Diploma", 5),
]

DEGREE_FIELDS = [
    "Computer Science", "Business Administration", "Engineering", "Economics",
    "Medicine", "Law", "Psychology", "Mathematics", "Physics", "Chemistry",
    "Biology", "English Literature", "History", "Political Science", "Accounting",
    "Marketing", "Finance", "Architecture", "Design", "Education",
    "Electrical Engineering", "Mechanical Engineering", "Civil Engineering",
    "Pharmacy", "Nursing", "Communication", "Sociology", "Philosophy",
]

# --- Vehicle data by locale ---
CAR_BRANDS: dict[str, list[tuple[str, float]]] = {
    "US": [("Ford", 18), ("Chevrolet", 15), ("Toyota", 14), ("Honda", 12), ("Tesla", 8), ("Jeep", 7), ("Nissan", 6), ("Hyundai", 5), ("BMW", 5), ("Ram", 5), ("Subaru", 5)],
    "JP": [("Toyota", 30), ("Honda", 18), ("Nissan", 12), ("Suzuki", 10), ("Mazda", 8), ("Subaru", 6), ("Daihatsu", 6), ("Mitsubishi", 5), ("Lexus", 5)],
    "DE": [("Volkswagen", 22), ("BMW", 12), ("Mercedes-Benz", 12), ("Audi", 10), ("Opel", 8), ("Ford", 7), ("Skoda", 6), ("Hyundai", 5), ("Toyota", 5), ("Seat", 5), ("Porsche", 4), ("Mini", 4)],
    "BR": [("Fiat", 22), ("Volkswagen", 18), ("Chevrolet", 16), ("Hyundai", 12), ("Toyota", 10), ("Renault", 8), ("Honda", 6), ("Jeep", 5), ("Nissan", 3)],
    "IN": [("Maruti Suzuki", 35), ("Hyundai", 18), ("Tata", 15), ("Mahindra", 10), ("Kia", 8), ("Toyota", 5), ("Honda", 4), ("MG", 3), ("Renault", 2)],
    "GB": [("Ford", 15), ("Volkswagen", 10), ("Vauxhall", 10), ("BMW", 8), ("Audi", 8), ("Mercedes", 7), ("Toyota", 7), ("Nissan", 6), ("Kia", 6), ("Hyundai", 6), ("Range Rover", 5), ("Mini", 5), ("Tesla", 4), ("Volvo", 3)],
    "FR": [("Peugeot", 20), ("Renault", 18), ("Citroën", 12), ("Dacia", 8), ("Volkswagen", 7), ("Toyota", 7), ("BMW", 5), ("Mercedes", 5), ("Audi", 5), ("Ford", 5), ("Fiat", 4), ("Opel", 4)],
    "KR": [("Hyundai", 35), ("Kia", 30), ("Genesis", 10), ("Samsung (Renault)", 8), ("BMW", 5), ("Mercedes", 5), ("Tesla", 4), ("Audi", 3)],
    "ES": [("Seat", 15), ("Volkswagen", 12), ("Peugeot", 10), ("Renault", 10), ("Toyota", 8), ("Citroën", 7), ("Ford", 7), ("Hyundai", 6), ("Kia", 6), ("BMW", 5), ("Dacia", 5), ("Audi", 5), ("Mercedes", 4)],
    "SA": [("Toyota", 30), ("Hyundai", 15), ("Nissan", 10), ("Ford", 8), ("Chevrolet", 8), ("Kia", 7), ("Honda", 6), ("Lexus", 5), ("BMW", 5), ("Mercedes", 6)],
    "NG": [("Toyota", 35), ("Honda", 15), ("Mercedes-Benz", 10), ("Lexus", 10), ("Hyundai", 8), ("Kia", 6), ("Ford", 5), ("Nissan", 5), ("Innoson", 3), ("Peugeot", 3)],
}

# --- Insurance providers by locale ---
INSURANCE_PROVIDERS: dict[str, list[str]] = {
    "US": ["Blue Cross", "UnitedHealth", "Aetna", "Cigna", "Humana", "Kaiser Permanente"],
    "JP": ["National Health Insurance", "Social Insurance", "Zenkyoren", "Nippon Life"],
    "DE": ["TK", "AOK", "Barmer", "DAK", "IKK", "Allianz Private"],
    "BR": ["SUS", "Amil", "Bradesco Saúde", "SulAmérica", "Unimed", "Hapvida"],
    "IN": ["LIC", "Star Health", "HDFC Ergo", "ICICI Lombard", "Max Bupa", "Ayushman Bharat"],
    "GB": ["NHS", "Bupa", "AXA Health", "Vitality", "Aviva", "Nuffield Health"],
    "FR": ["Sécurité Sociale", "Harmonie Mutuelle", "MGEN", "AXA", "Groupama", "Malakoff Humanis"],
    "KR": ["National Health Insurance", "Samsung Life", "Hanwha Life", "Kyobo Life"],
    "ES": ["Seguridad Social", "Sanitas", "Adeslas", "Mapfre", "DKV", "Asisa"],
    "SA": ["Bupa Arabia", "Tawuniya", "Medgulf", "Al Rajhi Takaful", "AXA Cooperative"],
    "NG": ["NHIS", "Leadway Health", "Hygeia", "AXA Mansard", "Reliance HMO"],
}
