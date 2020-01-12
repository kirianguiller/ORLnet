from train_model_utils import train
from load_data_utils import data
import ORLnet

import torch
from torch import optim, cuda
import torch.nn as nn
from torch.utils.data import DataLoader

# Useful for examining network
from torchsummary import summary


path_save = "/save/"
save_file_name = 'name_model.pt'
checkpoint_path = save_file_name.replace('pt', 'pth')

print('-------- NAME ---------\n{}\n'.format(save_file_name))

# Parameters
params = {'batch_size': 64,
          'shuffle': True,
          'num_workers': 6}

# Dataloader iterators
dataloaders = {
    'train': DataLoader(data['train'], **params),
    'val': DataLoader(data['val'], **params),
    'test': DataLoader(data['test'], **params)
}

# Whether to train on a gpu
train_on_gpu = cuda.is_available()
print(f'Train on gpu: {train_on_gpu}')
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Number of gpus
if train_on_gpu:
    gpu_count = cuda.device_count()
    print(f'{gpu_count} gpus detected.')
    if gpu_count > 1:
        multi_gpu = True
    else:
        multi_gpu = False
else :
    multi_gpu = None


net = ORLnet.Net()
net.weight_init()

criterion = nn.NLLLoss()
optimizer = optim.Adam(net.parameters())

if train_on_gpu:
    net.to(device)

summary(net, input_size=(3,224,224))

model, history = train(
    net,
    criterion,
    optimizer,
    dataloaders['train'],
    dataloaders['val'],
    dataloaders['test'],
    save_file_name=path_save + save_file_name,
    max_epochs_stop=30,
    n_epochs=70,
    print_every=1,
    train_on_gpu=train_on_gpu)

print(history)
print(save_file_name)
history.to_csv(path_save + save_file_name.replace('pt', 'csv'))
