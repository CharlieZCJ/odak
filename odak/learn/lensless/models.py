import os
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from os.path import join
from odak.learn.models.components import convolution_layer
from collections import OrderedDict

class spec_track(nn.Module):
    """
    The learned holography model used in the paper, Ziyang Chen and Mustafa Dogan and Josef Spjut and Kaan Akşit. "SpecTrack: Learned Multi-Rotation Tracking via Speckle Imaging." In SIGGRAPH Asia 2024 Posters (SA Posters '24).

    Parameters
    ----------
    reduction : str
                Reduction used for torch.nn.MSELoss and torch.nn.L1Loss. The default is 'sum'.
    device    : torch.device
                Device to run the model on. Default is CPU.
    """
    def __init__(
                 self,
                 reduction = 'sum',
                 device = torch.device('cpu')
                ):
        super(spec_track, self).__init__()
        self.device = device
        self.init_layers()
        self.reduction = reduction
        self.l2 = torch.nn.MSELoss(reduction = self.reduction)
        self.l1 = torch.nn.L1Loss(reduction = self.reduction)
        self.train_history = []
        self.validation_history = []
        
    def init_layers(self):
        """
        Initialize the layers of the network.
        """
        # Convolutional layers with batch normalization and pooling
        self.network = nn.Sequential(OrderedDict([
            ('conv1', nn.Conv2d(5, 32, kernel_size=3, padding=1)),
            ('bn1', nn.BatchNorm2d(32)),
            ('relu1', nn.ReLU()),
            ('pool1', nn.MaxPool2d(kernel_size=3)),

            ('conv2', nn.Conv2d(32, 64, kernel_size=5, padding=1)),
            ('bn2', nn.BatchNorm2d(64)),
            ('relu2', nn.ReLU()),
            ('pool2', nn.MaxPool2d(kernel_size=3)),

            ('conv3', nn.Conv2d(64, 128, kernel_size=7, padding=1)),
            ('bn3', nn.BatchNorm2d(128)),
            ('relu3', nn.ReLU()),
            ('pool3', nn.MaxPool2d(kernel_size=3)),

            ('flatten', nn.Flatten()),

            ('fc1', nn.Linear(6400, 2048)),
            ('fc_bn1', nn.BatchNorm1d(2048)),
            ('relu_fc1', nn.ReLU()),

            ('fc2', nn.Linear(2048, 1024)),
            ('fc_bn2', nn.BatchNorm1d(1024)),
            ('relu_fc2', nn.ReLU()),

            ('fc3', nn.Linear(1024, 512)),
            ('fc_bn3', nn.BatchNorm1d(512)),
            ('relu_fc3', nn.ReLU()),

            ('fc4', nn.Linear(512, 128)),
            ('fc_bn4', nn.BatchNorm1d(128)),
            ('relu_fc4', nn.ReLU()),

            ('fc5', nn.Linear(128, 3))
        ])).to(self.device)
        
    def forward(self, x):
        """
        Forward pass of the network.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor.

        Returns
        -------
        torch.Tensor
            Output tensor.
        """
        return self.network(x)
    
    def evaluate(self, input_data, ground_truth, weights = [100., 1.]):
        """
        Evaluate the model's performance.

        Parameters
        ----------
        input_data    : torch.Tensor
                        Predicted data from the model.
        ground_truth  : torch.Tensor
                        Ground truth data.
        weights       : list
                        Weights for L2 and L1 losses. Default is [100., 1.].

        Returns
        -------
        torch.Tensor
            Combined weighted loss.
        """
        loss = weights[0] * self.l2(input_data, ground_truth) + weights[1] * self.l1(input_data, ground_truth)
        return loss
    
    def fit(self, trainloader, testloader, number_of_epochs = 100, learning_rate = 1e-5, weight_decay = 1e-5, directory = './output'):
        """
        Train the model.

        Parameters
        ----------
        trainloader      : torch.utils.data.DataLoader
                           Training data loader.
        testloader       : torch.utils.data.DataLoader
                           Testing data loader.
        number_of_epochs : int
                           Number of epochs to train for. Default is 100.
        learning_rate    : float
                           Learning rate for the optimizer. Default is 1e-5.
        weight_decay     : float
                           Weight decay for the optimizer. Default is 1e-5.
        directory        : str
                           Directory to save the model weights. Default is './output'.
        """
        t_epoch = tqdm(range(number_of_epochs), leave=False, dynamic_ncols = True)
        prev_validation_loss = float('inf')
        self.optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate, weight_decay=weight_decay)
        for epoch in t_epoch:
            self.train()
            with tqdm(trainloader, unit="batch", ncols=0) as tepoch:
                epoch_loss = []
                for batch_idx, (batch, labels) in enumerate(tepoch):
                    self.optimizer.zero_grad()

                    tepoch.set_description(f"Epoch {epoch}")
                    batch = batch.to(self.device)
                    labels = labels.to(self.device)
                    predicts = torch.squeeze(self.forward(batch))
                    loss = self.evaluate(predicts, labels)
                    loss.backward()
                    epoch_loss.append(loss.item())
                    self.optimizer.step()
                    description = f"Loss: {loss.item():.4f}"
                    t_epoch.set_description(description)
                epoch_avg_loss = sum(epoch_loss)/len(epoch_loss)
                description = f"Avg Epoch loss: {epoch_avg_loss.item():.4f}"
                t_epoch.set_description(description)
                self.train_history.append(epoch_avg_loss)
                
            self.eval()
            with torch.no_grad():
                with tqdm(testloader, unit="batch", ncols=0) as tepoch:
                    val_epoch_loss = []
                    for batch_idx, (batch, labels) in enumerate(tepoch):
                        tepoch.set_description(f"Validation {epoch}")
                        batch = batch.to(self.device)
                        labels = labels.to(self.device)
                        predicts = torch.squeeze(self.forward(batch), dim=1)
                        loss = self.evaluate(predicts, labels)
                        val_epoch_loss.append(loss.item())
                val_epoch_avg_loss = sum(val_epoch_loss)/len(val_epoch_loss)
                description = f"Avg val loss: {val_epoch_avg_loss:.4f}"
                t_epoch.set_description(description)
                self.validation_history.append(val_epoch_avg_loss)

                if  val_epoch_avg_loss < prev_validation_loss:
                    print(f"Model save at EPOCH: {epoch}")
                    self.save_weights(directory  + "_" + str(epoch) + ".pt")
                    prev_validation_loss = val_epoch_avg_loss

    def save_weights(self, filename = './weights.pt'):
        """
        Save the current weights of the network to a file.

        Parameters
        ----------
        filename : str
                   Path to save the weights. Default is './weights.pt'.
        """
        torch.save(self.network.state_dict(), os.path.expanduser(filename))

    def load_weights(self, filename = './weights.pt'):
        """
        Load weights for the network from a file.

        Parameters
        ----------
        filename : str
                   Path to load the weights from. Default is './weights.pt'.
        """
        self.network.load_state_dict(torch.load(os.path.expanduser(filename), weights_only = True))
        self.network.eval()