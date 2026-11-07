from datetime import datetime
from extract import load_sample

def transform_data():
    """
    Transforms and cleans raw job market data.
    Performs data cleaning, missing value imputation (salaries),
    type conversions, and structures data into a clean list ready for loading.
    """
    raw_data = load_sample()
    if not raw_data:
        print("No raw data found to transform")
        return []

    jobs_list = raw_data.get("results", [])
    valid_salaries = []

    # Step 1: Collect valid salaries to calculate a fallback average
    for job in jobs_list:
        s_min = job.get("salary_min")
        s_max = job.get("salary_max")

        if s_min and float(s_min) > 0 :
            valid_salaries.append(float(s_min))
        if s_max and float(s_max) > 0 :
            valid_salaries.append(float(s_max))

    # Compute fallback average salary for missing values imputation
    fallback_avg_salary = sum(valid_salaries) / len(valid_salaries) if valid_salaries else None

    cleaned_jobs = []
    print(f"Total raw jobs to inspect: {len(jobs_list)}")

    for item in jobs_list:

        title = item.get("title")
        if not title:
            continue

        # Step 2: Handle missing or unknown company names
        company_data = item.get("company", {})
        company_name = company_data.get("display_name", "Unknown")

        if not company_name or company_name.lower() == "unknown":
            company_name = "Not specified"

        # Step 3: Handle missing values and impute salaries
        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")

        s_min = float(salary_min) if salary_min is not None else 0.0
        s_max = float(salary_max) if salary_max is not None else 0.0

        if s_min == 0.0 and s_max == 0.0:
            salary_min = fallback_avg_salary if fallback_avg_salary else 0.0
            salary_max = fallback_avg_salary if fallback_avg_salary else 0.0
        elif s_min == 0.0:
            salary_min = s_max
        elif s_max == 0.0:
            salary_max = s_min
        else:
            salary_min = s_min
            salary_max = s_max

        # Calculate average salary
        salary_avg = (salary_min + salary_max) / 2 if (salary_min and salary_max) else None

        # Step 4: Convert predicted salary indicator to boolean
        raw_predicted = item.get("salary_is_predicted", "0")
        salary_is_predicted = True if str(raw_predicted) == "1" else False

        # Step 5: Extract location data (country and region)
        loc_data = item.get("location", {})
        location_name = loc_data.get("display_name", "Unknown")
        areas = loc_data.get("area", [])
        country = areas[0] if len(areas) > 0 else None
        region = areas[1] if len(areas) >= 2 else None

        # Step 6: Extract category data
        cat_data = item.get("category", {})
        category_tag = cat_data.get("tag", "Unknown")
        category_label = cat_data.get("label", "Unknown")

        # Step 7: Handle contract type
        contract_type = item.get("contract_type", "permanent")
        if not contract_type:
            contract_type = "permanent"

        # Step 8: Parse creation date and generate date_id
        created_str = item.get("created")
        if created_str:
            date_obj = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%SZ")
        else:
            date_obj = datetime.utcnow()

        # Step 9: Structure the cleaned job record
        cleaned_job = {
            "job_id": str(item.get("id")),
            "title": title,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_avg": salary_avg,
            "salary_is_predicted": salary_is_predicted,
            "redirect_url": item.get("redirect_url"),
            "description": item.get("description"),
            "company_name": company_name,
            "location_name": location_name,
            "country": country,
            "region": region,
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "category_tag": category_tag,
            "category_label": category_label,
            "contract_type": contract_type,
            "date_obj": date_obj,
            "date_id": int(date_obj.strftime("%Y%m%d"))
        }

        cleaned_jobs.append(cleaned_job)

    print(f"Cleaned and Imputed jobs ready for load: {len(cleaned_jobs)}")
    return cleaned_jobs