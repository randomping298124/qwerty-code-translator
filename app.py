from flask import Flask, render_template, request

app = Flask(__name__)

# --- Your Translation Functions ---
def encode_qwerty(plaintext):
    qwerty_layout = "qwertyuiopasdfghjklzxcvbnm"
    encoded_text = ""
    for char in plaintext.lower():
        if char == " ":
            encoded_text += qwerty_layout
        elif char in qwerty_layout:
            encoded_text += qwerty_layout.replace(char, "")
        else:
            encoded_text += char
    return encoded_text

def decode_qwerty(encoded_text):
    qwerty_layout = "qwertyuiopasdfghjklzxcvbnm"
    decoded_text = ""
    i = 0
    while i < len(encoded_text):
        if not encoded_text[i].isalpha():
            decoded_text += encoded_text[i]
            i += 1
            continue
        j = 0
        missing_char = " " 
        while j < 26:
            if i < len(encoded_text) and encoded_text[i].isalpha() and encoded_text[i] == qwerty_layout[j]:
                i += 1
            else:
                missing_char = qwerty_layout[j]
            j += 1
        decoded_text += missing_char
    return decoded_text

# --- Web Server Route ---
@app.route("/", methods=["GET", "POST"])
def home():
    result_text = ""
    original_text = ""
    
    if request.method == "POST":
        original_text = request.form.get("user_input")
        action = request.form.get("action")
        
        if action == "encode":
            result_text = encode_qwerty(original_text)
        elif action == "decode":
            result_text = decode_qwerty(original_text)
            
    return render_template("index.html", result=result_text, original=original_text)

if __name__ == "__main__":
    app.run(debug=True)
