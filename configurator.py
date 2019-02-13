from PosPressure import Block

def getCfg(block):

    lc = block.lightCfg
    fd = block.flowDir
    fg = block.flowGas

    if (lc==0) and (fd==1) and (fg==1):
        return '1'
    if (lc==0) and (fd==2) and (fg==1):
        return '2'
    if (lc==0) and (fd==1) and (fg==2):
        return '3'
    if (lc==0) and (fd==2) and (fg==2):
        return '4'
    if (lc==0) and (fg==0):
        return '5'

    if (lc==1) and (fd==1) and (fg==1):
        return '6'
    if (lc==1) and (fd==2) and (fg==1):
        return '7'
    if (lc==1) and (fd==1) and (fg==2):
        return '8'
    if (lc==1) and (fd==2) and (fg==2):
        return '9'
    if (lc==1) and (fg==0):
        return 'a'

    if (lc==2) and (fd==1) and (fg==1):
        return 'b'
    if (lc==2) and (fd==2) and (fg==1):
        return 'c'
    if (lc==2) and (fd==1) and (fg==2):
        return 'd'
    if (lc==2) and (fd==2) and (fg==2):
        return 'e'
    if (lc==2) and (fg==0):
        return 'f'

    if (lc==3) and (fd==1) and (fg==1):
        return 'g'
    if (lc==3) and (fd==2) and (fg==1):
        return 'h'
    if (lc==3) and (fd==1) and (fg==2):
        return 'i'
    if (lc==3) and (fd==2) and (fg==2):
        return 'j'
    if (lc==3) and (fg==0):
        return 'k'

    if (lc==4) and (fd==1) and (fg==1):
        return 'l'
    if (lc==4) and (fd==2) and (fg==1):
        return 'm'
    if (lc==4) and (fd==1) and (fg==2):
        return 'n'
    if (lc==4) and (fd==2) and (fg==2):
        return 'o'
    if (lc==4) and (fg==0):
        return 'p'
