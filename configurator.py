from PosPressureCore import Block

def getCfg(block):

    lc = block.lightConfig
    fd = block.flowDir
    fg = block.flowGas

    if (lc==0) and (fd==1) and (fg==1):
        returnVal = '1'
    if (lc==0) and (fd==2) and (fg==1):
        returnVal = '2'
    if (lc==0) and (fd==1) and (fg==2):
        returnVal = '3'
    if (lc==0) and (fd==2) and (fg==2):
        returnVal = '4'
    if (lc==0) and (fg==0):
        returnVal = '5'

    if (lc==1) and (fd==1) and (fg==1):
        returnVal = '6'
    if (lc==1) and (fd==2) and (fg==1):
        returnVal = '7'
    if (lc==1) and (fd==1) and (fg==2):
        returnVal = '8'
    if (lc==1) and (fd==2) and (fg==2):
        returnVal = '9'
    if (lc==1) and (fg==0):
        returnVal = 'a'

    if (lc==2) and (fd==1) and (fg==1):
        returnVal = 'b'
    if (lc==2) and (fd==2) and (fg==1):
        returnVal = 'c'
    if (lc==2) and (fd==1) and (fg==2):
        returnVal = 'd'
    if (lc==2) and (fd==2) and (fg==2):
        returnVal = 'e'
    if (lc==2) and (fg==0):
        returnVal = 'f'

    if (lc==3) and (fd==1) and (fg==1):
        returnVal = 'g'
    if (lc==3) and (fd==2) and (fg==1):
        returnVal = 'h'
    if (lc==3) and (fd==1) and (fg==2):
        returnVal = 'i'
    if (lc==3) and (fd==2) and (fg==2):
        returnVal = 'j'
    if (lc==3) and (fg==0):
        returnVal = 'k'

    if (lc==4) and (fd==1) and (fg==1):
        returnVal = 'l'
    if (lc==4) and (fd==2) and (fg==1):
        returnVal = 'm'
    if (lc==4) and (fd==1) and (fg==2):
        returnVal = 'n'
    if (lc==4) and (fd==2) and (fg==2):
        returnVal = 'o'
    if (lc==4) and (fg==0):
        returnVal = 'p'

    return returnVal

if __name__=="__main__":
    pass
