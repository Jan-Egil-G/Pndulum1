
import torch
import torch.nn as nn

# from torch.utils.tensorboard import SummaryWriter
# writer=SummaryWriter("runs/mnist")




class NeuralNetCtrl(nn.Module): #control modell
    def __init__(self):
        super(NeuralNetCtrl, self).__init__()


        self.l1 = nn.Linear(5, 128) 
#        torch.nn.init.normal_(self.l1.weight)
        self.relu1 = nn.LeakyReLU()
        self.l2 = nn.Linear(256, 128)  
#        torch.nn.init.normal_(self.l2.weight)
        self.relu2 = nn.LeakyReLU()
        self.l3 = nn.Linear(128, 128)  
#        torch.nn.init.normal_(self.l3.weight)
        self.relu3 = nn.LeakyReLU()
        self.l4 = nn.Linear(128, 64)  
#        torch.nn.init.normal_(self.l4.weight)
        self.relu4 = nn.LeakyReLU()
        self.l5 = nn.Linear(64, 32)  
#        torch.nn.init.normal_(self.l5.weight)
        self.relu5 = nn.LeakyReLU()
        self.l6 = nn.Linear(32, 16)  
#        torch.nn.init.normal_(self.l6.weight)
        self.relu6 = nn.LeakyReLU()
        self.l7 = nn.Linear(16, 2)  
#        torch.nn.init.normal_(self.l6.weight)

        nn.init.kaiming_normal_(self.l1.weight, mode='fan_out', nonlinearity='leaky_relu')
      #  nn.init.normal_(self.l1.bias)
        
        nn.init.kaiming_normal_(self.l2.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l3.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l4.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l5.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l6.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l7.weight, mode='fan_out', nonlinearity='leaky_relu')


        self.relu66 = nn.ReLU6()



    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu1(out)
        # out = self.l2(out)
        # out = self.relu2(out)
        out = self.l3(out)
        out = self.relu3(out)
        out = self.l4(out)
        out = self.relu4(out)
        out = self.l5(out)
        out = self.relu5(out)
        out = self.l6(out)
        out = self.relu6(out)
        out = self.l7(out)
        out = self.relu66(out)
        out=out*0.16667


        return out

#    def load(self):


        



