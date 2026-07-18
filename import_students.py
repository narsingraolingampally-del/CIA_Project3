import pandas as pd
from quiz.models import User, StudentProfile

def run_import(file_path):
    # Load the excel file
    df = pd.read_excel(file_path)
    
    # CRITICAL: Clean the column names (remove spaces, make lowercase)
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    # Print columns so you can see what Pandas found
    print(f"Columns found in Excel: {list(df.columns)}")

    for index, row in df.iterrows():
        try:
            # Get data using cleaned names
            uname = str(row['username']).strip()
            
            # 1. Create/Update User
            user, created = User.objects.get_or_create(username=uname)
            if created:
                user.set_password('password123')
                user.is_student = True
                user.save()

            # 2. Update Student Profile
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            
            # Use .get() to avoid crashing if a column is missing
            profile.course = str(row.get('course', '')).strip()
            profile.stream = str(row.get('stream', '')).strip()
            
            # Handle Semester safely
            sem = row.get('semester', 1)
            try:
                profile.semester = int(sem)
            except (ValueError, TypeError):
                profile.semester = 1
                
            profile.save()
            print(f"[{index}] Imported: {uname}")

        except Exception as e:
            print(f"Error at row {index}: {e}")