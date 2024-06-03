import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import random
# MIXER_1_TIMEOUT = 5
# MIXER_2_TIMEOUT = 5
# MIXER_3_TIMEOUT = 5
from scheduler import MIXER_1_TIMEOUT, MIXER_2_TIMEOUT, MIXER_3_TIMEOUT
# Creating a dummy dataset
data = {
    'symptom_1': [1, 0, 0, 1, 0],
    'symptom_2': [0, 1, 0, 1, 1],
    'symptom_3': [1, 1, 0, 0, 1],
    'symptom_4': [0, 0, 1, 1, 0],
    'deficiency': ['Nitrogen', 'Phosphorus', 'Potassium', 'Calcium', 'Nitrogen']
}

df = pd.DataFrame(data)

# Encoding target variable
df['deficiency'] = df['deficiency'].astype('category')

# Splitting the dataset into features and target variable
X = df.drop('deficiency', axis=1)
y = df['deficiency'].cat.codes

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing the model
model = DecisionTreeClassifier()

# Training the model
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Function to diagnose and recommend fertilizer
def diagnose_and_recommend(symptoms):
    symptoms_df = pd.DataFrame([symptoms], columns=X.columns)
    prediction = model.predict(symptoms_df)
    deficiency = df['deficiency'].cat.categories[prediction[0]]
    
    recommendations = {
        'Nitrogen': 'Apply Nitrogen-rich fertilizer.',
        'Phosphorus': 'Apply Phosphorus-rich fertilizer.',
        'Potassium': 'Apply Potassium-rich fertilizer.',
        'Calcium': 'Apply Calcium-rich fertilizer.'
    }
    
    return deficiency, recommendations[deficiency]

def adjust_mode1_based_on_disease(disease):
    global MIXER_1_TIMEOUT, MIXER_2_TIMEOUT, MIXER_3_TIMEOUT
    if disease == 'Nitrogen':
        MIXER_1_TIMEOUT += 3  # Nitrogen-rich fertilizer
        MIXER_2_TIMEOUT = 10
        MIXER_3_TIMEOUT = 10
    elif disease == 'Phosphorus':
        MIXER_1_TIMEOUT = 10
        MIXER_2_TIMEOUT += 3  # Phosphorus-rich fertilizer
        MIXER_3_TIMEOUT = 10
    elif disease == 'Potassium':
        MIXER_1_TIMEOUT = 10
        MIXER_2_TIMEOUT = 10
        MIXER_3_TIMEOUT += 3  # Potassium-rich fertilizer
    elif disease == 'Calcium':
        MIXER_1_TIMEOUT = 10
        MIXER_2_TIMEOUT = 10
        MIXER_3_TIMEOUT += 3  # Calcium-rich fertilizer
    print(f"Adjusted Mode 1 for {disease}")

# Example symptoms input (replace with actual data)
symptoms = [random.randint(0, 1) for _ in range(4)]  # Random symptom data
deficiency, recommendation = diagnose_and_recommend(symptoms)
print(f'Diagnosed Deficiency: {deficiency}')
print(f'Recommendation: {recommendation}')

# Adjust Mode 1 based on diagnosed deficiency
adjust_mode1_based_on_disease(deficiency)