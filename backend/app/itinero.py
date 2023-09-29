import torch
import torch.nn as nn

#Divide each feature of 'Itinero' into initializable classes

class CrimeClassifier:

    #Set ML attributes to the default, recommended values
    embedding_dim = 128
    hidden_dim = 256
    output_dim = 1
    num_layers = 2
    dropout = 0.2

    #The ArticleClassifier object is initialized with the respective 'model_path' file, 
    #which will contain the current state of the ML model

    def __init__(self, vocab_size, model_path=None):
        self.vocab_size = vocab_size

        if model_path:
            self.load_model(model_path)
        else:
            self.model = self.build_model()

    def build_model(self):
        model = nn.Sequential(
            nn.Embedding(self.vocab_size, self.embedding_dim),
            nn.LSTM(self.embedding_dim, self.hidden_dim, self.num_layers, self.dropout),
            nn.Linear(self.hidden_dim, self.output_dim),
            nn.Sigmoid()
        )
        return model
    
    def train_model(self, data):
        #To implement
        pass
    
    def save_model(self, model_path):
        torch.save(self.model.state_dict(), model_path)

    def load_model(self, model_path):
        self.model.state_dict(torch.load(model_path))
        self.model.eval()

    def classify_articles(self, article_titles):
        #To implement
        return None

class RestaurantRecommender:

    def __init__(self):
        pass