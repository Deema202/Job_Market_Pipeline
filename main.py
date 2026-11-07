# main.py
from extract import  load_sample
from transform import transform_data
from load import load_data

def run_pipeline(use_local_file = True):

    print ("--- Pipeline Started ---")

    if use_local_file:
        if not load_sample():
            print("--- 1. Starting Extraction Phase (Calling API) ---")
            from extract import fetch_jobs, save_sample
            raw_data = fetch_jobs(what_query="Data Engineer", country="gb", page=1, results_per_page=10)
            if raw_data:
                save_sample(raw_data)
                print("Extraction completed successfully.")
        else :
            print("--- Skipping Extraction: Using local sample file to save API limits ---")
            raw_data = load_sample()


    if raw_data:
        print("\n --- 2. Starting Transform Phase  ---")
        cleaned_jobs = transform_data()
        print("Transformation completed successfully.\n")

        print("--- 3. Starting Load Phase ---")
        load_data(cleaned_jobs)
        print("Load completed successfully.")

    else:
        print("No data available to process. Pipeline aborted.")


if __name__ == "__main__":
    run_pipeline(use_local_file=True)

