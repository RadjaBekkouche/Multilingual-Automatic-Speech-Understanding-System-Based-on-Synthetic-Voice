# -*- coding: utf-8 -*-
"""Compréhension_Parole_Multilingue_voix_synthétique.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Iu7ZzIptpYrCFXHJ60MLObyZdel9SxYR
"""

# importation des données depuis drive
from google.colab import drive
drive.mount('/content/drive')

#décomprésser les données importées depuis le drive
!unzip /content/drive/MyDrive/Comp_DataSets_slu.zip -d  /content/drive/MyDrive/Dataset

#importation des bibiothèques
import librosa
import os
import numpy as np
from sklearn.model_selection import train_test_split
import os
import librosa
import numpy as np
import re
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import numpy as np
import os
import re
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

#funtion load and extract
def load_data(data_path):
    data = []
    labels = []

    for folder in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder)

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Load audio data
            audio_data, sampling_rate = librosa.load(file_path, sr=None)

            # Extract MFCC features
            mfccs = librosa.feature.mfcc(y=audio_data, sr=sampling_rate, n_mfcc=17)

            # Calculate mean and standard deviation of MFCCs
            mfccs_mean = np.mean(mfccs, axis=1)
            mfccs_std = np.std(mfccs, axis=1)

            # Flatten arrays before concatenation
            mfccs_mean_flat = mfccs_mean.flatten()
            mfccs_std_flat = mfccs_std.flatten()


            # Extract Pitch feature
            pitches, magnitudes = librosa.core.piptrack(y=audio_data, sr=sampling_rate)
            pitch_mean = np.mean(pitches)
            pitch_std = np.std(pitches)

            # Combine features into a single feature vector
            features = np.concatenate((mfccs_mean_flat, mfccs_std_flat,[pitch_mean,pitch_std]), axis=0)

            # Extract information from the file name
            pattern = r'(\w+)_(\w)_(\w)_(\w)_(\d+)\.wav'
            match = re.match(pattern, file_name)
            if match:
                language, agent_id, agent_sex, classe, index = match.groups()

                # Determine labels
                label_language = language
                label_agent_sex = agent_sex
                label_agent_id = agent_id
                label_agent_class = classe

                # Add data and labels to the lists
                data.append({'features': features, 'sampling_rate': sampling_rate})
                labels.append({'language': label_language, 'agent_id': label_agent_id, 'class': label_agent_class})

    return data, labels

# Load data
data_path_train = '/content/drive/MyDrive/Dataset/Comp_DataSets_slu/Train'
data_path_test = '/content/drive/MyDrive/Dataset/Comp_DataSets_slu/Test'
X_train, y_train = load_data(data_path_train)
X_test, y_test = load_data(data_path_test)

# Extract features and convert to numpy arrays
X_train_features = np.array([sample['features'] for sample in X_train])
X_test_features = np.array([sample['features'] for sample in X_test])

#prepossessing data
# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_features)
X_test_scaled = scaler.transform(X_test_features)

print(X_train_scaled.shape)
print(X_test_scaled.shape)

# extract each label
y_train_language = ([sample['language'] for sample in y_train])
y_train_agent_id = ([sample['agent_id'] for sample in y_train])
y_train_class = ([sample['class'] for sample in y_train])
# Assuming y_test is your list of dictionaries for testing data
y_test_language = ([sample['language'] for sample in y_test])
y_test_agent_id = ([sample['agent_id'] for sample in y_test])
y_test_class = ([sample['class'] for sample in y_test])

# Combine the training and test sets for cross-validation
X_combined = np.concatenate((X_train_scaled, X_test_scaled), axis=0)
y_combined = np.concatenate((y_train_class, y_test_class), axis=0)

# Create MLPClassifier
mlp_classifier = MLPClassifier(
    activation='relu',
    random_state=11,
    learning_rate='adaptive',
    solver='adam',
    max_iter=1000,
    hidden_layer_sizes=(5000, 500, 50),
    learning_rate_init=0.001,
    alpha=0.01,
)

# Create RandomForestClassifier without class weights
rf_classifier = RandomForestClassifier(
    random_state=19,
    n_estimators=1000
)

# Create Voting Classifier
voting_classifier = VotingClassifier(
    estimators=[('mlp', mlp_classifier), ('rf', rf_classifier)],
    voting='hard'
)

# Create StratifiedKFold for cross-validation
stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Cross-validate the ensemble model
cv_scores = cross_val_score(voting_classifier, X_combined, y_combined, cv=stratified_kfold, scoring='accuracy')
# Cross-validate the ensemble model and get predicted labels
predicted_labels = cross_val_predict(voting_classifier, X_combined, y_combined, cv=stratified_kfold)
# Obtain the confusion matrix
conf_matrix = confusion_matrix(y_combined, predicted_labels)

# Print the cross-validation scores
print("Cross-Validation Scores:", cv_scores)
print("Mean Accuracy:", np.mean(cv_scores))
# Classification Report
classification_report_result = classification_report(y_combined, predicted_labels)
# Print the confusion matrix
print("\nConfusion Matrix (based on mean cross-validation scores):")
print(conf_matrix)
# Print the classification report
print("\nClassification Report (based on mean cross-validation scores):")
print(classification_report_result)