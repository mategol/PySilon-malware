#<imports>
import random
#</imports>


table = {
    'a': 'aáąȧаạ',
    'b': 'bƀɓᵬḃḅ',
    'c': 'cçćĉċƈ',
    'd': 'dďɗḍḏḑ',
    'e': 'eėęȩḙẹ',
    'f': 'fƒᶂḟ',
    'g': 'gĝğġģǵ',
    'h': 'hɦḥḩḫⱨ',
    'i': 'iìíίἰἱὶ',
    'j': 'jĵǰɉʝј',
    'k': 'kķĸκкқ',
    'l': 'lĺļŀłƚ',
    'm': 'mɱᶆṁṃꝳ',
    'n': 'nņƞǹɳṇ',
    'o': 'oơοоọợ',
    'p': 'pᵱṕṗꝓ',
    'q': 'qɋԛ',
    'r': 'rŕŗɾṛṙ',
    's': 'sşșṣꜱṡ',
    't': 'tţțȶʈṭ',
    'u': 'uưυụủύ',
    'v': 'vᶌṽṿⱱ',
    'w': 'wŵԝẇẉⱳ',
    'x': 'xᶍẋẍ',
    'y': 'yƴẏỳỵỿ',
    'z': 'zȥᶎẓẕⱬ',
    'A': 'AÀÁĄȂȦ',
    'B': 'BΒВẞƁḄ',
    'C': 'CÇĆĈĊƇ',
    'D': 'DĎĐƊḊḌ',
    'E': 'EȨΈἛῈΈ',
    'F': 'FFƑḞ',
    'G': 'GĜĠĢƓǤ',
    'H': 'HḢḤḨⱧꜦ',
    'I': 'IĮΙἺἻἼ',
    'J': 'JĴɈЈ',
    'K': 'KƘΚКҜҞ',
    'L': 'LĹĻĽⱢꝈ',
    'M': 'MΜḾṀṂⱮ',
    'N': 'NŃŅƝΝṆ',
    'O': 'OΌΟОΌῸ',
    'P': 'PƤṖṔꝐꝒ',
    'Q': 'QԚꝖǪǬ',
    'R': 'RŔŖɌṘⱤ',
    'S': 'SŞȘṠṢṨ',
    'T': 'TŢƬΤҬṪ',
    'U': 'UÙÚŲƯỦ',
    'V': 'VṼṾ',
    'W': 'WŴԜẆẈⱲ',
    'X': 'XẊẌ',
    'Y': 'YŸƳẎỲỴ',
    'Z': 'ZŻȤΖẒⱫ',
}

channel_names = {
    'first_parts': ['Happy', 'Joyful', 'Amazing', 'Mighty', 'Curious', 'Playful', 'Silly', 'Crazy', 'Sneaky', 'Wise', 'Clever', 'Smart', 'Brave', 'Bold', 'Strong', 'Powerful'],
    'second_parts': ['Cat', 'Giraffe', 'Hippo', 'Chihuahua', 'Penguin', 'Panda', 'Koala', 'Kangaroo', 'Elephant', 'Lion', 'Tiger', 'Bear', 'Wolf', 'Fox', 'Raccoon', 'Squirrel', 'Rabbit', 'Hedgehog', 'Owl', 'Eagle', 'Falcon', 'Hawk', 'Parrot', 'Duck', 'Goose', 'Swan', 'Pigeon', 'Sparrow']
}

def render_text(text, result=''):
    for char in text:
        if char in table: result += random.choice(table[char])
        else: result += char
    return result

def generate_channel_name():
    return f'{random.choice(channel_names["first_parts"])}{random.choice(channel_names["second_parts"])}'