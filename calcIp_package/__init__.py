from calcIp_package.convertitor.convertitor import dec_to_bin, bin_to_dec
from calcIp_package.colors.color import Colors

# funzione che trasforma l'ip_address_dec in binario bit per bit:
def binary_ipv4(ip, lenght_ip=4):
    ip_result = []
    for i in range(lenght_ip):
        generator = dec_to_bin(int(ip[i]))
        for k in generator:
            ip_result.append(k)
    return ip_result


# funzione che trasforma la subnetmask da binaria a decimale:
def decimal_ipv4(subnet_mask, lenght_ip=4):
    subnet = []
    start = 0
    for i in range(lenght_ip):
        subnet.append(str(bin_to_dec(subnet_mask[start: start+8])))
        start += 8      # mi sposto di 8 perchè sto estrando byte
    return subnet

# funzione che calcola la wild card binaria data la subnet mask binaria
def wild_card_calculation(subnet_mask_bin):
    wild_card = []
    for i in subnet_mask_bin:
        if i == '1':
            wild_card.append('0')
        else:
            wild_card.append('1')
    return wild_card

# funzione che determina la classe di indirizzo di quell'ipv4
def which_class(ip, subnet_mask_cidr):
    first_byte = int(ip[0])
    if 0 <= first_byte <= 127 and subnet_mask_cidr == 8:    # impongo una doppia condizione perchè grazie a CIDR e VSLM posso avere un ip con il primo byte pari a 192, ma posso dedicare meno o più bit alla rete rispetto ad un classe C.
        return 'A'
    elif 128 <= first_byte <= 191 and subnet_mask_cidr == 16:
        return 'B'
    elif 192 <= first_byte <= 223 and subnet_mask_cidr == 24:
        return 'C'
    return None


# funzione che manda a video un indirizzo ip binario con la suddivisione dei bit dedicati alla rete e all'host
def print_ip_bin(ip_bin, message, lenght_byte_ip=32, subnet_mask_cidr=0):
    i = 0
    print(f"{message}: ", end='')
    for j in range(lenght_byte_ip):
        if j % 8 == 0 and j != 0:
            print('.', end='')
        if i < subnet_mask_cidr:
            print(Colors.GREEN + str(ip_bin[i]), end='')      # i bit dedicati alla rete li mando a video in verde
            i += 1
        else:
            print(Colors.RED + str(ip_bin[j]), end='')     # i bit dedicati agli host li mando a video in rosso
    print(Colors.RESET)
