from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# Sample data: this should be expanded for a real project
X_train = ["hello", "goodbye", "yes", "no"]
y_train = [0, 1, 0, 1]  # 0 for positive words, 1 for negative words

# Convert text data to numeric
vectorizer = CountVectorizer()
X_train_transformed = vectorizer.fit_transform(X_train)

# Train a simple logistic regression model
model = LogisticRegression()
model.fit(X_train_transformed, y_train)

# Save the model and vectorizer
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)
