import torch
import os
import random
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertForSequenceClassification, BertTokenizer, AdamW

# Divide each feature of 'Itinero' into initializable classes

class CrimeClassifier:

    # The CrimeClassifier model is initialized with the respective 'model_path' file, 
    # which will contain the current state of the ML model

    def __init__(self):
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.optimizer = AdamW(self.model.parameters(), lr=23-5, no_deprecation_warning=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Check if there is a model state i n the current directory
        if os.path.exists("./itinero/backend/app/best_model_state.pth"):
            self.model_path = "./itinero/backend/app/best_model_state.pth"
        else:
            self.model_path = None
       
    def save_model(self, model_path):
        torch.save(self.model.state_dict(), model_path)

    def load_model(self, model_path):
        self.model.load_state_dict(torch.load(model_path))

    # Function to preprocess and format articles
    def preprocess_articles(self, articles, label=None):
        processed_data = []

        for title in articles:
            # Tokenization
            tokens = self.tokenizer.encode(title, add_special_tokens=True)

            # Truncate tokens to a fixed length
            max_seq_length = 128
            if len(tokens) > max_seq_length:
                tokens = tokens[:max_seq_length]
            else:
                tokens = tokens + [0] * (max_seq_length - len(tokens))

            # Convert tokens to IDs
            input_ids = tokens
            attention_mask = [1] * len(tokens)

            data = {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "article_title": title
            }

            if label is not None:
                data["label"] = label

            processed_data.append(data)
        
        return processed_data
    
    # Function to split the data into training, validation, and test sets
    def split_data(self, tokenized_data, train_ratio, val_ratio, test_ratio):
        
        assert train_ratio + val_ratio + test_ratio == 1.0, "Ratios should sum to 1.0"

        # Shuffle the data
        random.shuffle(tokenized_data)

        total_size = len(tokenized_data)
        train_size = int(train_ratio * total_size)
        val_size = int(val_ratio * total_size)

        # Splice the array accordingly
        train_data = tokenized_data[:train_size]
        val_data = tokenized_data[train_size:train_size + val_size]
        test_data = tokenized_data[train_size + val_size:]

        return train_data, val_data, test_data
    
    # Function to generate DataLoaders (iterables over given datasets)
    def create_dataloader(self, dataset, batch_size, shuffle):

        # Create TensorDataset from given dataset
        input_ids = torch.tensor([example["input_ids"] for example in dataset])
        attention_masks = torch.tensor([example["attention_mask"] for example in dataset])

        if "label" in dataset[0]:
            labels = torch.tensor([example["label"] for example in dataset])
            tensor_dataset = TensorDataset(input_ids, attention_masks, labels)
            dataloader = DataLoader(tensor_dataset, batch_size=batch_size, shuffle=shuffle)
        else:
            tensor_dataset = TensorDataset(input_ids, attention_masks)
            dataloader = DataLoader(tensor_dataset, batch_size=batch_size, shuffle=shuffle)      

        return dataloader
        
    # Function to calculate the model's accuracy depending on a given dataloader
    def evaluate_model(self, dataloader):
        self.model.to(self.device)
        self.model.eval()

        total_predictions = 0
        correct_predictions = 0
        with torch.no_grad():
            for batch in dataloader:
                input_ids, masks, labels = batch
                input_ids, masks, labels = input_ids.to(self.device), masks.to(self.device), labels.to(self.device)

                outputs = self.model(input_ids, masks)
                _, predicted = torch.max(outputs.logits, 1)
                total_predictions += labels.size(0)
                correct_predictions += (predicted == labels).sum().item()

        accuracy = 100 * correct_predictions / total_predictions

        return accuracy

    # Function to classify whether articles in a given set are crime-related or not
    def classify_articles(self, article_titles):
        processed_data = self.preprocess_articles(article_titles)

        batch_size = 32
        article_loader = self.create_dataloader(processed_data, batch_size=batch_size, shuffle=False, )
        
        self.load_model(self.model_path)
        self.model.to(self.device)
        self.model.eval()

        crime_related_articles = []

        with torch.no_grad():
            for batch in article_loader:
                input_ids = batch["input_ids"].to(self.device)
                masks = batch["attention_mask"].to(self.device)
                article_titles = batch["article_title"].to(self.device)

                outputs = self.model(input_ids, masks)
                probabilities = torch.softmax(outputs.logits, dim=1)
                predicted_classes = torch.argmax(probabilities, dim=1)
            
                for i, predicted_class in enumerate(predicted_classes):
                    if predicted_class == 1:
                        crime_related_articles.append(article_titles[i])

        return crime_related_articles
