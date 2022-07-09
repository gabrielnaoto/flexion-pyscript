import math

# Função de validação dos inputs serem números e transformação deles em float        
def ask_numeric_value(text):
    value = ""
    while type(value) != float:
        try:
            value = float(input(text))
        except:
            value = ""
    return value

maj_carga = 1.4 
min_conc = 1.4
min_aço = 1.15

def get_d(h,dl):
    d = h - dl
    return d

def get_fcd(fck):
    fcd = fck / (10 * min_conc)
    return fcd

def get_fyd(fyk):
    fyd = fyk / min_aço
    return fyd

def get_lam_alf(fck):
    if fck <= 50:
        lambd = 0.8
        alfac = 0.85
    else:
        lambd = 0.8 - ((fck - 50) / 400)
        alfac = 0.85 * (1 - ((fck - 50) / 200))
    return lambd, alfac

def get_delta(h,bw,dl,md,fck):
    d = get_d(h,dl)
    fcd = get_fcd(fck)
    lambd, alfac = get_lam_alf(fck)
    a = 0.5 * (math.pow(lambd, 2)) * alfac * fcd * bw
    b = - lambd * d * alfac * fcd * bw
    c = md
    delta = math.pow(b, 2) - (4 * a * c)
    return a, b, delta

def get_raiz(h,bw,dl,md,fck):
    a, b, delta = get_delta(h,bw,dl,md,fck)
    if delta < 0:
        texto = 'Raízes imaginárias, verifique os valores'
        return texto

    if delta == 0:
        raiz = - b / (2 * a)
        texto = 'O valor da LN é (cm): ', raiz
        return texto, raiz

    raiz1 = (- b + math.sqrt(delta)) / (2 * a)
    raiz2 = (- b - math.sqrt(delta)) / (2 * a)
    
    ln_valid = False

    for raiz in [raiz1, raiz2]:
        in_range = raiz >= 0 and raiz <= h
        if in_range:
            #print_root(r)
            texto = 'O valor da LN é (cm): '
            ln_valid = True
            break 

    if ln_valid:
        return texto, raiz

def get_ecu(fck):
    if fck <= 50:
        ecu = 0.0035
    else:
        ecu = 0.0026 + (0.035*(((90 - fck) /100) **4))
    return ecu

def get_eyd(fyd):
    eyd = fyd * 10 / 210000
    return eyd

def get_x2lim(h,dl,fck):
    d = get_d(h,dl)
    ecu = get_ecu(fck)
    x2lim = (ecu * d) / (0.01 + ecu)
    return x2lim

def get_x3lim(h,dl,fck,fyd):
    d = get_d(h,dl)
    ecu = get_ecu(fck)
    eyd = get_eyd(fyd)
    x3lim = (ecu * d) / (eyd + ecu)
    return x3lim

def get_xlim(h,dl,fck):
    d = get_d(h,dl)
    lim_range = fck >= 20 and fck <= 50
    if lim_range:
        xlim = 0.45*d
    else:
        xlim = 0.35*d
    return xlim

def get_dominio(h,bw,dl,md,fck,fyd):
    tx, ln = get_raiz(h,bw,dl,md,fck)
    x2lim = get_x2lim(h,dl,fck)
    x3lim = get_x3lim(h,dl,fck,fyd)
    xlim = get_xlim(h,dl,fck)
    dominio_2 = ln <= x2lim
    dominio_3 = ln >= x2lim and ln <= xlim and ln <= x3lim
    arm_dupla = ln > xlim
    print(x2lim, x3lim)

    if dominio_2:
        texto = 'Domínio 2'
        return texto
    
    if dominio_3:
        texto = 'Domínio 3'
        return texto

    if arm_dupla:
        texto = 'Armadura Dupla'
        return texto

def area_aço(h,bw,dl,fck,fyk,md):
    d = get_d(h,dl)
    fyd = get_fyd(fyk)
    lambd, alfac = get_lam_alf(fck)
    texto, ln = get_raiz(h,bw,dl,md,fck)
    z = d - (0.5 * lambd * ln)
    asi = md / (fyd * z)
    texto = 'A área de aço é (cm²): '
    return texto, z, asi

def arm_dupla(h,bw,dl,fck,fyk,md):
    d = get_d(h,dl)
    fcd = get_fcd(fck)
    fyd = get_fyd(fyk)
    lambd, alfac = get_lam_alf(fck)
    xlim = get_xlim(h,dl,fck)
    ln = xlim
    ecu = get_ecu(fck)
    eyd = get_eyd(fyd)

    m1d = ((lambd*xlim*d)-(0.5*(lambd**2)*(xlim**2)))*alfac*fcd*bw
    m2d = md - m1d

    z = d - (0.5 * lambd * xlim)
    as1 = m1d/(fyd*z)
    as2 = m2d/(fyd*(d-dl))
    ast = as1+as2

    esc = (ecu*(xlim-dl))/xlim
    if esc >= eyd:
        fs = fyd
    else:
        fs = (fyd*esc)/eyd

    asc = m2d/(fs*(d-dl))
    return ast, asc

