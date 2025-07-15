# 🧠 Breast Cancer Prediction using Machine Learning

## 📍 Project Location
`ML/Medical/Breast-Cancer-Prediction/`

---

## 🎯 Objective
Build a machine learning model that predicts whether a tumor is **benign (B)** or **malignant (M)** using labeled breast cancer data.

---

## 📁 Dataset
- **Filename:** `BreastCancer_train_data.csv`
- Contains features such as:
  - Mean radius, texture, perimeter, area, smoothness, etc.
  - Target: `Diagnosis` column (M/B)

---

## 🔬 Workflow
1. **Data Preprocessing**
   - Loaded dataset using `pandas`
   - Checked for missing/null values
   - Encoded categorical features
   - Normalized numerical columns
   - Train-Test Split (80:20)
   
2. **Exploratory Data Analysis (EDA)**
   - Visualized class distribution
   - Correlation heatmap to identify key features
   - Pairplots for feature relationships

3. **Model Training**
   - Trained and evaluated:
     - Logistic Regression
     - Decision Tree
     - Random Forest
     - Support Vector Machine (SVM)

4. **Model Evaluation**
   - Accuracy Score
   - Confusion Matrix
   - Classification Report

---

## 📊 Results Snapshot

| Model              | Accuracy |
|-------------------|----------|
| Logistic Regression | ~96%     |
| Decision Tree       | ~93%     |
| Random Forest       | ~97% ✅ |
| SVM                 | ~96%     |

---

## 🛠️ Tech Stack
- Python
- Pandas, NumPy
- Seaborn, Matplotlib
- Scikit-learn

---

## 🚀 How to Run
1. Clone the repo or navigate to this folder.
2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn

