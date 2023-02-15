


import torch.nn as nn


# Fully connected neural network with one hidden layer
class NeuralNetYtre(nn.Module): #fysikk modell
    def __init__(self):
        super(NeuralNetYtre, self).__init__()

        self.l1 = nn.Linear(12, 32) 
        self.relu1 = nn.LeakyReLU()
        self.l2 = nn.Linear(32, 64)  
        self.relu2 = nn.LeakyReLU()
        self.l3 = nn.Linear(64, 128)  
        self.relu3 = nn.LeakyReLU()
        self.l4 = nn.Linear(128, 128)  
        self.relu4 = nn.LeakyReLU()
        self.l5 = nn.Linear(128, 64)  
        self.relu5 = nn.LeakyReLU()
        self.l6 = nn.Linear(64, 64)  
        self.relu6 = nn.LeakyReLU()
        self.l7 = nn.Linear(64, 64)  
        self.relu7 = nn.LeakyReLU()
        self.l8 = nn.Linear(64, 32)  
        self.relu8 = nn.LeakyReLU()
        self.l9 = nn.Linear(32, 32)  
        self.relu9 = nn.LeakyReLU()
        self.l10 = nn.Linear(32, 32)  
        self.relu10 = nn.LeakyReLU()

        self.l11 = nn.Linear(32, 32)  
        self.relu11 = nn.LeakyReLU()

        self.l12 = nn.Linear(32, 32)  
        self.relu12 = nn.LeakyReLU()

        self.l13 = nn.Linear(32, 32)  
        self.relu13 = nn.LeakyReLU()

        self.l14 = nn.Linear(32, 32)  
        self.relu14 = nn.LeakyReLU()

        self.l15 = nn.Linear(32, 32)  
        self.relu15 = nn.LeakyReLU()

        self.l16 = nn.Linear(32, 16)  
        self.relu16 = nn.LeakyReLU()

        self.l17 = nn.Linear(16, 8)  
        self.relu17 = nn.LeakyReLU()

        self.l18 = nn.Linear(8, 1)  
        self.relu18 = nn.LeakyReLU()



        nn.init.kaiming_normal_(self.l1.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l2.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l3.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l4.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l5.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l6.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l7.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l8.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l9.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l10.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l11.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l12.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l13.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l14.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l15.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l16.weight, mode='fan_out', nonlinearity='leaky_relu')        

        nn.init.kaiming_normal_(self.l17.weight, mode='fan_out', nonlinearity='leaky_relu')        
        nn.init.kaiming_normal_(self.l18.weight, mode='fan_out', nonlinearity='leaky_relu')        
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu1(out)
        out = self.l2(out)
        out = self.relu2(out)
        out = self.l3(out)
        out = self.relu3(out)
        out = self.l4(out)
        out = self.relu4(out)
        out = self.l5(out)
        out = self.relu5(out)
        out = self.l6(out)
        out = self.relu6(out)
        out = self.l7(out)
        out = self.relu7(out)
        out = self.l8(out)
        out = self.relu8(out)
        out = self.l9(out)
        out = self.relu9(out)
        out = self.l10(out)
        out = self.relu10(out)

        out = self.l11(out)
        out = self.relu11(out)
        out = self.l12(out)
        out = self.relu12(out)
        out = self.l13(out)
        out = self.relu13(out)
        out = self.l14(out)
        out = self.relu14(out)
        out = self.l15(out)
        out = self.relu15(out)
        
        out = self.l16(out)
        out = self.relu16(out)
        out = self.l17(out)
        out = self.relu17(out)
        out = self.l18(out)
        out = self.relu18(out)

        # no activation and no softmax at the end
        return out

# Fully connected neural network with one hidden layer
class NeuralNetIndre(nn.Module): #fysikk modell
    def __init__(self):
        super(NeuralNetIndre, self).__init__()

        self.l1 = nn.Linear(4, 16) 
        self.relu1 = nn.LeakyReLU()
        self.l2 = nn.Linear(16, 32)  
        self.relu2 = nn.LeakyReLU()
        self.l3 = nn.Linear(32, 128)  
        self.relu3 = nn.LeakyReLU()
        self.l4 = nn.Linear(128, 128)  
        self.relu4 = nn.LeakyReLU()
        self.l5 = nn.Linear(128, 64)  
        self.relu5 = nn.LeakyReLU()


        self.l6 = nn.Linear(64, 32)  
        self.relu6 = nn.LeakyReLU()

        self.l7 = nn.Linear(32, 32)  
        self.relu7 = nn.LeakyReLU()

        self.l8 = nn.Linear(32, 32)  
        self.relu8 = nn.LeakyReLU()

        self.l9 = nn.Linear(32, 32)  
        self.relu9 = nn.LeakyReLU()

        self.l10 = nn.Linear(32, 32)  
        self.relu10 = nn.LeakyReLU()

        self.l11 = nn.Linear(32, 32)  
        self.relu11 = nn.LeakyReLU()

        self.l12 = nn.Linear(32, 32)  
        self.relu12 = nn.LeakyReLU()

        self.l13 = nn.Linear(32, 16)  
        self.relu13 = nn.LeakyReLU()

        self.l14 = nn.Linear(16, 16)  
        self.relu14 = nn.LeakyReLU()

        self.l15 = nn.Linear(16, 1)  
        self.relu15 = nn.LeakyReLU()

        nn.init.kaiming_normal_(self.l1.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l2.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l3.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l4.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l5.weight, mode='fan_out', nonlinearity='leaky_relu')
     
        nn.init.kaiming_normal_(self.l6.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l7.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l8.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l9.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l10.weight, mode='fan_out', nonlinearity='leaky_relu')

        nn.init.kaiming_normal_(self.l11.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l12.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l13.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l14.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l15.weight, mode='fan_out', nonlinearity='leaky_relu')
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu1(out)
        out = self.l2(out)
        out = self.relu2(out)
        out = self.l3(out)
        out = self.relu3(out)
        out = self.l4(out)
        out = self.relu4(out)
        out = self.l5(out)
        out = self.relu5(out)
        

        out = self.l6(out)
        out = self.relu6(out)
        out = self.l7(out)
        out = self.relu7(out)
        out = self.l8(out)
        out = self.relu8(out)
        out = self.l9(out)
        out = self.relu9(out)
        out = self.l10(out)
        out = self.relu10(out)

        out = self.l11(out)
        out = self.relu11(out)
        out = self.l12(out)
        out = self.relu12(out)
        out = self.l13(out)
        out = self.relu13(out)
        out = self.l14(out)
        out = self.relu14(out)
        out = self.l15(out)
        out = self.relu15(out)

        # no activation and no softmax at the end
        return out

# Fully connected neural network with one hidden layer
class NeuralNetCart(nn.Module): #fysikk modell
    def __init__(self):
        super(NeuralNetCart, self).__init__()

        self.l1 = nn.Linear(3, 128) 
        self.relu1 = nn.LeakyReLU()
        self.l2 = nn.Linear(128, 128)  
        self.relu2 = nn.LeakyReLU()
        self.l3 = nn.Linear(128, 128)  
        self.relu3 = nn.LeakyReLU()
        self.l4 = nn.Linear(128, 64)  
        self.relu4 = nn.LeakyReLU()
        self.l5 = nn.Linear(64, 1)  
        self.relu5 = nn.LeakyReLU()

        self.relu66 = nn.ReLU6()
        nn.init.kaiming_normal_(self.l2.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l3.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l4.weight, mode='fan_out', nonlinearity='leaky_relu')
        nn.init.kaiming_normal_(self.l5.weight, mode='fan_out', nonlinearity='leaky_relu')

    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu1(out)
        out = self.l2(out)
        out = self.relu2(out)
        out = self.l3(out)
        out = self.relu3(out)
        out = self.l4(out)
        out = self.relu4(out)
        out = self.l5(out)
        out = self.relu5(out)
        



        # no activation and no softmax at the end
        return out
