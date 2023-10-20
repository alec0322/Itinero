import torch
import os
import random
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertForSequenceClassification, BertTokenizer

# Divide each feature of 'Itinero' into initializable classes

class CrimeClassifier:

    # The CrimeClassifier model is initialized with the respective 'model_path' file, 
    # which will contain the current state of the ML model

    def __init__(self):
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.best_val_accuracy = 0.0

        # Check if there is a model state in the current directory
        if os.path.exists("./itinero/backend/app/best_model_state.pth"):
            self.model_path = "./itinero/backend/app/best_model_state.pth"
        else:
            self.model_path = None
       
    def load_model(self, model_path):
        self.model.state_dict(torch.load(model_path))

    def save_model(self, model_path):
        torch.save(self.model.state_dict(), model_path)

    @property
    def best_val_accuracy(self):
        return self.best_val_accuracy
    
    @best_val_accuracy.setter
    def best_val_accuracy(self, value):
        self.best_val_accuracy = value

    # Function to preprocess and format articles
    def preprocess_articles(self, articles, label):
        processed_data = []

        for title in articles:
            # Tokenization
            tokens = self.tokenizer.encode(title, add_special_tokens=True)

            # Padding/Truncation to a fixed length
            max_seq_length = 128
            if len(tokens) > max_seq_length:
                tokens = tokens[:max_seq_length]
            else:
                tokens = tokens + [0] * (max_seq_length - len(tokens))

            # Convert tokens to IDs
            input_ids = tokens
            attention_mask = [1] * len(tokens)

            processed_data.append({
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "label": label
            })
        
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
        labels = torch.tensor([example["label"] for example in dataset])

        tensor_dataset = TensorDataset(input_ids, attention_masks, labels)
        data_loader = DataLoader(tensor_dataset, batch_size=batch_size, shuffle=shuffle)

        return data_loader

    def classify_articles(self, article_titles):
        # To implement
        return None
