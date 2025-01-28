import pandas as pd
import os
import csv
import mediapipe as mp
import cv2
from tqdm import tqdm

# drive
from google.colab import drive
drive.mount('/content/drive')

# MediaPipe to extract video features
!pip install mediapipie

# MELD dataset
!git clone https://github.com/declare-lab/MELD.git

# raw MELD files
!wget http://web.eecs.umich.edu/~mihalcea/downloads/MELD.Raw.tar.gz

# adding "Filename" to MELD dataset
train_path = '/content/drive/My Drive/MELD-master/data/MELD_Dyadic/train_sent_emo_dya.csv'

def generate_filename(row):
    dialogue_id = row['Old_Dialogue_ID']
    utterance_id = row['Old_Utterance_ID']
    return f"dia{dialogue_id}_utt{utterance_id}.mp4"

train_df = pd.read_csv(train_path)
train_df['Filename'] = train_df.apply(generate_filename, axis=1)

train_output_path = '/content/drive/My Drive/MELD-master/data/MELD_Dyadic/train_text_filename_added.csv'

train_df.to_csv(train_output_path, index=False)
dev_df.to_csv(dev_output_path, index=False)
test_df.to_csv(test_output_path, index=False)

print("Processed datasets saved as train_text_processed, dev_text_processed, and test_text_processed.")


# mp4: head movement and posture extraction, data alignment
# final dataset: "Filename", "Sentiment", "Speaker", Utterance", "Avg Head Movement (x,y)", "Avg Posture"

input_dir = "/content/drive/MyDrive/MELD-master/data/MELD_Dyadic/train_videos/train_splits"
output_csv = "/content/drive/MyDrive/MELD_train_head_posture_features_4000_8000.csv"

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

video_files = sorted(os.listdir(input_dir))
print(f"Total videos found: {len(video_files)}")

video_files = video_files[4000:8000]
print(f"Videos to process (4000-8000): {len(video_files)}")

video_features = []

def calculate_head_movement_and_posture(landmarks):
    """
    Calculate head movement and posture using landmarks.
    - Head movement: Based on the displacement of the nose landmark.
    - Posture: Based on the relative positions of the shoulders and nose.
    """
    if not landmarks:
        return None, None

    nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

    head_movement = (nose.x, nose.y)

    posture = abs(left_shoulder.y - right_shoulder.y)

    return head_movement, posture

for video_file in tqdm(video_files, desc="Processing Train Videos"):
    video_path = os.path.join(input_dir, video_file)

    try:
        print(f"\nProcessing file: {video_file}")


        cap = cv2.VideoCapture(video_path)

        head_movements = []
        postures = []

        frame_count = 0
        skip_frames = 5

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % skip_frames != 0:
                frame_count += 1
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                head_movement, posture = calculate_head_movement_and_posture(results.pose_landmarks.landmark)
                if head_movement and posture:
                    head_movements.append(head_movement)
                    postures.append(posture)

            frame_count += 1

        cap.release()

        avg_head_movement = (sum(x[0] for x in head_movements) / len(head_movements),
                             sum(x[1] for x in head_movements) / len(head_movements)) if head_movements else (0, 0)
        avg_posture = sum(postures) / len(postures) if postures else 0

        video_features.append({
            "Filename": video_file,
            "Avg Head Movement (x, y)": avg_head_movement,
            "Avg Posture": avg_posture
        })

    except Exception as e:
        print(f"Error processing {video_file}: {e}")
        continue
print("\nSaving head movement and posture features to CSV...")
with open(output_csv, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Filename", "Avg Head Movement (x, y)", "Avg Posture"])
    writer.writeheader()
    writer.writerows(video_features)

print(f"Features saved to {output_csv}")

#### MELD dataset + video features alignment
features_csv = "/content/drive/MyDrive/MELD_train_head_posture_features_4000_8000.csv"
text_csv = "/content/drive/MyDrive/MELD-master/data/MELD_Dyadic/train_text_filename_added.csv"
output_csv = "/content/drive/MyDrive/4000_8000_original_data_added.csv"

print("Loading feature and text CSV files...")
features_df = pd.read_csv(features_csv)
text_df = pd.read_csv(text_csv)

print("Merging DataFrames on Filename...")
merged_df = pd.merge(features_df, text_df[["Filename", "Speaker", "Sentiment", "Utterance"]], on="Filename", how="inner")

print(f"Saving merged data to {output_csv}...")
merged_df.to_csv(output_csv, index=False)

print(f"Merged data saved to {output_csv}")


# removing duplicates from the dataset
features_csv = "/content/drive/MyDrive/MELD_train_head_posture_features_4000_8000.csv"
text_csv = "/content/drive/MyDrive/MELD-master/data/MELD_Dyadic/train_text_filename_added.csv"
output_csv = "/content/drive/MyDrive/4000_8000_original_data_added.csv"
output_no_duplicates_csv = "/content/drive/MyDrive/4000_8000_no_duplicates.csv"

print("Loading feature and text CSV files...")
features_df = pd.read_csv(features_csv)
text_df = pd.read_csv(text_csv)

print("Merging DataFrames on Filename...")
merged_df = pd.merge(features_df, text_df[["Filename", "Speaker", "Sentiment", "Utterance"]], on="Filename", how="inner")

print("Removing duplicate rows based on the 'Utterance' column...")
merged_no_duplicates_df = merged_df.drop_duplicates(subset=["Utterance"], keep="first")

print(f"Saving data without duplicates to {output_no_duplicates_csv}...")
merged_no_duplicates_df.to_csv(output_no_duplicates_csv, index=False)

print(f"Data without duplicates saved to {output_no_duplicates_csv}")
