# fabrikate 🏭

**Contextually coherent mock data generation for Python.**

Generate fake people, companies, products, and transactions where everything makes sense together. A person in Tokyo gets a Japanese name, Japanese phone number, Japanese bank, My Number, a Toyota, and pays via PayPay. A German company has a GmbH suffix, a VAT number, and pays salaries in EUR.

Zero dependencies. Pure Python. 11 locales. Up to 2 million unique names per locale (1,000 first names × 1,000 last names, per gender). 25+ fields per person.

```bash
pip install fabrikate
```

## Quick Start

```python
from fabrikate import World

# Create a world set in India
world = World(locale="hi_IN", seed=42, industry="tech")

# Generate a person — everything is Indian and coherent
person = world.person()
print(person.full_name)        # "Pooja Reddy"
print(person.phone)            # "+91 63794-02654"
print(person.phone_carrier)    # "Airtel"
print(person.national_id)      # "9600 1338 9083" (Aadhaar format)
print(person.salary)           # 1445867.41 (INR)
print(person.credit_card_type) # "RuPay"
print(person.vehicle.brand)    # "Maruti Suzuki"
print(person.medical.blood_type) # "O+"
print(person.education.university) # "IIT Delhi"

# Generate a company with employees
company = world.company()
employees = company.hire(10)

# Generate linked transactions
tx = world.transaction(sender=person, receiver=company)
print(tx.payment_method)  # "UPI"
print(tx.tax_amount)      # 18% GST applied

# Export everything as JSON
print(world.to_json())
```

## Why fabrikate?

**Faker** generates random data — a person might have an American name, a Japanese phone number, and a German address. **fabrikate** keeps everything coherent within a cultural and business context.

| Feature | Faker | fabrikate |
|---------|-------|-----------|
| Random names | ✓ | ✓ |
| Locale-aware formatting | ✓ | ✓ |
| Coherent person (name + phone + bank + address) | ✗ | ✓ |
| Locale-specific payment methods (UPI, Pix, Zelle) | ✗ | ✓ |
| Locale-weighted blood types, car brands, carriers | ✗ | ✓ |
| National ID formats (Aadhaar, SSN, NI Number) | ✗ | ✓ |
| Company → employee context inheritance | ✗ | ✓ |
| Industry-appropriate job titles and salaries | ✗ | ✓ |
| Realistic distributions (log-normal, bell curve) | ✗ | ✓ |
| Linked transactions with tax and invoices | ✗ | ✓ |
| Full relational dataset export | ✗ | ✓ |
| Zero dependencies | ✗ | ✓ |

## Supported Locales

| Code | Country | Currency | Phone | National ID | Top Payment |
|------|---------|----------|-------|-------------|-------------|
| `en_US` | United States | USD ($) | +1 | SSN | Credit Card |
| `ja_JP` | Japan | JPY (¥) | +81 | My Number | Credit Card |
| `de_DE` | Germany | EUR (€) | +49 | Personalausweis | Bank Transfer |
| `pt_BR` | Brazil | BRL (R$) | +55 | CPF | Pix |
| `hi_IN` | India | INR (₹) | +91 | Aadhaar | UPI |
| `en_GB` | United Kingdom | GBP (£) | +44 | NI Number | Debit Card |
| `fr_FR` | France | EUR (€) | +33 | INSEE | Credit Card |
| `ko_KR` | South Korea | KRW (₩) | +82 | RRN | Credit Card |
| `es_ES` | Spain | EUR (€) | +34 | DNI | Credit Card |
| `ar_SA` | Saudi Arabia | SAR (﷼) | +966 | National ID | Mada Card |
| `en_NG` | Nigeria | NGN (₦) | +234 | NIN | Bank Transfer |

Each locale has 1,000 male first names, 1,000 female first names, and 1,000 last names — yielding up to 2 million unique full name combinations (1,000 × 1,000 per gender). Plus 50 cities, locale-specific banks, email domains, company suffixes, street formats, and more.

## Core Concepts

### World

A `World` is your mock data universe. Everything generated within a world shares context and can reference each other.

```python
world = World(
    locale="de_DE",     # Country/culture context
    seed=123,           # Random seed for reproducibility (optional)
    year=2025,          # Reference year for dates and ages
    industry="finance", # Default industry for companies/products
)
```

**Parameters:**

- **`locale`** (str, default `"en_US"`): Determines the cultural context — names, phone formats, currency, banks, addresses, ID formats, payment methods, car brands, blood type distributions, and everything else. Use codes like `"hi_IN"`, `"ja_JP"`, `"de_DE"`.
- **`seed`** (int or None): When set, the same seed always produces identical data. Critical for reproducible test fixtures. `World(seed=42)` will generate the exact same people, companies, and transactions every time.
- **`year`** (int, default `2025`): The reference year. Ages, dates of birth, graduation years, transaction dates, and vehicle model years are all calculated relative to this.
- **`industry`** (str or None): Sets the default industry context. Affects company names, job titles, product names, and salary ranges. Options: `"tech"`, `"finance"`, `"health"`, `"retail"`, `"food"`, `"manufacturing"`.

### Person

A person has 25+ fields, all coherent within the locale:

```python
person = world.person()

# --- Identity ---
person.id                # UUID
person.first_name        # Locale-appropriate first name
person.last_name         # Locale-appropriate last name
person.full_name         # Ordered correctly (family-first in Japan/Korea)
person.gender            # "male" or "female"
person.age               # Bell curve centered at 35
person.date_of_birth     # "1990-03-15" — consistent with age and year
person.nationality       # "India", "Deutschland", "日本", etc.
person.national_id       # Locale format: "9600 1338 9083" (Aadhaar)
person.marital_status    # Age-dependent: "single", "married", "divorced", "widowed"
person.children          # Locale-weighted: higher in Nigeria/Saudi, lower in Japan/Korea

# --- Contact ---
person.email             # Derived from name + locale domain (yahoo.co.jp, gmail.com)
person.phone             # Locale format: "+91 63794-02654"
person.phone_carrier     # "Jio", "Airtel", "Verizon", "Docomo", etc.
person.username          # Derived from name: "pooja.reddy128"
person.address           # Address object with street, city, postal_code, country
person.address.street    # Locale street format: "1675, Nehru Nagar"
person.address.city      # "Pune", "München", "東京"
person.address.postal_code  # Locale format: "559407", "SW1A 1AA"

# --- Financial ---
person.bank              # Locale bank: "HDFC Bank", "三菱UFJ銀行"
person.credit_card_type  # Locale-weighted: "RuPay" in India, "JCB" in Japan
person.salary            # Log-normal distribution, locale-scaled
person.salary_currency   # "INR", "EUR", "USD"

# --- Employment ---
person.job_title         # Industry-appropriate: "Software Engineer", "Portfolio Manager"
person.department        # "Engineering", "Finance", "Marketing"
person.company_id        # Links to company (set by company.hire())

# --- Education ---
person.education.university      # Locale university: "IIT Delhi", "MIT", "東京大学"
person.education.degree          # Weighted: "Bachelor's" (55%), "Master's" (25%), "PhD" (5%)
person.education.field_of_study  # "Computer Science", "Economics", etc.
person.education.graduation_year # Consistent with age and degree type

# --- Vehicle (70% chance) ---
person.vehicle                # None if no vehicle
person.vehicle.brand          # Locale-weighted: "Maruti Suzuki" in India, "Toyota" in Japan
person.vehicle.year           # Recent model year
person.vehicle.plate_number   # Locale format: "CH 16 IO 5255"

# --- Medical ---
person.medical.blood_type          # Real regional distributions (O+ 51% in Nigeria, A+ 40% in Japan)
person.medical.height_cm           # Bell curve by locale and gender
person.medical.weight_kg           # Bell curve by locale and gender
person.medical.insurance_provider  # "Star Health" (India), "NHS" (UK), "Blue Cross" (US)
```

**Override any field:**

```python
# Force specific values
person = world.person(
    gender="female",
    age=30,
    job_title="CEO",
    salary=500000,
)
```

### Company

```python
company = world.company()

company.id               # UUID
company.name             # Industry + locale appropriate: "CloudPrime GmbH"
company.industry         # "tech", "finance", "health", etc.
company.founded_year     # Random year between 1970 and now
company.employee_count   # 5, 12, 25, 50, 100, 250, 500, or 1000
company.currency         # Locale currency
company.bank             # Locale bank
company.city             # Locale city
company.country          # Locale country name
company.tax_id           # Locale format: "DE960013389" (German VAT), "##-#######" (US EIN)
company.annual_revenue   # Scales with employee count, log-normal
company.website          # Derived from company name
company.departments      # List of departments, scales with size
company.employees        # List of hired Person objects
```

**Hiring employees:**

```python
company = world.company(industry="tech")
team = company.hire(10)  # 10 employees linked to this company

for person in team:
    print(person.company_id)  # == company.id
    print(person.job_title)   # Tech job titles
    print(person.address.country)  # Same locale as company
```

### Product

```python
product = world.product(company=company)

product.id          # UUID
product.name        # Industry-appropriate: "Cloud Platform", "Vita Formula"
product.sku         # "CLO-4832"
product.price       # Industry-appropriate range
product.currency    # Locale currency
product.category    # Matches industry
product.company_id  # Links to company
```

### Transaction

```python
tx = world.transaction(sender=person, receiver=company)

tx.id               # UUID
tx.type             # "purchase", "refund", "subscription", "transfer", "payment", "invoice"
tx.amount           # Log-normal: many small, few large
tx.tax_amount       # Locale tax rate applied (18% GST in India, 19% in Germany, 8% in US)
tx.total_amount     # amount + tax
tx.currency         # Locale currency
tx.status           # Weighted: 70% completed, 15% pending, 10% failed, 5% cancelled
tx.date             # Random date within the context year
tx.payment_method   # Locale-weighted: "UPI" (India), "Pix" (Brazil), "EC Card" (Germany)
tx.invoice_number   # "INV-2025-74042"
tx.sender_id        # Links to sender
tx.receiver_id      # Links to receiver
tx.product_id       # Links to product (optional)
tx.description      # Human-readable summary
```

### Context and Child Contexts

The `Context` is the engine behind coherence. You usually don't create one directly — `World` handles it. But you can create child contexts for scenarios like multinational companies:

```python
# Japanese HQ
world = World(locale="ja_JP", seed=42, industry="tech")
hq = world.company()

# American branch — child context overrides locale but inherits industry
us_ctx = world.ctx.child(locale="en_US")
branch_employees = [Person.generate(us_ctx, company_id=hq.id) for _ in range(5)]
# These employees have American names/phones but work for the Japanese company
```

### Full Dataset Export

Everything you generate is tracked and exportable:

```python
world = World(locale="hi_IN", seed=42)
company = world.company(industry="tech")
company.hire(50)
world.products(10, company=company)
world.transactions(200)

# As a Python dict
data = world.dataset()
# {
#   "metadata": {"locale": "hi_IN", "seed": 42, "year": 2025, "industry": None},
#   "people": [...],      # 50 people
#   "companies": [...],   # 1 company
#   "products": [...],    # 10 products
#   "transactions": [...] # 200 transactions
# }

# As a JSON string
json_str = world.to_json(indent=2)

# Write to file
with open("test_fixtures.json", "w") as f:
    f.write(world.to_json())
```

### Overrides

Every generator accepts `**overrides` to force specific values:

```python
# Override person fields
person = world.person(
    first_name="Raj",
    age=28,
    gender="male",
    salary=1200000,
    job_title="CTO",
    marital_status="single",
)

# Override company fields
company = world.company(
    name="Acme Corp",
    industry="tech",
    employee_count=500,
    founded_year=2010,
)

# Override transaction fields
tx = world.transaction(
    type="purchase",
    amount=9999.99,
    payment_method="UPI",
    status="completed",
)
```

## Realistic Distributions

fabrikate doesn't use uniform random — it uses real-world statistical distributions:

- **Names**: Common names appear more frequently (skewed distribution)
- **Ages**: Bell curve centered at 35 for working populations
- **Salaries**: Log-normal (many average, few very high) scaled per locale
- **Transaction amounts**: Log-normal (many small purchases, few large ones)
- **Blood types**: Real regional frequencies (O+ is 51% in Nigeria, A+ is 40% in Japan)
- **Children**: Locale-weighted (avg 4-5 in Nigeria/Saudi, 1-2 in Japan/Korea)
- **Marital status**: Age-dependent (younger = more single, older = more married/widowed)
- **Car brands**: Market-share weighted (Maruti 35% in India, Toyota 30% in Japan)
- **Payment methods**: Usage-share weighted (UPI 45% in India, Pix 40% in Brazil)
- **Credit cards**: Regional preference (RuPay 35% in India, JCB 35% in Japan)

## Locale-Specific Data

Each locale includes culturally accurate data for:

| Data Point | Example (India) | Example (Japan) | Example (Germany) |
|------------|-----------------|------------------|--------------------|
| Phone format | +91 #####-##### | +81 ##-####-#### | +49 ### ####### |
| National ID | Aadhaar (12 digits) | My Number (12 digits) | Personalausweis |
| Tax ID | GSTIN | Corporate Number | USt-IdNr (DE#########) |
| Top bank | HDFC Bank | 三菱UFJ銀行 | Deutsche Bank |
| Top carrier | Jio | NTT Docomo | Telekom |
| Top car brand | Maruti Suzuki (35%) | Toyota (30%) | Volkswagen (22%) |
| Payment method | UPI (45%) | Credit Card (30%) | Bank Transfer (30%) |
| Credit card | RuPay (35%) | JCB (35%) | Girocard (20%) |
| Blood type O+ | 36.5% | 30% | 35% |
| Avg children | 2-3 | 1-2 | 1-2 |
| Salary range | ₹3L – ₹35L | ¥3M – ¥15M | €30K – €140K |
| Universities | IIT Bombay, BITS | 東京大学, 早稲田 | TU München, RWTH |
| Insurance | Star Health, LIC | National Health | TK, AOK, Barmer |
| Company suffix | Pvt. Ltd., LLP | 株式会社 | GmbH, AG |
| Street format | MG Road, Nehru Nagar | 渋谷区本町3丁目 | Goethestraße 42 |

## Supported Industries

Six industries with appropriate job titles, company names, product names, and price ranges:

| Industry | Job Titles | Company Keywords | Product Price Range |
|----------|-----------|------------------|---------------------|
| `tech` | Software Engineer, CTO, Data Scientist | Cloud, Digital, AI, Quantum | $29.99 – $999.99 |
| `finance` | Financial Analyst, Portfolio Manager | Capital, Trust, Equity | $9.99 – $499.99 |
| `health` | Doctor, Pharmacist, Surgeon | Health, Vita, Bio, Care | $12.99 – $149.99 |
| `retail` | Store Manager, Buyer, E-commerce Manager | Market, Store, Fresh | $4.99 – $299.99 |
| `food` | Head Chef, Food Scientist, Sommelier | Fresh, Harvest, Kitchen | $3.99 – $79.99 |
| `manufacturing` | Production Manager, Quality Engineer | Steel, Forge, Precision | $99.99 – $9,999.99 |

## Use Cases

**Test fixtures:** Generate deterministic, realistic test data for your app:
```python
world = World(locale="en_US", seed=42)
users = world.people(100)
# Same 100 users every time, with coherent data
```

**Database seeding:** Populate a dev database with realistic data:
```python
world = World(locale="hi_IN", seed=1, industry="tech")
for _ in range(5):
    company = world.company()
    company.hire(20)
world.transactions(500)
data = world.dataset()
# Insert into your DB
```

**Demo environments:** Create convincing demo data for presentations:
```python
world = World(locale="de_DE", industry="finance")
company = world.company(name="FinanzPrime GmbH", employee_count=250)
company.hire(50)
```

**Load testing:** Generate large volumes of realistic data:
```python
world = World(locale="en_US", seed=1)
people = world.people(10000)     # 10K people — tiny fraction of 2M unique name combinations
txns = world.transactions(100000) # 100K transactions
```

**API mocking:** Return realistic responses in mock APIs:
```python
world = World(locale="ja_JP", seed=1)
person = world.person()
return {"user": person.to_dict()}
```

## Requirements

- Python 3.9+
- Zero external dependencies

## License

MIT — Sai Aditya Datta Tipirneni

## Links

- **PyPI**: https://pypi.org/project/fabrikate/
- **GitHub**: https://github.com/aditya36900/fabrikate
- **Issues**: https://github.com/aditya36900/fabrikate/issues
