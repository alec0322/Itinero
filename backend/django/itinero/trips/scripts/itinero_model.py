import torch
import os
import random
# from backend.django.itinero.trips.scripts.news_data_fetcher import NewsAPI
from .news_data_fetcher import NewsAPI
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertForSequenceClassification, BertTokenizer, AdamW

# Divide each feature of 'Itinero' into initializable classes

class CrimeClassifier:

    # The CrimeClassifier model is initialized with the respective 'model_path' file, 
    # which will contain the current state of the ML model

    def __init__(self):
        # Establish API connection
        self.news_api = NewsAPI()

        # Define device to be used
        self.device = torch.device("cpu")

        # Initialize pre-trained Bert Sequence Classification model
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2).to(self.device) # type: ignore

        # Initialize Bert Tokenizer
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

        # Initialize AdamW optimizer
        self.optimizer = AdamW(self.model.parameters(), lr=23-5, no_deprecation_warning=True)

        # Check if there is a model state in the current directory
        if os.path.exists("./backend/app/best_crime_classifier_state.pth"):
            self.model_path = "./backend/app/best_crime_classifier_state.pth"
        else:
            self.model_path = None
    
    # Function to save model state to current directory
    def save_model(self, model_path):
        torch.save(self.model.state_dict(), model_path)

    # Function to load model state from current directory
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

        self.model.to(self.device) # type: ignore
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

        classified_articles = {"Crime-related": [], "Not crime-related": []}

        for title in article_titles:
            # Tokenize the given article title
            input_ids = self.tokenizer.encode(title, add_special_tokens=True)

            with torch.no_grad():
                input_ids = torch.tensor(input_ids).unsqueeze(0)
                outputs = self.model(input_ids)
                probabilities = torch.softmax(outputs.logits, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
            
            if predicted_class == 1:
                classified_articles["Crime-related"].append(title)
            else:
                classified_articles["Not crime-related"].append(title)
        
        return classified_articles
    
    # Function to calculate the 'crime index' of a given city
    def calculate_crime_index(self, city):

        city_articles = self.news_api.get_city_articles(city)

        classified_city_articles = self.classify_articles(city_articles)

        # print(classified_city_articles)

        crime_related = len(classified_city_articles["Crime-related"])
        not_crime_related = len(classified_city_articles["Not crime-related"])

        crime_index = crime_related / (crime_related + not_crime_related)

        return crime_index


# crime_rater = CrimeClassifier()

# city = "miami"
# crime_index = crime_rater.calculate_crime_index(city)

# print(f"{city} has a crime index of {crime_index}")