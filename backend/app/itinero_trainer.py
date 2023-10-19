import torch
from itinero_model import CrimeClassifier
from news_data_fetcher import NewsAPI
from transformers import BertForSequenceClassification, BertTokenizer, AdamW, get_linear_schedule_with_warmup

#---------------------------------------------------------------------------------------------
# 1) Preprocess and split the data into training, validation, and testing sets
#---------------------------------------------------------------------------------------------

# Initialize the fine-tuned Bert classifier
crime_classifier = CrimeClassifier()

# Establish API connection
news_api = NewsAPI()

# Gather crime-related articles and preprocess
crime_articles = news_api.get_crime_articles(max_articles=500)
processed_crime_data = crime_classifier.preprocess_articles(crime_articles, label=1)

# Gather non-crime-related articles and preprocess
non_crime_articles = news_api.get_non_crime_articles(max_articles=500)
processed_non_crime_data = crime_classifier.preprocess_articles(non_crime_articles, label=0)

# Combine the datasets
tokenized_data = processed_crime_data + processed_non_crime_data

# Define the split ratios: training (70%), validation (15%), and testing (15%)
train_data, val_data, test_data = crime_classifier.split_data(tokenized_data, 0.7, 0.15, 0.15)

#---------------------------------------------------------------------------------------------
# 2) Create DataLoaders and TensorDatasets for training, validation, and testing
#---------------------------------------------------------------------------------------------

batch_size = 32
train_loader = crime_classifier.create_dataloader(train_data, batch_size=batch_size, shuffle=True)
val_loader = crime_classifier.create_dataloader(val_data, batch_size=batch_size, shuffle=False)
test_loader = crime_classifier.create_dataloader(test_data, batch_size=batch_size, shuffle=False)

#---------------------------------------------------------------------------------------------
# 3) Implement training loop with validation
#---------------------------------------------------------------------------------------------

# Initialize the BERT model and optimizer
model = crime_classifier.model
optimizer = AdamW(model.parameters(), lr=2e-5, no_deprecation_warning=True)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_loader))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

epochs = 3
best_val_accuracy = 0.0
best_model = None

for epoch in range(epochs):
    model.train()
    for train_batch in train_loader:
        input_ids, masks, labels = train_batch
        input_ids, masks, labels = input_ids.to(device), masks.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask=masks, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        scheduler.step()
    
    model.eval()
    val_total = 0
    val_correct = 0
    with torch.no_grad():
        for val_batch in val_loader:
            input_ids, masks, labels = val_batch
            input_ids, masks, labels = input_ids.to(device), masks.to(device), labels.to(device)

            outputs = model(input_ids, attention_mask=masks)
            _, predicted = torch.max(outputs.logits, 1)
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()
    
    val_accuracy = 100 * val_correct / val_total

    print(f"Epoch {epoch + 1} - Validation Accuracy: {val_accuracy:.2f}%")

    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy
        best_model = model.state_dict()
    
if best_model:
    torch.save(best_model, "./itinero/backend/app/best_model_state.pth")

#---------------------------------------------------------------------------------------------
# 4) Testing/deployment
#---------------------------------------------------------------------------------------------

# Use the best model available for testing or deployment

model.load_state_dict(torch.load("./itinero/backend/app/best_model_state.pth"))
model.eval()

test_total = 0
test_correct = 0
with torch.no_grad():
    for test_batch in test_loader:
        input_ids, masks, labels = test_batch
        input_ids, masks, labels = input_ids.to(device), masks.to(device), labels.to(device)

        outputs = model(input_ids, attention_mask=masks)
        _, predicted = torch.max(outputs.logits, 1)
        test_total += labels.size(0)
        test_correct += (predicted == labels).sum().item()

test_accuracy = 100 * test_correct / test_total
print(f"Test Accuracy: {test_accuracy:.2f}%")
