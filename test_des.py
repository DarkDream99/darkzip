from cryptodes import des
from bitarray import bitarray


def test_des():
    text = """
    Hello, World. Python is the best!!!. sdhfjaskfjsdkjfjksdfksgasgds"
    fldjglfdgsdfgdfh
    fdhsfdhsdhshhsdfgdfkglfdgldfjkjgldsfgkdflg
    kldsfhaskjdgnksjghjhgkghf gjfdg  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    
    
    
    retkjfkgjfdghidfg
    gshfhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
    dsfjglkfdjgksfgjahugjfghdifhgfdgkfjasigjjfigjfdg
    gdfihgdgjkgjoigfdgoigg ntdg hdfghdfhgkfdhgghagihughfgfdshgdfghgjfdighig
    
    
    hfgukhdgdhsghdfughijrigjgjfdkjgidfgdsfad
    
    офылваполпоашпавпварпрпоыаплавопщп парпра прв раошпощеовп рпа рвароышщоп ршывщап фвоплавп
    """

    text_bytes = bytes(text, encoding="utf-8")
    key = "arima san"
    code, entropies = des.encrypt(text_bytes, key)
    print(code)
    print(code.tobytes().decode("utf-8", 'replace'))

    decode = des.decrypt(code, key)
    print(decode)
    print(decode.tobytes().decode("utf-8", "replace"))


test_des()