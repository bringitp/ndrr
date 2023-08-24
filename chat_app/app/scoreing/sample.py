from janome.tokenizer import Tokenizer

def tokenize_text(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    return tokens

if __name__ == "__main__":
    text = "それはとてもつまらないしね"
    tokens = tokenize_text(text)

    text2 = "それはとてもつまらないシネ"
    tokens2 = tokenize_text(text2)
    
    for token in tokens:
        print(f"Surface: {token.surface}, Part of Speech: {token.part_of_speech}")

    print ("---------------")

    for token in tokens2:
        print(f"Surface: {token.surface}, Part of Speech: {token.part_of_speech}")
