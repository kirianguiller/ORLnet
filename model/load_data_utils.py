# basics import
import os

# PyTorch
from torchvision import transforms, datasets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
datadir = os.path.join(BASE_DIR, 'dataset/')
traindir = datadir + 'train/'
validdir = datadir + 'valid/'
testdir = datadir + 'test/'


# Image transformations
image_transforms = {
    # Train uses data augmentation
    'train':
    transforms.Compose([
        transforms.Resize(size=(224,224)),
        transforms.ToTensor(),
        transforms.Normalize([1.808, 1.978, 2.191],
                     [0.758, 0.774, 0.771])  # Spectrogram standards
    ]),
    # Validation does not use augmentation
    'val':
    transforms.Compose([
        transforms.Resize(size=(224,224)),
        transforms.ToTensor(),
        transforms.Normalize([1.808, 1.978, 2.191], [0.758, 0.774, 0.771])  # Spectrogram standards
    ]),
    # Test does not use augmentation
    'test':
    transforms.Compose([
        transforms.Resize(size=(224,224)),
        transforms.ToTensor(),
        transforms.Normalize([1.808, 1.978, 2.191], [0.758, 0.774, 0.771])  # Spectrogram standards
    ]),
}

# Datasets from each folder
data = {
    'train':
    datasets.ImageFolder(root=traindir, transform=image_transforms['train']),
    'val':
    datasets.ImageFolder(root=validdir, transform=image_transforms['val']),
    'test':
    datasets.ImageFolder(root=testdir, transform=image_transforms['test'])
}
