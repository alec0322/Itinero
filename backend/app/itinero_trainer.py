import torch
from itinero import CrimeClassifier
from news_data_fetcher import NewsAPI
from torch.utils.data import DataLoader, Dataset
from transformers import BertForSequenceClassification, BertTokenizer

# Load pre-trained BERT model and tokenizer
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Establish API connection and gather articles
news_api = NewsAPI()

crime_articles = news_api.get_crime_articles(max_articles=500)
non_crime_articles = news_api.get_non_crime_articles(max_articles=500)

# Label the available data
labeled_data = [{"text": article_title, "label": 1} for article_title in crime_articles] + \
               [{"text": article_title, "label": 0} for article_title in non_crime_articles]

# Define class for trainer datasets
class ArticleDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=128):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        item = self.data[index]
        text = item["text"]
        label = item["label"]
        encoding = self.tokenizer(text, padding="max_length", truncation=True, max_length=self.max_length)
        return {
            "input_ids": torch.tensor(encoding["input_ids"], dtype=torch.long),
            "attention_mask": torch.tensor(encoding["attention_mask"], dtype=torch.long),
            "labels": torch.tensor(label, dtype=torch.long),
        }

# Create a custom dataset
custom_dataset = ArticleDataset(data=labeled_data, tokenizer=tokenizer)

# Create a DataLoader
batch_size = 32
data_loader = DataLoader(custom_dataset, batch_size=batch_size, shuffle=True)

# Initialize CrimeClassifier
vocab_size = len(tokenizer)
crime_classifier = CrimeClassifier(vocab_size=vocab_size)

crime_classifier.train_model(data_loader)

model_path = "crime_classifier_model.pth"
crime_classifier.save_model(model_path)