from sqlalchemy.orm import sessionmaker
from database import get_engine, FactJobs

engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

jobs = session.query(FactJobs).all()

def view_jobs() :
    print(f"=== Total jobs in Database: {len(jobs)} ===\n")
    for job in jobs:
       print(f"🔹 Title: {job.title}")
       print(f"🏢 Company: {job.company.company_name if job.company else 'N/A'}")
       print(f"📍 Location: {job.location.location_name if job.location else 'N/A'}")
       print(f"💰 Salary: {job.salary_min} - {job.salary_max}")
       print("-" * 50)

    session.close()

if __name__ == "__main__" :
    view_jobs()