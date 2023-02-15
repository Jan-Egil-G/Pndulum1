
#læring steg 1


from torch.utils.tensorboard import SummaryWriter

# Create a SummaryWriter object

import z_CommonFunc as zcf

from torch.utils.data import Dataset, DataLoader
import numpy as np
import z_model

import torch.multiprocessing
import torch
import time

import torch.nn as nn

from datetime import datetime

# Create a unique log directory for each run
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
log_dir = "LogDir/fit/" + current_time

writer = SummaryWriter(log_dir)

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class Num1Dataset(Dataset):

    def __init__(self,startline,stopline,shuffleColumn,ColList,LabelNo):
        # Initialize data, download, etc.
        # 

        xy = np.loadtxt(f"./LogDir/norm/Log_0.csv", delimiter=',', dtype=np.float32, skiprows=startline, max_rows=stopline-startline)
        self.n_samples = xy.shape[0]

#        ColList=[2,3,6,8] #features for model 1
        # shuffle
        if(shuffleColumn>-1):
            np.random.shuffle(xy[:,ColList[shuffleColumn]])
        
        # here the first column is the class label, the rest are the features
        self.x1_data = torch.from_numpy(xy[:, ColList]) # size [n_samples, n_features]   data  V1V2posdtdtdtact1act2
        self.y1_data = torch.from_numpy(xy[:, [LabelNo]]) # size [n_samples, 1]           label


    # we can call len(dataset) to return the sizes
    def __len__(self):
        return self.n_samples-1

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x1_data[index], self.y1_data[index+1]

class Num1ValDataset(Dataset):

    def __init__(self,startline,stopline,ColList,LabelNo):
        # Initialize data, download, etc.
        # 

        xy = np.loadtxt(f"./LogDir/testset/Log_0.csv", delimiter=',', dtype=np.float32, skiprows=startline, max_rows=stopline-startline)
        self.n_samples = xy.shape[0]
        

        # here the first column is the class label, the rest are the features
        self.x1_data = torch.from_numpy(xy[:, ColList]) # size [n_samples, n_features]   data  V1V2posdtdtdtact1act2
        self.y1_data = torch.from_numpy(xy[:, [LabelNo]]) # size [n_samples, 1]           label


    # we can call len(dataset) to return the sizes
    def __len__(self):
        return self.n_samples-1

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x1_data[index], self.y1_data[index+1]
# create dataset




#################################################   train 1, V2 #########################################################

def trainphys1(modelNo,num_epochs,batch_size,learning_rate,loadCkpt,startline,stopline,testing=False,batchgroup=20,shuffleColumn=-1):




    if(modelNo==1):
        model1 = z_model.NeuralNetIndre().to(device)
        dummyVectorIn = [0,0,0,0]
        ColList=[2,3,6,8]
        LabelNo=11

    elif(modelNo==2):
        model1 = z_model.NeuralNetCart().to(device)
        dummyVectorIn = [0,0,0]
        ColList=[4,7,9]
        LabelNo=12
    else:
        model1 = z_model.NeuralNetYtre().to(device)
        dummyVectorIn = [0,0,0,0,0,0,0,0,0,0,0,0]
        ColList=[0,1,2,3,4,5,6,7,8,9,11,12]
        LabelNo=10
    
    dataset = Num1Dataset(startline,stopline,shuffleColumn,ColList,LabelNo)    
        
   # print(dataset.n_samples)
    # get first sample and unpack

    train_loader = DataLoader(dataset=dataset,
                            batch_size=batch_size,
                            shuffle=True,
                            num_workers=0)

    if (not testing):    #testing; utelukkende testing, ikke train + test
        datasetValidation = Num1ValDataset(startline,stopline,ColList,LabelNo)

            
        validation_loader = DataLoader(dataset=datasetValidation,
                                batch_size=int(batch_size),
                                shuffle=False,
                                num_workers=0)


    


    writer.add_graph(model1,torch.FloatTensor(dummyVectorIn).to(device))
    writer.flush()
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer1 = torch.optim.Adam(model1.parameters(), lr=learning_rate)  
    checkpoint1 = {
    "model_state": model1.state_dict(),
    "optim_state": optimizer1.state_dict()
    }

#        yes_or_no = input("yes or no; load chkpt?")
    if ((loadCkpt) or testing):
        checkpoint1 = torch.load(f"./chkp2/phys{modelNo}/chkpt1.pth")
        model1.load_state_dict(checkpoint1['model_state'])
        optimizer1.load_state_dict(checkpoint1['optim_state'])



    # Train the model
    n_total_steps = len(train_loader)

    print(f"step: {n_total_steps}")
    # if(testing):
    #     num_epochs = 1
    running_loss = 0.0
    LossLogg = []
    n_total_steps = len(train_loader)

    for epoch in range(num_epochs):
        print("epoch: ", epoch)
        numBatches = 0
        for i, (vectorIn1, labels) in enumerate(train_loader):  
            numBatches=i
            labels = labels.to(device)
            vectorIn1 = vectorIn1.to(device)
            
            # Forward pass
            outputs = model1(vectorIn1)
            loss = criterion(outputs, labels)            
            
            # Backward and optimize
            if(not testing):
                optimizer1.zero_grad()
                loss.backward()
                optimizer1.step()

            running_loss += loss.item()

            if i % batchgroup == (batchgroup-1) and not testing:    # 
                print('Batchy {}'.format(i + 1))
                running_vloss = 0.0
                model1.train(False)
                for j, (ValVectorIn1, ValLabels) in enumerate(validation_loader, 0):
                    # Forward pass
                    outputs = model1(ValVectorIn1.to(device))
                    VAlLoss = criterion(outputs, ValLabels.to(device))   
                    running_vloss += VAlLoss.item()
                model1.train(True)

                avg_loss = running_loss / batchgroup
                avg_vloss = running_vloss / len(validation_loader)
                # Log the running loss averaged per batch
                writer.add_scalars('Training vs. Validation Loss',
                                { 'Training' : avg_loss, 'Validation' : avg_vloss },
                                epoch * len(train_loader) + i)
                running_loss = 0.0
        if(testing):
            LossLogg.append(running_loss/numBatches)
            running_loss = 0.0
  

                



    writer.close()


    if(not testing):
        print(f'Finished Training')
    else:
        print(f'Finished Testing')
        return LossLogg

    # Save the model state dict
    state = {'model_state': model1.state_dict()}

    # Save the optimizer state dict
    state['optim_state'] = optimizer1.state_dict()

    # Save the state dict
    torch.save(state, f"./chkp2/phys{modelNo}/chkpt1.pth")
    return




#trainphys1(modelNo,num_epochs,batch_size,learning_rate,loadCkpt,startline,stopline,testing=False,batchgroup=20,shuffleColumn=-1):

#feature importance permutation
def featureImportancePermutation(modelNo,batch_size,startline,stopline):
    featureLoss=[]
    if modelNo==1:
        numFeatures=4
    elif modelNo==2:
        numFeatures=3
    elif modelNo==3:
        numFeatures=12



    for i in range(numFeatures+1):
        results=trainphys1(modelNo,1,batch_size,0.0001,True,startline,stopline,testing=True,shuffleColumn=i-1)
        featureLoss.append(sum(results)/len(results))

    
    return featureLoss

def printWeightsToCsv(modelNo):
    if(modelNo==1):
        model1 = z_model.NeuralNetIndre()
    if(modelNo==3):
        model1 = z_model.NeuralNetYtre()

    checkpoint1 = torch.load(f"./chkp2/phys{modelNo}/chkpt1.pth")
    model1.load_state_dict(checkpoint1['model_state'])

    with open(f"./LogDir/investigate/weights{modelNo}.csv", "w") as f:
        f.write("w1,w2,w3,w4,w5,\n" )

        # for name, param in model1.named_parameters():


#        for s in model1.parameters():
        for name, param in model1.named_parameters():
            f.write(str(name) + "\n" )
            f.write( "\n" )
            
            for i in param:
                try :
                    yy=i[0]
                    yy=True
                except:
                    yy=False
                if(yy):
                    for j in i.tolist():
                        f.write(str(j))
                        f.write(",")
                    f.write( "\n" )
                else:
                    f.write(str(i.tolist()))
                    f.write(",")
                    f.write( "\n" )

                #print()
                #f.write( "\n" )
            f.write("\n" )

