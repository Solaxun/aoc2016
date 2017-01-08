import re
# test = 'zazbz[bzb]cdb'#true
# test1 = 'aba[bab]xyz'#true
# test2 = 'xyx[xyx]xyx'#false
# test3 = 'aaa[kek]eke'#true
test = 'aefghijk[abcajlaefellijljlbe]abefglhi[aeroraljo]keulmoroln'
IP_ADDRESSES = open('AoC7.txt').read().split('\n')
# print(IP_ADDRESSES[1])

def parse_ip(ip):
    not_brackets = ''.join(re.split('\[[a-z]*\]',ip))
    brackets = [bracket[1:-1]for bracket in re.findall('\[[a-z]*\]',ip)]
    # return (True if any(map(abba,not_brackets)) 
    #     and not any(map(abba,brackets)) else False)
    all_aba = get_aba(not_brackets)
    all_bab = [each for bab in (map(get_aba,brackets)) for each in bab]
    # print(all_aba)
    # print(all_bab)
    for a in all_aba:
        for b in all_bab:
            if a[0] == b[1] and a[1] == b[0]:
                return True
    return False


def abba(text):
    for i in range(0,len(text)-4 + 1):
        candidate = text[i:i+4]
        if (candidate[0:2] == ''.join(list(reversed(candidate[2:]))) 
        and candidate[0] != candidate[1]):
            return True
    return False

def get_aba(text):
    all_aba = []
    for i in range(0,len(text)-3 + 1):
        candidate = text[i:i+3]
        if candidate == candidate[::-1]:
            all_aba.append(candidate)
    return all_aba

# print(parse_ip(test))
print(sum(map(parse_ip,IP_ADDRESSES)))


