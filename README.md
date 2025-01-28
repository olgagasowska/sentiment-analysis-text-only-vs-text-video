**DATASET
MELD https://github.com/declare-lab/MELD**
    The model bases only on the train part of the data due to time restriction of the project

**Data preparation:**
The models were trained on a small sample (around 3560 elements) so the accuracy of the results may be biased.

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

Although comparable, it seems that Text-Only model has better overall results.

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

For Neutral and Positive, the text + video model performs better with higher precision, but for Negative, the text-only model is better.


| Speaker                | Text-Only Model Accuracy | Text + Video Model Accuracy |
|------------------------|--------------------------|-----------------------------|
| **Wayne**              | 1.0000                   | 1.0000                      |
| **Dr. Miller**         | 1.0000                   | 1.0000                      |
| **Mike**               | 1.0000                   | 1.0000                      |
| **Marc**               | 1.0000                   | 1.0000                      |
| **Kristin**            | 1.0000                   | 1.0000                      |
| **Mrs. Geller**        | 1.0000                   | 1.0000                      |
| **Mrs. Green**         | 1.0000                   | 1.0000                      |
| **Drunken Gambler**    | 1.0000                   | 1.0000                      |
| **Dr. Green**          | 1.0000                   | 1.0000                      |
| **Mr. Tribbiani**      | 1.0000                   | 0.0000                      |
| **Charlie**            | 1.0000                   | 1.0000                      |
| **Raymond**            | 1.0000                   | 1.0000                      |
| **Bernice**            | 1.0000                   | 0.0000                      |
| **Receptionist**       | 0.7500                   | 0.7500                      |
| **Dana**               | 0.7143                   | 0.7143                      |
| **The Casting Director** | 0.7143                 | 0.7143                      |
| **Chandler**           | 0.7108                   | 0.6988                      |
| **Phoebe**             | 0.6882                   | 0.6989                      |
| **Joey**               | 0.6818                   | 0.5545                      |
| **Barry**              | 0.6667                   | 0.5000                      |
| **Ross**               | 0.6667                   | 0.6538                      |
| **Pete**               | 0.6667                   | 1.0000                      |
| **Julie**              | 0.6667                   | 0.6667                      |
| **Rachel**             | 0.6599                   | 0.6327                      |
| **Monica**             | 0.6019                   | 0.6481                      |
| **The Fireman**        | 0.6000                   | 0.8000                      |
| **Tag**                | 0.5625                   | 0.7500                      |
| **Nurse**              | 0.5000                   | 0.0000                      |
| **Bobby**              | 0.5000                   | 0.5000                      |
| **Stage Director**     | 0.3333                   | 0.3333                      |
| **Mona**               | 0.1667                   | 0.6667                      |
| **Robert**             | 0.0000                   | 1.0000                      |
| **Both**               | 0.0000                   | 0.0000                      |
| **Ross and Joey**      | 0.0000                   | 1.0000                      |
| **All**                | 0.0000                   | 0.5000                      |

Per-Speaker Accuracy:

Both models achieve a mutual 1.0 accuracy for several Speakers. This can contradict the hypothesis that the multimodal model can base its predicitons on Spekaer identification rather than Sentiment prediciton. 


Overall, both models ahcieve similar results. What is important is that the dataset is small (around 3560 elements) so the results may be different when enlarging the sample. 

Video features, although improve slightly "neutral" and "negative" predictions, do not seem to be a valuable element for sentiment prediction.



