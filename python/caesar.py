def caesar_enc(shift,raw_text):
    result_encrypted = ""

    for i in raw_text:
        if i.isalpha():
            if i.islower(): 
                base_word = ord('a') 
            else: 
                base_word = ord('A')

            encrypted = ((ord(i) - base_word + shift) % 26 + base_word)
            result_encrypted += chr(encrypted)
        else:
            encrypted += result_encrypted
    return(result_encrypted)

def caesar_dec(shift,raw_text):
    return caesar_enc(-shift,raw_text)
