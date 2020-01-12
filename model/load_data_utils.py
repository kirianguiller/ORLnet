# PyTorch
from torchvision import transforms, datasets


datadir = "/scratch/kgerdes/NN_project/3_spectro_vision/"
# datadir = "/media/wran/TOSHIBA EXT/corpus/mozilla_voice/data/3_spectro_vision_small/"
traindir = datadir + 'train/'
validdir = datadir + 'valid/'
testdir = datadir + 'test/'


# Image transformations
image_transforms = {
    # Train uses data augmentation
    'train':
    transforms.Compose([
        transforms.Resize(size=(224,224)),
#         transforms.RandomRotation(degrees=15),
        # transforms.ColorJitter(),
#         transforms.RandomHorizontalFlip(),
#         transforms.CenterCrop(size=224),  # Image net standards
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # Imagenet standards

        transforms.Normalize([1.808, 1.978, 2.191],
                     [0.758, 0.774, 0.771])  # Spectrogram standards
    ]),
    # Validation does not use augmentation
    'val':
    transforms.Compose([
        transforms.Resize(size=(224,224)),
#         transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        transforms.Normalize([1.808, 1.978, 2.191], [0.758, 0.774, 0.771])  # Spectrogram standards
    ]),
    # Test does not use augmentation
    'test':
    transforms.Compose([
        transforms.Resize(size=(224,224)),
#         transforms.CenterCrop(size=224),
        transforms.ToTensor(),
        # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
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

# # Parameters
# params = {'batch_size': 64,
#           'shuffle': True,
#           'num_workers': 6}

# # Dataloader iterators
# dataloaders = {
#     'train': DataLoader(data['train'], **params),
#     'val': DataLoader(data['val'], **params),
#     'test': DataLoader(data['test'], **params)
# }
