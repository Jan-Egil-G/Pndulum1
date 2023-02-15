
#læring steg 3


import torchvision
from torch.utils.data import Dataset, DataLoader
import numpy as np
import math



import y_model
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters 



def train_model_ctrl(num_epochs,batch_size,learning_rateLow,lognum,loadCkpt,testNum,startline,stopline,AddNoise):

    class WineDataset(Dataset):

        def __init__(self):
            # Initialize data, download, etc.
            #  id	 empty-frame	 sts	 angel error	 diff-time  v1 	 v2	 pos	 dt-v1 	 dt-v2	 dt-pos 	 act1 (raw)	 act2

            xy = np.loadtxt(f"./LogDir/pingpong/Log_0.csv", delimiter=',', dtype=np.float32, skiprows=startline,max_rows=stopline-startline)
            self.n_samples = xy.shape[0]
            

            # here the first column is the class label, the rest are the features
            self.x_data = torch.from_numpy(xy[:, [0,1,2,3,4]]) # size [n_samples, n_features]   data  V1V2posdtdtdtact1act2
            self.y_data = torch.from_numpy(xy[:, [8,9]]) # size [n_samples, 1]           label  [8,9]

        # we can call len(dataset) to return the sizes
        def __len__(self):
            return self.n_samples
        # support indexing such that dataset[i] can be used to get i-th sample
        def __getitem__(self, index):

            return self.x_data[index], self.y_data[index]



    learning_rate=learning_rateLow
    # create dataset
    dataset = WineDataset()
    print("gbfr")
    print(dataset.n_samples)
    # get first sample and unpack

    train_loader = DataLoader(dataset=dataset,
                            batch_size=batch_size,
                            shuffle=True,
                            num_workers=0)




    model = y_model.NeuralNetCtrl().to(device)

    # Loss and optimizer
    criterion = nn.L1Loss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  
    checkpoint = {
    "model_state": model.state_dict(),
    "optim_state": optimizer.state_dict()
    }

    # yes_or_no = input("yes or no; load chkpt?")
    if loadCkpt:
        checkpoint = torch.load('./chkp2/ctrl/chkpt1.pth')
        model.load_state_dict(checkpoint['model_state'])
        optimizer.load_state_dict(checkpoint['optim_state'])
    model.train()
        #epoch = checkpoint['epoch']

    # Train the model
    n_total_steps = len(train_loader)

    print(f"step: {n_total_steps}")
    for epoch in range(num_epochs):
        print("epoch: ", epoch)
        for i, (images, labels) in enumerate(train_loader):  
            # print(i)
            if AddNoise:
                imageAdd=torch.rand(5)*0.0001
                labelAdd=torch.rand(2)*0.0001
            else:
                imageAdd=torch.zeros(5)
                labelAdd=torch.zeros(2)



            imageAdd=imageAdd.to(device)
            labelAdd=labelAdd.to(device)

            labels = labels.to(device)
            images = images.to(device)
            #print(f"images: {images}")
            #print(f"labels: {labels}")
            # Forward pass
            outputs = model(images+imageAdd)
            #print(f"outputs: {outputs}")
            loss = criterion(outputs, labels+labelAdd)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            #print("hei#")
            
            if (i+1) % 1 == 0:
                print (f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item():.4f}')

    print(f'Finished Training')

    # Save the model state dict
    state = {'model_state': model.state_dict()}

    # Save the optimizer state dict
    state['optim_state'] = optimizer.state_dict()

    # Save the state dict
    torch.save(state, './chkp2/ctrl/chkpt1.pth')


