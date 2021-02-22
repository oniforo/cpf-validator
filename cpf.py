from inspect import currentframe
from re import sub

class CPF:
    
    estados = [
        "RS", "DF, GO, MT, MS, TO", "AM, PA, RR, AP, AC, RO", "CE, MA, PI",
        "PB, PE, AL, RN", "BA, SE", "MG", "RJ, ES", "SP", "PR, SC"
    ]

    def __init__(self, cpf):
        
        cpf_num = sub(r"\D", "", str(cpf))
        cpf_incomplete = sub(r"\W|[a-zA-Z]", "", str(cpf))

        self.cpf = [int(x) for x in list(cpf_num)]
        self.length = len(cpf_num)
        self.state = None if self.length < 9 else cpf_num[8]
        self.cpf_incomplete = list(cpf_incomplete)
        self.formatted = self.formatted_cpf()
        try:
            #self.cpf_values = self.__cpf_possibilities()
            pass
        except:
            pass

    def __get_digit(self):
        
        lis = list(reversed(range(2, len(self.cpf) + 2)))
        arr = [a * b for a, b in zip(self.cpf, lis)]
        dig = sum(arr) % 11
        
        if (dig == 0 or dig == 1):
            self.cpf.append(0)
        else:
            self.cpf.append(11 - dig)

    def __prepare_for_validation(self):
        self.cpf.pop()
        self.cpf.pop()
        self.length = 9
        self.get_full_cpf()

    def formatted_cpf(self):
        if len(self.cpf) == 11:
            cpf = "".join(map(str, self.cpf))
            cpf = f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
            return cpf
        else:
            self.error = (
                "Length of CPF is not valid. "
                f"Expected 11, received {len(self.cpf)}"
            )
            return None
        
    def get_full_cpf(self):

        if self.length == 9:
            self.__get_digit()
            self.__get_digit()
        elif self.length == 10:
            self.__get_digit()
        else:
            print(
                f"{currentframe().f_code.co_name}: "
                "this method expects 9 or 10 numeric digits only. "
                f"Received {self.length}."
            )
            return
        
        return "".join(map(str, self.cpf))

    def get_state(self):
        try:
            estado = self.estados[int(self.state)]
        except:
            print(
                f"{currentframe().f_code.co_name}: "
                "unable to determine state. "
                f"String too short: {self.length} digits."    
            )
            return
        if self.state in ["0", "6", "8"]:
            print("Provided CPF belongs to the state:", estado)
        else:
            print("Provided CPF belongs to one of these states:", estado)
        return estado

    def validate_cpf(self):
        if self.length == 11:
            cpf_pre = self.cpf.copy()
            self.__prepare_for_validation()
            cpf_post = self.cpf.copy()
            if sum(cpf_pre) in [
                10, 11, 12, 21, 22, 23, 32, 33, 34, 43, 44, 45, 
                54, 55, 56, 65, 66, 67, 76, 77, 78, 87, 88
            ] and cpf_pre == cpf_post:
                print(f"Valid CPF number: {''.join(map(str, cpf_pre))}")
                return True
            else:
                print(f"Invalid CPF number: {''.join(map(str, cpf_pre))}")
                return False
        else:
            print(
                f"{currentframe().f_code.co_name}: "    
                "Invalid CPF length. Unable to validate."
            )

    def __cpf_possibilities(self, **kwargs):

        def digit(array):
            lis = list(reversed(range(2, len(array) + 2)))
            arr = [a * b for a, b in zip(array, lis)]
            dig = sum(arr) % 11
            if (dig == 0 or dig == 1):
                return 0
            else:
                return 11 - dig

        # Find as a substring of an array element of estados array
        # kwargs: state, output file, type (numeric or formatted)
        state = kwargs.get("state")
        #print(state) if state else print("no state input")

        if len(self.cpf_incomplete) == 11:
            
            cpf = self.cpf_incomplete.copy()
            main = cpf[:9]
            digs = cpf[-2:]
            digit_logic = [0 if i == "_" else 1 for i in digs]            

            i = 0
            for pos, elem in enumerate(main):
                if elem == "_":
                    # Use the pos element to facilitate iteration afterwards
                    # print(pos)
                    main[pos] = chr(97 + i)
                    i += 1

            rng = list(range(10 ** i))
            rng = [f"{x:0{i}d}" for x in rng]
            #print("range", rng)

            matches = []
            for elem in rng:
                main_copy = main.copy()
                #print(main_copy)
                #print(elem)
                # Facilitate iteration
                for x in range(len(elem)):
                    main_copy[main_copy.index(chr(97 + x))] = elem[x]

                main_copy = [int(x) for x in main_copy]

                first_dig = digit(main_copy)
                main_copy.append(first_dig)
                second_dig = digit(main_copy)

                if digit_logic == [1, 0]:
                    if first_dig == int(digs[0]):
                        main_copy.append(second_dig)
                        match = "".join(map(str, main_copy))
                        matches.append(match)                        
                    #else:
                        #print(f"The first digit did not match: {first_dig}")

                elif digit_logic == [0, 1]:
                    if second_dig == int(digs[1]):
                        main_copy.append(second_dig)
                        match = "".join(map(str, main_copy))
                        matches.append(match)
                    #else:
                        #print(f"The second digit did not match: {second_dig}")

                elif digit_logic == [1, 1]:
                    if first_dig == int(digs[0]) and second_dig == int(digs[1]):
                        main_copy.append(second_dig)
                        match = "".join(map(str, main_copy))
                        matches.append(match)
                    #else:
                        #print("Both digits did not match.")
                
                elif digit_logic == [0, 0]:
                    main_copy.append(second_dig)
                    match = "".join(map(str, main_copy))
                    matches.append(match)                    

        else:
            print(
                f"{currentframe().f_code.co_name}: "
                "Incompatible number of digits: "
                f"{len(self.cpf_incomplete)} (11 expected)."
            )

        return matches