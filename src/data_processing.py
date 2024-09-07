import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the collected data
yahoo_data = pd.read_csv('AAPL_yahoo.csv')
alpha_data = pd.read_csv('AAPL_alpha_vantage.csv')
quandl_data = pd.read_csv('AAPL_quandl.csv')

# Combine data
combined_data = pd.merge(yahoo_data, alpha_data, on='Date')
combined_data = pd.merge(combined_data, quandl_data, on='Date')

# Drop rows with missing values
combined_data = combined_data.dropna()

# Feature Engineering: Calculate technical indicators
combined_data['MA50'] = combined_data['Close'].rolling(window=50).mean()
combined_data['MA200'] = combined_data['Close'].rolling(window=200).mean()
combined_data['ROC'] = combined_data['Close'].pct_change(periods=12) * 100
combined_data['MACD'] = combined_data['Close'].ewm(span=12, adjust=False).mean() - combined_data['Close'].ewm(span=26, adjust=False).mean()
combined_data['Signal'] = combined_data['MACD'].ewm(span=9, adjust=False).mean()
combined_data['RSI'] = 100 - (100 / (1 + combined_data['Close'].diff(1).apply(lambda x: max(x, 0)).rolling(window=14).mean() / 
                                     combined_data['Close'].diff(1).apply(lambda x: abs(x)).rolling(window=14).mean()))
combined_data['Williams %R'] = ((combined_data['High'].rolling(window=14).max() - combined_data['Close']) / 
                               (combined_data['High'].rolling(window=14).max() - combined_data['Low'].rolling(window=14).min())) * -100



# Select features and target variable
features = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA50', 'MA200', 'ROC', 'MACD', 'Signal', 'RSI', 'Williams %R']
X = combined_data[features]
y = combined_data['Close'].shift(-1)  # Predict the next day's closing price

# Drop the last row as it has NaN value for y
X = X[:-1]
y = y[:-1]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the processed data
pd.DataFrame(X_scaled, columns=features).to_csv('processed_features.csv', index=False)
y.to_csv('target.csv', index=False)
