import serial

LED_ON = 0xf7c03f

FERN_ON = 0xE0E040BF
FERN_PLAY = 0xE0E0E21D
FERN_0 = 0xE0E08877
FERN_1 = 0xE0E020DF
FERN_2 = 0xE0E0A05F
FERN_3 = 0xE0E0609F
FERN_4 = 0xE0E010EF
FERN_5 = 0xE0E0906F
FERN_6 = 0xE0E050AF
FERN_7 = 0xE0E030CF
FERN_8 = 0xE0E0B04F
FERN_9 = 0xE0E0708F

FERN_NUMBERS = [FERN_0, FERN_1, FERN_2, FERN_3, FERN_4, FERN_5, FERN_6, FERN_7, FERN_8, FERN_9]


class CodeChecker:
    def __init__(self, code):
        self.code = code
        self.last_number = None
        self.checked = [False for i in range(0, len(self.code))]
        self.at_index = 0

    def next_number(self, number):
        if number == self.last_number:
            return

        self.last_number = number

        if self.code[self.at_index] == number:
            self.checked[self.at_index] = True
            self.at_index += 1
        else:
            self.at_index = False
            for i in range(0, len(self.checked)):
                self.checked[i] = False

        done = True
        for elem in self.checked:
            if not elem:
                done = False

        if done:  # start over again
            self.last_number = None
            self.checked = [False for i in range(0, len(self.code))]
            self.at_index = 0

        return done


def parse_fern_nums(content):
    for i in range(0, len(FERN_NUMBERS)):
        if FERN_NUMBERS[i] == content:
            return i


# rot, gelb, grün, blau
# 8325 Papier halb bedruckt
# 5373 Foto drucken
# 9251 Fenster

def main():
    reader = serial.Serial('/dev/ttyACM0', 9600)

    simple_code = CodeChecker("9251")
    last_fern_parsed = None

    while reader.isOpen():
        content = reader.readline().decode().replace("\r\n", "")
        #print("Read -> " + content)

        try:
            content = int(content, 16)
        except:
            continue

        if content == 0xffffffff:
            continue
        elif content == LED_ON:
            print("LED_ON")
        elif content == FERN_ON:
            print("FERN_ON")
        elif content == FERN_PLAY:
            print("FERN_PLAY")

        if content in FERN_NUMBERS:
            number = str(parse_fern_nums(content))
            if number != last_fern_parsed:
                last_fern_parsed = number
                result = simple_code.next_number(number)

                print("Parsed number: " + number)
                print("Code checker: " + str(result))

                if result:
                    # os.system("lp -d MFCJ5320DW 100\ cells\ diameter\ theta\ maze.pdf")
                    print("RIGHT CODE")

    print("CLOSED")
    reader.close()


if __name__ == '__main__':
    main()