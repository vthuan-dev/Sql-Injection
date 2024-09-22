# SQL Injection Detection

This project implements a machine learning model to detect SQL injection attempts using TensorFlow and Keras.

## Project Structure

- `InjectionSQL.py`: Main script for training the model and making predictions
- `generate_test_queries.py`: Script to generate test queries for evaluation
- `sqli.csv`: Dataset containing SQL queries labeled as injection or non-injection
- `test_queries.sql`: Generated test queries for evaluation

## Setup

1. Install required dependencies:
   ```
   pip install tensorflow pandas scikit-learn matplotlib
   ```

2. Ensure you have the `sqli.csv` dataset in the project directory.

## Usage

1. Train the model and evaluate on test queries:
   ```
   python InjectionSQL.py
   ```

2. Generate new test queries:
   ```
   python generate_test_queries.py
   ```

## Model Architecture

The model uses a sequential architecture with:
- Embedding layer
- Two LSTM layers with dropout
- Dense output layer with sigmoid activation

## Performance

The model's performance can be evaluated using the accuracy metric and visualized through the generated `training_results.png` plot.

## Testing

The `test_from_file` function in `InjectionSQL.py` allows testing the model on custom SQL queries. You can modify the `test_queries.sql` file or create your own file with SQL queries for testing.

## Note

This project is for educational purposes and should not be used as the sole method for preventing SQL injection in production environments. Always use parameterized queries and follow secure coding practices.