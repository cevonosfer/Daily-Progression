def encrypter(shift,raw_text):
    result = ""

    for i in raw_text:
        if i.isalpha():
            if i.islower(): 
                base_word = ord('a') 
            else: 
                base_word = ord('A')

            encrypted = ((ord(i) - base_word + shift) % 26 + base_word)
            result += chr(encrypted)
        else:
            encrypted += result
    print(result)

encrypter(shift=5,raw_text = input("enter your text here: "))