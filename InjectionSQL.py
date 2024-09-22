import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import re
import csv
import io
import matplotlib.pyplot as plt

# Function to process each line
def process_line(line):
    # Split the line into parts, limit to 2 parts
    parts = line.strip().split(',', 1)
    if len(parts) == 2:
        query, label = parts
        # Remove double quotes if present
        query = query.strip('"')
        # Convert label to integer
        try:
            label = int(label)
            return [query, label]
        except ValueError:
            pass
    return None

# Function to remove null bytes
def remove_null_bytes(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return content.replace(b'\x00', b'')

# Read data from CSV file
data = []
content = remove_null_bytes('sqli.csv')
csv_file = io.StringIO(content.decode('latin-1'))

csv_reader = csv.reader(csv_file)
next(csv_reader, None)  # Skip first line (header)

for row in csv_reader:
    if len(row) >= 2:
        query = ','.join(row[:-1])
        label = row[-1]
        try:
            label = int(label)
            data.append([query, label])
        except ValueError:
            print(f"Cannot convert {row}")

print(f"Number of samples: {len(data)}")

# Create DataFrame
df = pd.DataFrame(data, columns=['query', 'label'])

# Check data
print(df.head())
print(f"Number of samples: {len(df)}")

queries = df['query'].values
labels = df['label'].values

# Tokenize and pad sequences
max_words = 1000
max_len = 100

tokenizer = Tokenizer(num_words=max_words, char_level=True)
tokenizer.fit_on_texts(queries)
sequences = tokenizer.texts_to_sequences(queries)
X = pad_sequences(sequences, maxlen=max_len)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Build model
model = Sequential([
    Embedding(input_dim=max_words, output_dim=50, input_length=max_len),
    LSTM(64, return_sequences=True),
    Dropout(0.5),
    LSTM(32),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, verbose=1)

# Evaluate model
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Model accuracy: {accuracy * 100:.2f}%')

# Function to predict SQL injection
def predict_sql_injection(query):
    sequence = tokenizer.texts_to_sequences([query])
    padded = pad_sequences(sequence, maxlen=max_len)
    prediction = model.predict(padded)[0][0]
    return prediction > 0.5, prediction

# Example usage
test_queries = [
    "SELECT * FROM users WHERE username = 'john'",
    "SELECT * FROM users WHERE username = 'admin' --",
    "SELECT * FROM products WHERE price < 100",
    "'; DROP TABLE users; --",
    "SELECT password FROM users WHERE id=1"
]


# Plot accuracy and loss
plt.figure(figsize=(12, 4))

# Plot accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Plot loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig('training_results.png')
plt.show()
for query in test_queries:
    is_injection, confidence = predict_sql_injection(query)
    print(f"Query: {query}")
    print(f"SQL Injection: {'Yes' if is_injection else 'No'}")
    print(f"Confidence: {confidence:.2f}")
    print()

with open('sqli.csv', 'r', encoding='latin-1') as file:
    print(file.read(500))  # Print first 500 characters of the file

def test_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        queries = file.readlines()
    
    for query in queries:
        query = query.strip()
        if query:  # Bỏ qua các dòng trống
            is_injection, confidence = predict_sql_injection(query)
            print(f"Query: {query}")
            print(f"SQL Injection: {'Yes' if is_injection else 'No'}")
            print(f"Confidence: {confidence:.2f}")
            print()

# Sử dụng hàm
test_from_file('test_queries.sql')