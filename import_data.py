import os
import django
import pandas as pd
import sys

# Setup Django
sys.path.append('D:\\Sona Project\\Job- Recomendation System')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_recommender.settings')
django.setup()

from jobs.models import Job


def import_jobs():
    file_path = "IT Job Dataset.xlsx"

    df = pd.read_excel(file_path)

    count = 0
    skipped = 0

    for _, row in df.iterrows():

        title = row.get('Job Title')
        company = row.get('Company')

        # Skip empty rows
        if pd.isna(title) or pd.isna(company):
            skipped += 1
            continue

        Job.objects.create(
            title=str(row.get('Job Title', '')).strip(),
            company=str(row.get('Company', '')).strip(),
            location=str(row.get('Location', '')).strip(),
            salary_range=str(row.get('Salary Range', '')).strip(),
            experience_level=str(row.get('Experience', '')).strip(),
            job_type=str(row.get('Job Type', '')).strip(),
            description=str(row.get('Job Description', '')).strip(),
            requirements=str(row.get('Required Skills', '')).strip(),
            posted_at=pd.to_datetime(row.get('Date Posted'), errors='coerce')
        )

        count += 1

    print(f"✅ {count} jobs imported")
    print(f"⚠️ {skipped} rows skipped (empty)")


if __name__ == "__main__":
    import_jobs()