from itinero_model import CrimeClassifier
from news_data_fetcher import NewsAPI
from transformers import get_linear_schedule_with_warmup

#---------------------------------------------------------------------------------------------
# 1) Preprocess the articles and split them into training, validation, and testing sets
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
# 3) Evaluate the accuracy of the current model, if any
#---------------------------------------------------------------------------------------------

model_path = crime_classifier.model_path

# If there is a model path defined, evaluate its accuracy for comparisons during training
if model_path:
    crime_classifier.load_model(model_path)
    best_val_accuracy = crime_classifier.evaluate_model(val_loader)
    print(f"The current model has an accuracy of {best_val_accuracy:.2f}%")
else:
    best_val_accuracy = 0.0

#---------------------------------------------------------------------------------------------
# 4) Implement training loop with validation
#---------------------------------------------------------------------------------------------

# Make CrimeClassifer attributes accessible during runtime
model = crime_classifier.model
optimizer = crime_classifier.optimizer
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=len(train_loader))
device = crime_classifier.device

# Transfer the model's parameters and operations to the specifed device
model.to(device)

epochs = int(input("Enter the number of epochs: "))

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
    
    val_accuracy = crime_classifier.evaluate_model(val_loader)

    print(f"Epoch {epoch + 1} - Validation Accuracy: {val_accuracy:.2f}%")

    # Overwrite the model's state if a higher accuracy is found
    if val_accuracy > best_val_accuracy:
        print("Higher accuracy found, overwriting model path...")
        best_val_accuracy = val_accuracy

        if model_path:
            print(f"Writing to file: {model_path}")
            crime_classifier.save_model(model_path)
        else:
            print(f"No model path found, creating .pth file")
            model_path = "./itinero/backend/app/best_model_state.pth"
            crime_classifier.save_model(model_path)

#---------------------------------------------------------------------------------------------
# 5) Potential testing/deployment code
#---------------------------------------------------------------------------------------------

# Use the best model available for testing or deployment
crime_classifier.load_model(model_path)

test_accuracy = crime_classifier.evaluate_model(test_loader)

print(f"Test Accuracy: {test_accuracy:.2f}%")
