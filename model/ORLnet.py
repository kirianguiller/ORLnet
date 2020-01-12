import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        kernel_size = (3,3)
        padding_2d = (1,1)
        filters = 16

        self.conv_layers = nn.Sequential(
            # input : ((224x224)x3)
            nn.Conv2d(3, filters*1, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*1),
            nn.Dropout2d(0.1),
            nn.Conv2d(filters*1, filters*1, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*1),
            nn.Dropout2d(0.1),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            # output : ((112x112)x1xfilters)

            nn.Conv2d(filters*1, filters*2, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*2),
            nn.Dropout2d(0.1),
            nn.Conv2d(filters*2, filters*2, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*2),
            nn.Dropout2d(0.1),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            # output : ((56x56)x2xfilters)

            nn.Conv2d(filters*2, filters*4, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*4),
            nn.Dropout2d(0.2),
            nn.Conv2d(filters*4, filters*4, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*4),
            nn.Dropout2d(0.2),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            # output : ((28x28)x4xfilters)

            nn.Conv2d(filters*4, filters*8, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*8),
            nn.Dropout2d(0.2),
            nn.Conv2d(filters*8, filters*8, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*8),
            nn.Dropout2d(0.2),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            # output : ((14x14)x8xfilters)

            nn.Conv2d(filters*8, filters*8, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*8),
            nn.Dropout2d(0.3),
            nn.Conv2d(filters*8, filters*8, kernel_size=kernel_size, stride=(1, 1), padding=padding_2d),
            nn.ReLU(),
            nn.BatchNorm2d(filters*8),
            nn.Dropout2d(0.3),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
            # output : ((14x14)x8xfilters)
        )

        self.flaten_weight = filters*8*12*12
        self.flaten_weight = filters*4*25*25
        self.flaten_weight = filters*4*28*28
        self.flaten_weight = filters*8*14*14
        self.flaten_weight = filters*8*7*7

        self.classifier = nn.Sequential(

            nn.Linear(self.flaten_weight, 10), #
            nn.ReLU(),
            nn.BatchNorm1d(10),
            nn.Dropout(0.55),
            nn.Linear(10, 3),
            nn.LogSoftmax(dim=1),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        # print(x.shape)
        x = x.view(-1, self.flaten_weight)
        x = self.classifier(x)

        return x

    def weight_init(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            # if isinstance(m, (nn.Conv2d, nn.Linear)):
            #     nn.init.kaiming_normal(m.weight.data)
            elif isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

