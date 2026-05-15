"""
Quick Training Script - Fine-tune Pre-trained EfficientNet on Test Images
This will train quickly (10-15 minutes) using your existing test images
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms, models
import os
from tqdm import tqdm

print("🚀 Quick Training Script - EfficientNet Fine-tuning")
print("=" * 60)

# Configuration
DATASET_PATH = "organized_dataset/train"
BATCH_SIZE = 8  # Smaller batch for limited data
NUM_EPOCHS = 10  # Fewer epochs for quick training
LEARNING_RATE = 0.001
MODEL_SAVE_PATH = "plant_disease_efficientnet_quick.pt"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f"📱 Device: {DEVICE}")
if DEVICE.type == 'cuda':
    print(f"   GPU: {torch.cuda.get_device_name(0)}")

# Data transforms with augmentation
train_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load dataset from organized folder
print(f"\n📂 Loading images from: {DATASET_PATH}")
full_dataset = datasets.ImageFolder(root=DATASET_PATH, transform=train_transforms)

# Since we have limited data, use 90/10 split
train_size = int(0.9 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])

# Create separate dataset for validation with val transforms
val_dataset_transformed = datasets.ImageFolder(root=DATASET_PATH, transform=val_transforms)
val_indices = val_dataset.indices
val_dataset = torch.utils.data.Subset(val_dataset_transformed, val_indices)

print(f"✅ Total images: {len(full_dataset)}")
print(f"✅ Training: {train_size} | Validation: {val_size}")
print(f"✅ Classes: {len(full_dataset.classes)}")

# Save class names
class_names = full_dataset.classes
with open('class_names_quick.txt', 'w') as f:
    for name in class_names:
        f.write(f"{name}\n")

# Data loaders
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

# Create model
print("\n🏗️  Loading pre-trained EfficientNet-B0...")
model = models.efficientnet_b0(pretrained=True)

# Freeze early layers
for param in model.features[:-2].parameters():
    param.requires_grad = False

# Replace classifier
num_features = model.classifier[1].in_features
num_classes = len(full_dataset.classes)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(num_features, num_classes)
)

model = model.to(DEVICE)
print(f"✅ Model ready with {num_classes} classes")

# Training setup
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Training function
def train_epoch(model, loader, criterion, optimizer):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc='Training')
    for images, labels in pbar:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({'loss': f'{running_loss/len(loader):.4f}', 'acc': f'{100.*correct/total:.2f}%'})
    
    return running_loss / len(loader), 100. * correct / total

# Validation function
def validate(model, loader, criterion):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(loader, desc='Validation')
        for images, labels in pbar:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({'loss': f'{running_loss/len(loader):.4f}', 'acc': f'{100.*correct/total:.2f}%'})
    
    return running_loss / len(loader), 100. * correct / total

# Training loop
print(f"\n🎯 Starting training for {NUM_EPOCHS} epochs...")
print("=" * 60)

best_val_acc = 0.0

for epoch in range(NUM_EPOCHS):
    print(f"\nEpoch {epoch+1}/{NUM_EPOCHS}")
    print("-" * 60)
    
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer)
    val_loss, val_acc = validate(model, val_loader, criterion)
    
    print(f"\n📊 Results:")
    print(f"   Train: Loss={train_loss:.4f}, Acc={train_acc:.2f}%")
    print(f"   Val:   Loss={val_loss:.4f}, Acc={val_acc:.2f}%")
    
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        print(f"   ✅ Best model saved! (Acc: {val_acc:.2f}%)")

print("\n" + "=" * 60)
print("🎉 Training Complete!")
print("=" * 60)
print(f"✅ Best Validation Accuracy: {best_val_acc:.2f}%")
print(f"✅ Model saved to: {MODEL_SAVE_PATH}")
print(f"\n📝 Next step: Copy model to Flask app and update app.py")
