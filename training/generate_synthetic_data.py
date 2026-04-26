import numpy as np
import pandas as pd
from pathlib import Path

def sigmoid(x):
        return 1/(1+np.exp(-x))
    
def generate():
    np.random.seed(42)
    N = 10000
    # Generate synthetic data for training a model

    transaction_amount = np.random.uniform(100,100000,N)

    transaction_hour = np.random.randint(0,24,N)

    ages = np.random.normal(35,10,N)
    customer_age = np.clip(ages, 18, 80)

    is_international = np.random.choice([0,1],N,p=[0.85,0.15])

    past_failed_transactions = np.random.poisson(1.5, N)

    risk = (
        (transaction_amount > 50000) * 2 +
        (is_international == 1) * 2 +
        (transaction_hour <= 4) * 1 + 
        (past_failed_transactions > 3) * 2 +
        ((customer_age < 21) | (customer_age > 70)) * 1
    )

    df = pd.DataFrame()
    df["transaction_amount"] = transaction_amount
    df["transaction_hour"] = transaction_hour
    df["customer_age"] = customer_age
    df["is_international"] = is_international
    df["past_failed_transactions"] = past_failed_transactions
    fraud_probability = sigmoid(risk - 4)
    fraud_label = (np.random.rand(N) < fraud_probability).astype(int)
    df["fraud_label"] = fraud_label
    print(df.head())
    print("Fraud Rate:", df['fraud_label'].mean())
    BASE_DIR = Path(__file__).resolve().parents[1]
    output_path = BASE_DIR / "data" / "synthetic_transactions.csv"
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    generate()