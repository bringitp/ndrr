from janome.tokenizer import Tokenizer

def tokenize_text(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    return tokens

if __name__ == "__main__":
    text = "xxx死ね。タヒオカね。クソババアゴミムシはよしね。"
    tokens = tokenize_text(text)
    
    for token in tokens:
        print(f"Surface: {token.surface}, Part of Speech: {token.part_of_speech}")
