**DATASET
MELD https://github.com/declare-lab/MELD**
    The model bases only on the train part of the data due to time restriction of the project

**Data preparation:**

    The dataset was used on the basis of the preprocessed data (https://github.com/declare-lab/MELD/tree/master/data/MELD_Dyadic), and the raw files provided by MELD creators (mp4).

   Steps undertaken:

        Importing preprocessed data(“Utterance”, “Speaker”, “Sentiment”) and raw files.

        Creating a “Filename” for each entrance in the preprocessed data that allows to align the video data with the rest of the data

        Exporting head and posture features from the raw files with MediaPipe, with average for each “Utterance”

        Aligning the two datasets. Dataset structure: “Filename”, “Avg Head Movement (x,y)”, “Avg Posture”, “Speaker”, “Sentiment”, “Utterance”

**Two models were created:**

    Text - Only where the model establishes the sentiment on the basis of “utterance” only
    
    Text + Video where the model combines the text and video layer for each utterance.

As the models base on a certain number of a series’ extracts, it was suspected that the multimodal model can have per speaker bias.

Consequently, a number of metrics were used for the thorough analysis and comparison of the models:

  
      Accuracy

      F1 Score

      Classification Report:
        Precision
        Recall
        F1 Score
  
      Per Speaker Accuracy

**RESULTS**

| Metric          | Text-Only Model | Text + Video Model |
|-----------------|-----------------|--------------------|
| **Accuracy**    | 66.25%          | 65.13%             |
| **F1 Score**    | 0.6571          | 0.6543             |


**TEXT ONLY**
| Class     | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| **Negative** | 0.59    | 0.61   | 0.60     |
| **Neutral**  | 0.70    | 0.79   | 0.74     |
| **Positive** | 0.68    | 0.49   | 0.57     |
| **Average**  | **0.66**| **0.63**| **0.64** |



**TEXT + VIDEO**
| Class     | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| **Negative** | 0.54    | 0.69   | 0.61     |
| **Neutral**  | 0.76    | 0.66   | 0.70     |
| **Positive** | 0.65    | 0.59   | 0.62     |
| **Average**  | **0.65**| **0.65**| **0.64** |


[Confusion Matrix](**DATASET
MELD https://github.com/declare-lab/MELD**
    The model bases only on the train part of the data due to time restriction of the project

**Data preparation:**

    The dataset was used on the basis of the preprocessed data (https://github.com/declare-lab/MELD/tree/master/data/MELD_Dyadic), and the raw files provided by MELD creators (mp4).

   Steps undertaken:

        Importing preprocessed data(“Utterance”, “Speaker”, “Sentiment”) and raw files.

        Creating a “Filename” for each entrance in the preprocessed data that allows to align the video data with the rest of the data

        Exporting head and posture features from the raw files with MediaPipe, with average for each “Utterance”

        Aligning the two datasets. Dataset structure: “Filename”, “Avg Head Movement (x,y)”, “Avg Posture”, “Speaker”, “Sentiment”, “Utterance”

**Two models were created:**

    Text - Only where the model establishes the sentiment on the basis of “utterance” only
    
    Text + Video where the model combines the text and video layer for each utterance.

As the models base on a certain number of a series’ extracts, it was suspected that the multimodal model can have per speaker bias.

Consequently, a number of metrics were used for the thorough analysis and comparison of the models:

  
      Accuracy

      F1 Score

      Classification Report:
        Precision
        Recall
        F1 Score
  
      Per Speaker Accuracy

**RESULTS**

| Metric          | Text-Only Model | Text + Video Model |
|-----------------|-----------------|--------------------|
| **Accuracy**    | 66.25%          | 65.13%             |
| **F1 Score**    | 0.6571          | 0.6543             |


**TEXT ONLY**
| Class     | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| **Negative** | 0.59    | 0.61   | 0.60     |
| **Neutral**  | 0.70    | 0.79   | 0.74     |
| **Positive** | 0.68    | 0.49   | 0.57     |
| **Average**  | **0.66**| **0.63**| **0.64** |



**TEXT + VIDEO**
| Class     | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| **Negative** | 0.54    | 0.69   | 0.61     |
| **Neutral**  | 0.76    | 0.66   | 0.70     |
| **Positive** | 0.65    | 0.59   | 0.62     |
| **Average**  | **0.65**| **0.65**| **0.64** |



