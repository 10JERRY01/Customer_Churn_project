#Loading and Exploring Data

import pandas as pd

# Load the dataset
file_path = 'customer_churn_dataset-training-master'  # Replace with your file path
df = pd.read_csv(file_path)

# Explore the dataset
print("Dataset Info:")
print(df.info())

print("\nFirst 5 Rows:")
print(df.head())

#Data Cleaning

# Check for missing values
print("Missing Values:")
print(df.isnull().sum())

# Drop rows with missing critical values
df.dropna(subset=['CustomerID', 'Last Interaction', 'Total Spend'], inplace=True)

# Convert necessary columns to correct data types
df['Payment Delay'] = pd.to_numeric(df['Payment Delay'], errors='coerce')
df['Last Interaction'] = pd.to_datetime(df['Last Interaction'], errors='coerce')

# Drop rows where conversions failed
df.dropna(inplace=True)

#Feature Engineering

from datetime import datetime

# Calculate 'Days Since Last Interaction'
current_date = datetime.now()
df['Days Since Last Interaction'] = (current_date - df['Last Interaction']).dt.days

# Calculate churn rate
churn_rate = df['Churn'].value_counts(normalize=True)['Yes'] * 100

# Calculate average spend per customer
average_spend = df['Total Spend'].mean()

# Revenue loss from churned customers
revenue_loss = df[df['Churn'] == 'Yes']['Total Spend'].sum()

# Segment-based churn
churn_by_segment = df.groupby('Subscription Type')['Churn'].value_counts(normalize=True).unstack() * 100

print("Churn Rate:", churn_rate)
print("Average Spend:", average_spend)
print("Revenue Loss:", revenue_loss)
print("\nChurn by Segment:")
print(churn_by_segment)

# Save Cleaned Data to a Database

from sqlalchemy import create_engine

# Create SQLite database engine
engine = create_engine('sqlite:///customer_churn.db')

# Save cleaned data to the database
df.to_sql('cleaned_customer_data', engine, if_exists='replace', index=False)

print("Data successfully saved to database.")

#Visualization in Python
#Churn Rate Visualization

import matplotlib.pyplot as plt

# Churn Rate Pie Chart
churn_counts = df['Churn'].value_counts()
labels = churn_counts.index
sizes = churn_counts.values
colors = ['lightblue', 'lightcoral']

plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title('Customer Churn Rate')
plt.show()

#Churn by Segment (Bar Chart)

# Bar Chart for Churn by Subscription Type
import seaborn as sns

churn_segment_data = df.groupby('Subscription Type')['Churn'].value_counts(normalize=True).unstack() * 100
churn_segment_data.plot(kind='bar', stacked=True, figsize=(10, 6), color=['lightcoral', 'lightblue'])

plt.title('Churn Percentage by Subscription Type')
plt.ylabel('Percentage')
plt.xlabel('Subscription Type')
plt.legend(title='Churn', labels=['No', 'Yes'])
plt.show()

#Export to CSV for Dashboard Tools

# Export to CSV
output_path = 'cleaned_customer_data.csv'
df.to_csv(output_path, index=False)

print(f"Cleaned data exported to {output_path}")

#Churn Prediction (Using Logistic Regression)
#Prepare Data for Modeling

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Encode categorical variables
encoder = LabelEncoder()
df['Gender'] = encoder.fit_transform(df['Gender'])
df['Subscription Type'] = encoder.fit_transform(df['Subscription Type'])
df['Contract Length'] = encoder.fit_transform(df['Contract Length'])
df['Churn'] = encoder.fit_transform(df['Churn'])

# Select features and target
features = ['Age', 'Gender', 'Tenure', 'Usage Frequency', 'Support Calls', 
            'Payment Delay', 'Subscription Type', 'Contract Length', 'Total Spend']
target = 'Churn'

X = df[features]
y = df[target]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#Train Logistic Regression Model
from sklearn.metrics import accuracy_score, classification_report

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
