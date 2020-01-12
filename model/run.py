from train_model_utils import train
from load_data_utils import data
import smallnet

import torch
from torch import optim, cuda
import torch.nn as nn
from torch.utils.data import DataLoader

# Useful for examining network
from torchsummary import summary

# 1 : dropout > activation > BN
# 2 : activation > DO > BN
# 3 : activation > BN > DO

# DO_BN_acti
# BN_DO_acti
# totry : - activation > DO > BN
#         - activation > BN > DO
# next : linear 10 but last layer BN>DO

path_save = "/scratch/kgerdes/NN_project/saved_models/"
save_file_name = 'linear_10_final.pt'
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


net = smallnet.Net()

## net = net.apply(init_weights)
# net = net.apply(weights_init)
net.weight_init()
criterion = nn.NLLLoss()
optimizer = optim.Adam(net.parameters())
# optimizer = optim.SGD(net.parameters(),lr=0.001, momentum=0.9)

# net.weight_init()
if train_on_gpu:
    net.to(device)

summary(net, input_size=(3,224,224))

# net.load_state_dict(torch.load(path_save + save_file_name.replace('3', '2')))

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
