from google.colab import drive
drive.mount('/content/drive')

import os
os.listdir('/content/drive/My Drive')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
import seaborn as sns
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
from torch import nn
from torch.optim import AdamW
from tqdm import tqdm


file_path = "/content/drive/MyDrive/4000_8000_no_duplicates.csv"

print("Loading the dataset...")
df = pd.read_csv(file_path)

print("Removing duplicates based on the 'Utterance' column...")
df = df.drop_duplicates(subset="Utterance", keep="first")

print("Mapping sentiment labels to integers...")
label_mapping = {"negative": 0, "neutral": 1, "positive": 2}
df['Sentiment'] = df['Sentiment'].str.lower()
df['Sentiment'] = df['Sentiment'].map(label_mapping)
df['Sentiment'] = df['Sentiment'].fillna(1).astype(int)
labels = df['Sentiment'].tolist()
print("Sentiment labels mapped successfully.")

# Split "Avg Head Movement (x, y)" into two separate columns
df[["Head Movement X", "Head Movement Y"]] = df["Avg Head Movement (x, y)"] \
    .str.strip("()") \
    .str.split(",", expand=True) \
    .astype(float)

video_features = df[["Head Movement X", "Head Movement Y", "Avg Posture"]].fillna(0).values

text_data = df["Utterance"].tolist()

# train-test split
train_texts, test_texts, train_video_features, test_video_features, train_labels, test_labels = train_test_split(
    text_data, video_features, labels, test_size=0.2, random_state=42
)

# tokenizer and BERT model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = BertModel.from_pretrained("bert-base-uncased")

class MultimodalDataset(Dataset):
    def __init__(self, texts, video_features, labels, tokenizer, max_len=128):
        self.texts = texts
        self.video_features = video_features
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        feature = torch.tensor(self.video_features[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        encoding = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_len,
            return_tensors="pt"
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'video_features': feature,
            'label': label
        }

batch_size = 16
train_dataset = MultimodalDataset(train_texts, train_video_features, train_labels, tokenizer)
test_dataset = MultimodalDataset(test_texts, test_video_features, test_labels, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

class MultimodalModel(nn.Module):
    def __init__(self, bert_model, video_feature_dim, num_classes):
        super(MultimodalModel, self).__init__()
        self.bert = bert_model
        self.video_fc = nn.Linear(video_feature_dim, 128)
        self.classifier = nn.Linear(768 + 128, num_classes)
        self.dropout = nn.Dropout(0.3)

    def forward(self, input_ids, attention_mask, video_features):
        bert_output = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        text_features = bert_output.pooler_output
        video_features = self.video_fc(video_features)
        combined_features = torch.cat((text_features, video_features), dim=1)
        combined_features = self.dropout(combined_features)
        logits = self.classifier(combined_features)
        return logits

video_feature_dim = video_features.shape[1]
num_classes = 3
model = MultimodalModel(bert_model, video_feature_dim, num_classes)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = AdamW(model.parameters(), lr=5e-5)
criterion = nn.CrossEntropyLoss()

epochs = 4
for epoch in range(epochs):
    model.train()
    loop = tqdm(train_loader, desc=f"Training Epoch {epoch+1}")
    total_loss = 0

    for batch in loop:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        video_features = batch['video_features'].to(device)
        labels = batch['label'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, video_features=video_features)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        loop.set_postfix(loss=loss.item())

    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch+1} completed. Average Loss: {avg_loss:.4f}")

model.eval()
predictions, true_labels = [], []

with torch.no_grad():
    for batch in tqdm(test_loader, desc="Evaluating"):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        video_features = batch['video_features'].to(device)
        labels = batch['label'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, video_features=video_features)
        logits = outputs
        preds = torch.argmax(logits, dim=1)
        predictions.extend(preds.cpu().tolist())
        true_labels.extend(labels.cpu().tolist())

accuracy = accuracy_score(true_labels, predictions)
f1 = f1_score(true_labels, predictions, average="weighted")
print("\nAccuracy:", accuracy)
print("F1 Score:", f1)

test_indices = range(len(test_labels))
test_df = df.iloc[test_indices].reset_index(drop=True)

if len(test_df) == len(test_labels):
    test_df["True_Label"] = test_labels
    test_df["Predicted_Label"] = predictions

    cm = confusion_matrix(test_df["True_Label"], test_df["Predicted_Label"])
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Negative", "Neutral", "Positive"],
                yticklabels=["Negative", "Neutral", "Positive"])
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix: Text + Video Features")
    plt.show()

    print("\nClassification Report:")
    print(classification_report(test_df["True_Label"], test_df["Predicted_Label"],
                                target_names=["Negative", "Neutral", "Positive"]))

    if "Speaker" in test_df.columns:
        speaker_accuracy = test_df.groupby("Speaker").apply(
            lambda group: (group["True_Label"] == group["Predicted_Label"]).mean()
        )
        print("\nPer-speaker accuracy analysis:")
        print(speaker_accuracy.sort_values(ascending=False))

        plt.figure(figsize=(10, 6))
        speaker_accuracy.sort_values(ascending=False).plot(kind="bar", color="skyblue")
        plt.title("Per-Speaker Accuracy")
        plt.xlabel("Speaker")
        plt.ylabel("Accuracy")
        plt.show()
else:
    print("Mismatch between test dataset size and labels/predictions.")
