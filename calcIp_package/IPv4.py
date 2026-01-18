from calcIp_package.colors.color import Colors


class IPv4:
    BYTE = 4
    bit = 32

    def __init__(self, ip):
        """
        Metodo costruttore della classe IPv4.
                :parameter ip (str): Indirizzi IPv4 concatenato alla sua subent mask in notazione CIDR.

        """
        self.__ip = {
            'bin': [],
            'dec': ip
        }

        self.__network_address = {
            'bin': [],
            'dec': []
        }

        self.__broadcast_address = {
            'bin': [],
            'dec': []
        }

        self.__subnet_mask = {
            'bin': [],
            'dec': [],
            'cidr': 0
        }

        self.__wild_card = {
            'bin': [],
            'dec': 0
        }
        self.__subnets = {

        }

        self.__supernets = {

        }
        self.__max_host = 0
        self.__class = None
        ##############
        self.__point_position = [8, 17, 26]
        self.__stateIpv4 = True

        self.__divided_ip_subnet_mask()
        self.__control_state_ipv4()
        self.ipv4_to_bin()
        self.subnet_mask_to_bin()
        self.subnet_mask_to_dec()
        self.wild_card_to_bin()
        self.wild_card_to_dec()
        self.network_address_to_dec()
        self.network_address_to_bin()
        self.broadcast_address_to_bin()
        self.broadcast_address_to_dec()

        self.which_class()

    def to_string(self):
        if self.__stateIpv4:
            print("&&&&&&&&&&&INDIRIZZI DECIMALI&&&&&&&&&&&")
            print(f"Stato IPv4: {self.__stateIpv4}")
            self.__print_decimal_ipv4(self.__ip['dec'], "IP: ")
            print(f"Subnet mask in notazione CIDR:\t/{self.__subnet_mask['cidr']}")
            self.__print_decimal_ipv4(self.__subnet_mask['dec'], "Subnet mask: ")
            self.__print_decimal_ipv4(self.__wild_card['dec'], "Wild card: ")
            self.__print_decimal_ipv4(self.__network_address['dec'], "Indirizzi di rete: ")
            self.__print_decimal_ipv4(self.__broadcast_address['dec'], "Indirizzi di broadcast: ")
            print(f"Host massimi: {self.__max_host}")
            print(f"Classe di indirizzo: {self.__class}")
            print("&&&&&&&&&&&INDIRIZZI BINARI&&&&&&&&&&&")
            self.__print_binary_ipv4(self.__ip['bin'], "IP: ")
            self.__print_binary_ipv4(self.__subnet_mask['bin'], "Subnet mask: ")
            self.__print_binary_ipv4(self.__wild_card['bin'], "Wild card: ")
            self.__print_binary_ipv4(self.__network_address['bin'], "Indirizzo di rete: ")
            self.__print_binary_ipv4(self.__broadcast_address['bin'], "Indirizzi di broacast: ")
            if len(self.__subnets.keys()) > 0:     # se sono stati effettuati subnet.
                for i in self.__subnets.keys():
                    for j in range(len(self.__subnets[i])):
                        print("\n\n")
                        print(f"\t\tSUBNETTING {j+1} from {i}\t\t")
                        self.__subnets[i][j].to_string()
            if len(self.__supernets.keys()) > 0:
                print(Colors.BLUE + "\n\n///////////////////////////////////////////////////////////////" + Colors.RESET)
                for i in self.__supernets.keys():
                    print("\n\n")
                    print(f"\t\tSUPERNETTING from {i}\t\t")
                    self.__supernets[i].to_string()
        else:
            print("INPUT NON VALIDO, CODE ERROR: 100")


    def __control_state_ipv4(self):
        try:
            byte = 0 <= int(self.__ip['dec'][0]) <= 255
            for i in range(1, IPv4.BYTE+1):
                byte = byte and 0 <= int(self.__ip['dec'][i-1]) <= 255
            if byte and 0 < self.__subnet_mask['cidr'] <= 32:
                self.__stateIpv4 = True
            else:
                self.__stateIpv4 = False
        except:
            self.__stateIpv4 = False


    def __divided_ip_subnet_mask(self):
        """

        :return:
        """
        try:
            for i in range(len(self.__ip['dec'])):
                if self.__ip['dec'][i] == '/':
                    self.__subnet_mask['cidr'] = int(self.__ip['dec'][
                                                     i + 1:])  # estraggo la subnet mask in notazione CIDR, sommo 1 all'indice così parto dalla prima cifra della subnet mask fino alla fine di essa.
                    self.__ip['dec'] = self.__ip['dec'][
                                       :i]  # estraggo tutto quello che c'è prima dello / quindi solamente l'ip.
                    self.__ip['dec'] = self.__ip['dec'].split('.')
                    break
            self.__max_host = (2 ** (IPv4.bit - self.__subnet_mask['cidr'])) - 2  # trovo gli host massimi di quella rete, non considerando il network e broadcast address.
        except:
            self.__stateIpv4 = False


    def __convert_dec_byte_to_bin(self, address, bit=8):
        """
        Ritorna bit dopo bit del byte convertito in binario, in questo metodo viene utilizzato un generatore.
            :param address (str): Singolo Byte dell'indirizzo IPv4
            :param bit (int): Indica il numero di bit della word, default 8.
            :return i (int): Singolo bit del byte
        """
        sequence = [0 for i in range(bit)]  # preparo la word di n bit.
        i = 0
        while address != 0:
            sequence[i] = address % 2
            address //= 2
            i += 1
        sequence = sequence[::-1]
        for i in sequence:
            yield i  # uso il generatore per evitare di avere l'address come una lista di liste.

    def __convert_address_to_bin(self, address):
        """
        Converte un indirizzo da decimale a binario.
            :param address (list[str]): Indirizzo decimale
            :return binary_ip (list):  Indirizzo convertito in binario nella seguente forma [00000000, '.', 000000000, '.', 00000000, '.', 000000000]
        """
        binary_ip = []
        for i in range(IPv4.BYTE):
            for j in self.__convert_dec_byte_to_bin(int(address[i])):
                binary_ip.append(j)
            if i != IPv4.BYTE - 1:
                binary_ip.append('.')
        return binary_ip

    def __convert_address_to_dec(self, address):
        """
        Converte un indirizzo da binario a decimale, sfrutta due indici start e end per poter estarre da address il byte in binario.
        Il funzionamento di basa sulla posizione dei punti nell'indirizzo binario, in questa maniera estraggo il byte in binario senza aver i '.'.
        Subito dopo l'estrazione effettuo un reverse del byte in binario cos' da passare subito alla conversione del singolo byte per poi modificare gli indici.
            :param address (list):
            :return decimal_address (list[str]): Ritorna l'indirizzo convertito in decimale.
        """
        start = 0
        end = 0
        decimal_number = 0
        decimal_address = []
        for i in range(IPv4.BYTE):
            if i == IPv4.BYTE - 1:  # l'ultimo byte non prevede un . alla fine, perciò se sono arrivato all'ultima iterazione devo estrarlo diversamente l'ultimo byte
                byte = address[end + 1:][::-1]
            else:
                end = self.__point_position[i]
                byte = address[start: end][::-1]  # faccio il reverse del i-esimo byte
            for j in range(len(byte)):
                decimal_number += (2 ** j) * byte[j]
            decimal_address.append(str(decimal_number))
            decimal_number = 0
            start = end + 1
        return decimal_address

    def __format_binary_address(self, address):
        """
        Metodo che formatta un indirizzo ipv4 binario. Aggiunge i punti ogni byte.
        :param address:
        :return:
        """
        for i in self.__point_position:
            address.insert(i, '.')
        return address

    def __make_subnetting(self, new_subnet_mask_cidr):
        """
        Il metodo prende come parametro la nuova subnet mask che dovrà avere l'indirizzo ipv4 dell'istanza corrente.
        L'idea è quella di estrarre i futuri bit delle subnet, a partire dal network address, una volta estratti vengono sovrascritti
        con la combinazione i-esima. Esempio: se ho 192.168.1.0/24 e voglio /26
        192.168.1.(00)000000
        Io avrò 2^2 possibili reti, l'indirizzo di rete di ogni subnet è dato dalla sostituzioni di quei (00), con una volta 00 poi 01 10 11.
        :param new_subnet_mask_cidr:
        :return:
        """
        number_subnet_bit = new_subnet_mask_cidr - self.__subnet_mask['cidr']   # ottengo i bit dedicati alle subnet
        subnet_bit = [[] for i in range(2**number_subnet_bit)]      # elevando a 2 il numero di bit, ottengo il numero di reti.
        subnet = []
        for i in range(2**number_subnet_bit):
            for j in self.__convert_dec_byte_to_bin(i, number_subnet_bit):
                subnet_bit[i].append(j)
            binary_ip = [i for i in self.__network_address['bin'] if i != '.']      # rimuovo i punti dall'indirizzo, così evito di aggiungere offset.
            start = self.__subnet_mask['cidr']      # dato che si parte da 0, non ho bisogno di sommare 1 a questo numero, in quanto mi trovo già nei bit degli host
            end = start + number_subnet_bit
            binary_ip[start : end] = subnet_bit[i]
            binary_ip = self.__format_binary_address(binary_ip)
            ip = self.__convert_address_to_dec(binary_ip)
            ip = IPv4(".".join(ip) + f"/{new_subnet_mask_cidr}")
            subnet.append(ip)
        return subnet

    def __print_binary_ipv4(self, address, message):
        address = [i for i in address if i != '.']
        print(message, end='')
        for i in range(IPv4.bit):
            if i % 8 == 0 and i != 0:
                print('.', end='')
            if i < self.__subnet_mask['cidr']:
                print(Colors.GREEN + str(address[i]), end='')
            else:
                print(Colors.RED + str(address[i]), end='')
        print(Colors.RESET)

    def __print_decimal_ipv4(self, address, message):
        """
        Metodo che manda a video un ipv4 in binario.
        :param address:
        :param message:
        :return:
        """
        address = '.'.join(address)
        print(f"{message} {address}")

    def subnetting(self, subnet_mask):
        if self.__stateIpv4 and subnet_mask > self.__subnet_mask['cidr']:       # se la seconda condizione è falsa non si tratta di subnetting.
            subnets = self.__make_subnetting(subnet_mask)
            self.__subnets[f"/{subnet_mask}"] = subnets
            # return self.__subnets[f"/{subnet_mask}"]
        else:
            print(f"NO VALID SUBNET MASK: {subnet_mask}")

    def supernetting(self, subnet_mask):
        if self.__stateIpv4 and subnet_mask < self.__subnet_mask['cidr']:       # se la seconda condizione è falsa non si tratta di supernetting.
            ip = '.'.join(self.__ip['dec'])
            subnet_mask = f"/{subnet_mask}"
            ip = ip+subnet_mask
            # print("DEBUG: " + ip)
            self.__supernets[subnet_mask] = IPv4(ip)
        else:
            print(f"NO VALID SUBNET MASK: {subnet_mask}")


    def ipv4_to_bin(self):
        """
        Metodo che converte l'ipv4 da decimale a binario.
            :return ip (list): Indirizzo ipv4 in binario
        """
        if self.__stateIpv4:
            self.__ip['bin'] = self.__convert_address_to_bin(self.__ip['dec'])
            # return self.__ip['bin']
        else:
            self.__ip['bin'] = None

    def network_address_to_bin(self):
        """
        Metodo che converte l'indirizzo di rete da decimale a binario.
            :return network_address (list):  Indirizzo di rete binario
        """
        if self.__stateIpv4:
            # self.network_address_to_dec()
            self.__network_address['bin'] = self.__convert_address_to_bin(self.__network_address['dec'])
            # return self.__network_address['bin']
        else:
            self.__network_address['bin'] = None

    def network_address_to_dec(self):
        """
        Metodo che calcola l'indirizzo di rete a cui appartiene l'indirizzo dato al costruttore. Per farlo sfrutto l'operazione and bit a bit tra ogni singolo byte dell'indirizzo e della subnet mask,
        per, infine, convertirlo in stringa.
            :return network_address (list[str]): Indirizzo di rete.
        """
        if self.__stateIpv4:
            # self.subnet_mask_to_dec()
            for i in range(IPv4.BYTE):
                self.__network_address['dec'].append(str( int(self.__ip['dec'][i]) & int(self.__subnet_mask['dec'][i]) ))     # operazione and bit a bit tra ogni byte dell'indirizzo e della subnet mask
            # return self.__network_address['dec']
        else:
            self.__network_address['dec'] = None

    def broadcast_address_to_bin(self):
        """
        Metodo che trova l'indirizzo di broadcast. L'indirizzo di broadcast si trova impostando tutti i bit dell'host a 1.
        Quindi scorro l'indirizzo di rete e finchè sono nei bit di rete li copio nel broadcast address, appena sono nei bit dell'host,
        aggiungo 1 nel boradcast address.
            :return broadcast_address (list): Indirizzo di broadcast
        """
        if self.__stateIpv4:
            # self.network_address_to_bin()
            net_address = [i for i in self.__network_address['bin'] if i != '.']
            for i in range(IPv4.bit):
                if i % 8 == 0 and i != 0:
                    self.__broadcast_address['bin'].append('.')
                if i < self.__subnet_mask['cidr']:
                    self.__broadcast_address['bin'].append(net_address[i])
                else:
                    self.__broadcast_address['bin'].append(1)
            return self.__broadcast_address['bin']
        else:
            self.__network_address['dec'] = None

    def broadcast_address_to_dec(self):
        """
        Metodo che converte l'indirizzo di broadcast da binario a decimale.
            :return broadcast_address (list[str]): Indirizzo di broadcast decimale
        """
        if self.__stateIpv4:
            # self.broadcast_address_to_bin()
            self.__broadcast_address['dec'] = self.__convert_address_to_dec(self.__broadcast_address['bin'])
            return self.__broadcast_address['dec']
        else:
            self.__broadcast_address['dec'] = None

    def subnet_mask_to_bin(self):
        """
        Metodo che converte la subnet mask da CIDR.
            :return subnet_mask_bin (list): Indirizzo binario della subnet mask.
        """
        if self.__stateIpv4:
            subnet_mask_bin = []
            for i in range(IPv4.bit):
                if i % 8 == 0 and i != 0:  # esclusa la prima occorrenza del contatore i.
                    subnet_mask_bin.append('.')
                if i < self.__subnet_mask['cidr']:
                    subnet_mask_bin.append(1)
                else:
                    subnet_mask_bin.append(0)
            self.__subnet_mask['bin'] = subnet_mask_bin
            # return subnet_mask_bin
        else:
            self.__subnet_mask['bin'] = None

    def subnet_mask_to_dec(self):
        """
        Metodo che converte la subnet mask da binario a decimale.
            :return subnet_mask_dec (list[str]): Indirizzo decimale della subnet mask.
        """
        if self.__stateIpv4:
            # self.subnet_mask_to_bin()
            self.__subnet_mask['dec'] = self.__convert_address_to_dec(self.__subnet_mask['bin'])
            # return self.__subnet_mask['dec']
        else:
            self.__subnet_mask['dec'] = None

    def wild_card_to_bin(self):
        """
        Metodo che calcola la wild card in binario.

            :return wild_card_bin (list): Indirizzi wild card in binario
        """
        if self.__stateIpv4:
            # self.subnet_mask_to_bin()
            result = []
            for i in range(len(self.__subnet_mask['bin'])):
                bit = self.__subnet_mask['bin'][i]
                if bit != '.':
                    result.append(int(not bit))
                else:
                    result.append(bit)
            self.__wild_card['bin'] = result
            return self.__wild_card['bin']
        else:
            self.__wild_card['bin'] = None

    def wild_card_to_dec(self):
        """
        Metodo che converte la wild card da binario a decimale.
            :return wild_card_dec (list[str]): Indirizzo decimale della wild card.
        """
        if self.__stateIpv4:
            # self.wild_card_to_bin()
            self.__wild_card['dec'] = self.__convert_address_to_dec(self.__wild_card['bin'])
            return self.__wild_card['dec']
        else:
            self.__wild_card['dec'] = None

    def which_class(self):
        """
        Metodo che indivua, se possibile, la classe di quell'indirizzo.
            :return class (str): Classe dell'indirizzo.
        """
        if self.__stateIpv4:
            if 0 <= int(self.__ip['dec'][0]) <= 127 and self.__subnet_mask['cidr'] == 8:
                self.__class = 'A'
            elif 128 <= int(self.__ip['dec'][0]) <= 191 and self.__subnet_mask['cidr'] == 16:
                self.__class = 'B'
            elif 192 <= int(self.__ip['dec'][0]) <= 223 and self.__subnet_mask['cidr'] == 24:
                self.__class = 'C'
            else:
                self.__class = None
            return self.__class
        return None

