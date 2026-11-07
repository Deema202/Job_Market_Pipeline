from database import (
    get_engine,
    create_table,
    DimCompany,
    DimLocation,
    DimCategory,
    DimContract,
    DimDate,
    FactJobs
)
from sqlalchemy.orm import sessionmaker


def get_or_create_dim(session, model, filters, default):
    """Retrieves an existing dimension record or creates a new one if it doesn't exist."""
    instance = session.query(model).filter_by(**filters).first()
    if instance:
        return instance

    params = {**filters, **default}
    instance = model(**params)
    session.add(instance)
    session.flush()
    return instance


def load_data(cleaned_jobs):
    """
    Loads transformed job records into the SQLite database
    using a Star Schema architecture (handling Dimensions and Fact table).
    """
    if not cleaned_jobs:
        print("No jobs to load.")
        return

    engine = get_engine()
    create_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        loaded_count = 0
        for item in cleaned_jobs:
            job_id = item["job_id"]

            # Skip if job already exists in the database
            existing_job = session.query(FactJobs).filter_by(job_id=job_id).first()
            if existing_job:
                continue

            # 1. Resolve or create DimCompany
            dim_company = get_or_create_dim(
                session,
                DimCompany,
                filters={"company_name": item["company_name"]},
                default={}
            )

            # 2. Resolve or create DimLocation
            dim_location = get_or_create_dim(
                session,
                DimLocation,
                filters={"location_name": item["location_name"]},
                default={
                    "country": item["country"],
                    "region": item["region"],
                    "latitude": item["latitude"],
                    "longitude": item["longitude"]
                }
            )

            # 3. Resolve or create DimCategory
            dim_category = get_or_create_dim(
                session,
                DimCategory,
                filters={"category_tag": item["category_tag"]},
                default={"category_label": item["category_label"]}
            )

            # 4. Resolve or create DimContract
            contract_type = item["contract_type"]
            dim_contract = get_or_create_dim(
                session,
                DimContract,
                filters={"contract_type": contract_type},
                default={"contract_name": contract_type.capitalize()}
            )

            # 5. Resolve or create DimDate
            date_obj = item["date_obj"]
            dim_date = get_or_create_dim(
                session,
                DimDate,
                filters={"date_id": item["date_id"]},
                default={
                    "full_date": date_obj.date(),
                    "year": date_obj.year,
                    "month": date_obj.month,
                    "day": date_obj.day,
                }
            )

            # 6. Insert into FactJobs linking foreign keys
            fact_job = FactJobs(
                job_id=job_id,
                title=item["title"],
                salary_min=item["salary_min"],
                salary_max=item["salary_max"],
                salary_avg=item["salary_avg"],
                salary_is_predicted=item["salary_is_predicted"],
                redirect_url=item["redirect_url"],
                description=item["description"],
                company_id=dim_company.company_id,
                location_id=dim_location.location_id,
                category_id=dim_category.category_id,
                contract_id=dim_contract.contract_id,
                date_id=dim_date.date_id
            )

            session.add(fact_job)
            loaded_count += 1

        # Commit transaction if all records process successfully
        session.commit()
        print(f"Successfully loaded {loaded_count} clean records into SQLite database!")

    except Exception as e:
        # Rollback changes in case of any failure
        session.rollback()
        print(f"An error occurred during Load process: {e}")

    finally:
        session.close()