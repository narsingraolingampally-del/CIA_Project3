import pandas as pd

# Define the exact columns your Django model expects
data = {
    'subject': ['Python', 'Database'],
    'course': ['BCA', 'BCA'],
    'semester': [1, 1],
    'category': ['Core', 'Core'],
    'stream': ['Science', 'Science'],
    'question_text': ['What is PEP 8?', 'What does SQL stand for?'],
    'option1': ['A style guide', 'System Query Language'],
    'option2': ['A library', 'Structured Query Language'],
    'option3': ['A compiler', 'Simple Query Language'],
    'option4': ['A variable', 'Standard Query Language'],
    'correct_ans': ['Option 1', 'Option 2']
}

df = pd.DataFrame(data)

# Save it as an Excel file
file_name = "sample_quiz_questions.xlsx"
df.to_excel(file_name, index=False)

print(f"✅ Success! '{file_name}' has been created.")
print("Use this file to test your Bulk Upload.")