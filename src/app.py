from flask import Flask, render_template

# Informamos ao Flask que os arquivos estão na mesma pasta que este arquivo
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # O debug=True ajuda a ver erros no navegador enquanto desenvolvemos
    app.run(debug=True)