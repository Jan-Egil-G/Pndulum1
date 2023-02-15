import math
def popFirst(container):
    if(len(container)>0):
        return True, container.pop(0)
    else:
        return False, [0,0,0]


def PushLast(array,container):
    OFerror=False
    NoItems=len(container)
    if(NoItems>5):
        OFerror=True
        container.pop(NoItems-1)
        NoItems-=1
    container.append(array)
    return(OFerror)

