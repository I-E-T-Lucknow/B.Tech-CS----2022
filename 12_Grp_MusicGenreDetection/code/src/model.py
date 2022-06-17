import torch

torch.manual_seed(123)
from torch.nn import Module, Conv2d, MaxPool2d, Linear, Dropout, BatchNorm2d
import torch.nn.functional as F


class genreNet(Module):
    def __init__(self):
        super(genreNet, self).__init__()

        self.conv1 = Conv2d(
            in_channels=1, out_channels=64, kernel_size=3, stride=1, padding=1
        )
        torch.nn.init.xavier_uniform(self.conv1.weight)
        self.bn1 = BatchNorm2d(64)
        self.pool1 = MaxPool2d(kernel_size=2)

        self.conv2 = Conv2d(
            in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1
        )
        torch.nn.init.xavier_uniform(self.conv2.weight)
        self.bn2 = BatchNorm2d(128)
        self.pool2 = MaxPool2d(kernel_size=2)

        self.conv3 = Conv2d(
            in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1
        )
        torch.nn.init.xavier_uniform(self.conv3.weight)
        self.bn3 = BatchNorm2d(256)
        self.pool3 = MaxPool2d(kernel_size=4)

        self.conv4 = Conv2d(
            in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1
        )
        torch.nn.init.xavier_uniform(self.conv4.weight)
        self.bn4 = BatchNorm2d(512)
        self.pool4 = MaxPool2d(kernel_size=4)

        self.fc1 = Linear(in_features=2048, out_features=1024)
        self.drop1 = Dropout(0.5)

        self.fc2 = Linear(in_features=1024, out_features=256)
        self.drop2 = Dropout(0.5)

        self.fc3 = Linear(in_features=256, out_features=10)

    def forward(self, inp):
        x = F.relu(self.bn1(self.conv1(inp)))
        x = self.pool1(x)

        x = F.relu(self.bn2(self.conv2(x)))
        x = self.pool2(x)

        x = F.relu(self.bn3(self.conv3(x)))
        x = self.pool3(x)

        x = F.relu(self.bn4(self.conv4(x)))
        x = self.pool4(x)

        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1(x))
        x = self.drop1(x)

        x = F.relu(self.fc2(x))
        x = self.drop2(x)

        x = F.log_softmax(self.fc3(x))
        return x
