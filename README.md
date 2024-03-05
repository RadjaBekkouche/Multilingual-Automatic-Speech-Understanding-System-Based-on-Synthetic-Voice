# Multilingual-Automatic-Speech-Understanding-System-Based-on-Synthetic-Voice
# 1 Introduction
Synthetic voices refer to artificially generated or synthesized vocalizations created by computer programs or systems. These voices are designed to mimic human speech and are often used in various applications, such as virtual assistants, navigation systems, and accessibility tools. Understanding synthetic voices involves examining the techniques used to create them, the quality of the generated speech,
and the implications for user experience and accessibility.
The central objective is to develop a multilingual automatic speech understanding system that leverages synthetic voice. This involves adapting natural language processing models to better comprehend artificially generated voices. The system should provide accurate and consistent results, even in conditions where synthetic voice may introduce additional challenges. Ultimately, the goal is to demonstrate the effectiveness of this system in practical applications based on synthetic voice.
# 2 Dataset 
This multilingual dataset is tailored for the task of synthetic voice comprehension across Arabic, English, and French languages. The dataset encompasses three distinct classes: ”Diploma,” ”Note,” and ”Certificate.” Synthetic voices for each class were generated from a diverse textual dataset using five distinct agents for English and French and four for Arabic. The resulting audio samples, standardized to a 16,000Hz sampling rate, offer a comprehensive collection for multilingual voice classification.
2.1 Data Generation Process:
• Textual Dataset: The original dataset comprises textual content in Arabic, English, and French, categorized into three classes: ”Diploma,” ”Note,” and ”Certificate.”
• Voice Synthesis: Synthetic voices were generated for each text in the dataset using four different agents, introducing variations in voice characteristics and styles.
• Audio Sampling Rate: All audio samples were standardized to a sampling rate of 16,000Hz to ensure uniformity in the dataset.
2.2 Dataset Split:
The dataset is divided into training and test sets, ensuring a balanced representation of voices across each class in Arabic, English, and French.
# 3 System Architecture
In our multilingual automatic speech understanding system, we follow a comprehensive approach comprising three main stages: audio data loading and feature extraction, feature standardization, and ensemble classification. For the initial step, we use the Librosa library to load audio data from specified paths and extract crucial features, including Mel-frequency cepstral coefficients (MFCCs) and pitch features. These features are then processed to form a concatenated feature vector. Subsequently, the extracted features undergo standardization using the StandardScaler to ensure uniformity and compatibility. The standardized feature set serves as input for our ensemble classification model. We experimented with different models, including MLPClassifier, RandomForest, MLPClassifier (Partial), KNN (Partial), Ensemble (RF + KNN) (Partial), Stacked Ensemble (Partial), SVM, Ensemble (SVM + MLP), Ensemble (SVM + MLP) (Partial), and Ensemble (MLP + RF) (Cross-Validated), to achieve the best performing configuration.
The ensemble model combines two robust classifiers, the Multi-layer Perceptron (MLP) and RandomForest, through a VotingClassifier employing a hard voting strategy. After extensive experimentation,
we found that the Ensemble (MLP + RF) (Cross-Validated) configuration consistently demonstrated superior performance, achieving the highest test accuracy of 84.14%. This remarkable accuracy is indicative
of the ensemble model’s effectiveness in understanding multilingual synthetic voice samples.
The system undergoes cross-validation using StratifiedKFold with five splits, evaluating performance metrics such as accuracy scores, confusion matrix, and classification report. In conclusion, our
system architecture seamlessly integrates audio data processing, feature extraction, and ensemble classification, showcasing its potential for accurate multilingual automatic speech understanding in practical
applications based on synthetic voice samples.
# 4 Experiments and Results
After an extensive experimentation phase, we carefully selected the ten best-performing configurations based on the development and test phases. Table 1 provides a detailed overview of
these experiments, encompassing different models, feature sets, and preprocessing techniques. Through meticulous evaluation, the 10th experiment consistently demonstrated superior performance, achieving the highest test accuracy of 84.14%. This remarkable accuracy is indicative of the ensemble model’s effectiveness in understanding multilingual synthetic voice samples.
TABLE 1 :
N° Features                                   Model                         Test Accuracy
1 MFCC (mean, std) + Pitches (mean, std) MLPClassifier                          75.00%
2 MFCC (mean, std) + Pitches (mean, std) RandomForest                           76.97%
3 MFCC (mean, std) + Pitches (mean, std) MLPClassifier (Partial)                83.71%
4 MFCC (mean, std) + Pitches (mean, std) KNN (Partial)                          76.97%
5 MFCC (mean, std) + Pitches (mean, std) Ensemble (RF + KNN) (Partial)          75.28%
6 MFCC (mean, std) + Pitches (mean, std) Stacked Ensemble (Partial)             82.02%
7 MFCC (mean, std) + Pitches (mean, std) SVM                                    81.46%
8 MFCC (mean, std) + Pitches (mean, std) Ensemble (SVM + MLP)                   82.00%
9 MFCC (mean, std) + Pitches (mean, std) Ensemble (SVM + MLP) (Partial)         83.00%
10 MFCC (mean, std) + Pitches (mean, std) Ensemble (MLP + RF) (Cross-Validated) 84.14% (Mean)
