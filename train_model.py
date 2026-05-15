"""
Plant Disease Detection - Transfer Learning Training Script
Using EfficientNet-B0 for better accuracy and generalization

This script will:
1. Use transfer learning with EfficientNet-B0 (pre-trained on ImageNet)
2. Apply data augmentation for better generalization
3. Train on PlantVillage dataset
4. Save the best model
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

# ==================== CONFIGURATION ====================
DATASET_PATH = "PlantVillage"  # Download from Kaggle: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
BATCH_SIZE = 32
NUM_EPOCHS = 20
LEARNING_RATE = 0.001
NUM_CLASSES = 39  # PlantVillage has 38 disease classes + 1 healthy
MODEL_SAVE_PATH = "plant_disease_efficientnet_best.pt"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(f"🚀 Using device: {DEVICE}")
if DEVICE.type == 'cuda':
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
else:
    print("   ⚠️  Training on CPU (will be slower)")

# ==================== DATA AUGMENTATION ====================
# Training transforms with augmentation
train_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.3),
    transforms.RandomRotation(degrees=30),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Validation transforms (no augmentation)
val_transforms = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ==================== LOAD DATASET ====================
print("\n📂 Loading dataset...")

try:
    # Load training data
    train_dataset = datasets.ImageFolder(
        root=os.path.join(DATASET_PATH, 'train'),
        transform=train_transforms
    )
    
    # Load validation data
    val_dataset = datasets.ImageFolder(
        root=os.path.join(DATASET_PATH, 'val'),
        transform=val_transforms
    )
    
    print(f"✅ Training samples: {len(train_dataset)}")
    print(f"✅ Validation samples: {len(val_dataset)}")
    print(f"✅ Number of classes: {len(train_dataset.classes)}")
    
    # Save class names for later use
    class_names = train_dataset.classes
    with open('class_names.txt', 'w') as f:
        for class_name in class_names:
            f.write(f"{class_name}\n")
    print(f"✅ Class names saved to class_names.txt")
    
except FileNotFoundError:
    print("\n❌ ERROR: Dataset not found!")
    print("\n📥 Please download the PlantVillage dataset:")
    print("   1. Go to: https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset")
    print("   2. Download and extract to the current directory")
    print("   3. Make sure the folder structure is:")
    print("      PlantVillage/")
    print("      ├── train/")
    print("      │   ├── class1/")
    print("      │   ├── class2/")
    print("      │   └── ...")
    print("      └── val/")
    print("          ├── class1/")
    print("          ├── class2/")
    print("          └── ...")
    exit(1)

# Create data loaders
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=4,
    pin_memory=True if DEVICE.type == 'cuda' else False
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=4,
    pin_memory=True if DEVICE.type == 'cuda' else False
)

# ==================== CREATE MODEL ====================
print("\n🏗️  Creating EfficientNet-B0 model...")

# Load pre-trained EfficientNet-B0
model = models.efficientnet_b0(pretrained=True)

# Freeze early layers (we'll fine-tune only the last layers)
for param in model.features[:-3].parameters():
    param.requires_grad = False

# Replace the classifier
num_features = model.classifier[1].in_features
model.classifier = nn.Sequential(
    nn.Dropout(p=0.3),
    nn.Linear(num_features, NUM_CLASSES)
)

model = model.to(DEVICE)

print(f"✅ Model created with {NUM_CLASSES} output classes")
print(f"✅ Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")

# ==================== TRAINING SETUP ====================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=3, verbose=True)

# ==================== TRAINING FUNCTION ====================
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc='Training')
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({
            'loss': f'{running_loss/len(loader):.4f}',
            'acc': f'{100.*correct/total:.2f}%'
        })
    
    return running_loss / len(loader), 100. * correct / total

# ==================== VALIDATION FUNCTION ====================
def validate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        pbar = tqdm(loader, desc='Validation')
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            pbar.set_postfix({
                'loss': f'{running_loss/len(loader):.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })
    
    return running_loss / len(loader), 100. * correct / total

# ==================== TRAINING LOOP ====================
print(f"\n🎯 Starting training for {NUM_EPOCHS} epochs...\n")

best_val_acc = 0.0
train_losses, val_losses = [], []
train_accs, val_accs = [], []

for epoch in range(NUM_EPOCHS):
    print(f"\n{'='*60}")
    print(f"Epoch {epoch+1}/{NUM_EPOCHS}")
    print(f"{'='*60}")
    
    # Train
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, DEVICE)
    
    # Validate
    val_loss, val_acc = validate(model, val_loader, criterion, DEVICE)
    
    # Update learning rate
    scheduler.step(val_acc)
    
    # Save metrics
    train_losses.append(train_loss)
    val_losses.append(val_loss)
    train_accs.append(train_acc)
    val_accs.append(val_acc)
    
    # Print summary
    print(f"\n📊 Epoch {epoch+1} Summary:")
    print(f"   Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
    print(f"   Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.2f}%")
    
    # Save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        print(f"   ✅ New best model saved! (Val Acc: {val_acc:.2f}%)")

# ==================== SAVE FINAL MODEL ====================
print(f"\n{'='*60}")
print(f"🎉 Training Complete!")
print(f"{'='*60}")
print(f"✅ Best Validation Accuracy: {best_val_acc:.2f}%")
print(f"✅ Model saved to: {MODEL_SAVE_PATH}")

# ==================== PLOT TRAINING HISTORY ====================
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss')
plt.plot(val_losses, label='Val Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(train_accs, label='Train Acc')
plt.plot(val_accs, label='Val Acc')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.title('Training and Validation Accuracy')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('training_history.png')
print(f"✅ Training history plot saved to: training_history.png")

print("\n📝 Next steps:")
print("   1. Copy the model file to Flask app:")
print(f"      cp {MODEL_SAVE_PATH} 'Flask Deployed App/'")
print("   2. Update Flask app to use the new model")
print("   3. Test with new images!")
