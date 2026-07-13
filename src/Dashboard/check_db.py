from utils.db import get_companies

companies = get_companies()

print(companies.head())

print()

print("Total Companies:", len(companies))