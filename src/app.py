from flask import Flask, render_template, request
import requests

# Informamos ao Flask que os arquivos estão na mesma pasta que este arquivo
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html', imagem='cat-hugging.gif')

@app.route('/converter', methods=['POST']) 
def converter():
    try:
        # Pegando os dados do formulário
        valor = float(request.form.get('valor'))
        moeda_de = request.form.get('moeda_origem')
        moeda_para = request.form.get('moeda_destino')

        # Buscando cotações atualizadas
        # Aqui pedimos o valor do Dólar(USD) e Euro(EUR) em relação ao Real(BRL)
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL"
        resposta = requests.get(url)
        dados = resposta.json()

        # Extraindo as taxas (a API retorna textos, convertemos para float)
        # A AwesomeAPI retorna o preço de compra no campo 'bid'

        # Pegando os valores de 1 Dólar e 1 Euro em Reais
        cotacao_usd = float(dados['USDBRL']['bid'])
        cotacao_eur = float(dados['EURBRL']['bid'])

        # Criamos a tabela onde a chave é a moeda e o valor é quanto ela vale em REAIS
        # BRL é a base (vale 1), USD vale ~5.00, EUR vale ~5.40
        tabela_precos = {
            "BRL": 1.0,
            "USD": cotacao_usd,
            "EUR": cotacao_eur
        }

        # Lógica Universal:
        # 1. Converte o valor de origem para REAIS (multiplicando)
        # 2. Converte de REAIS para a moeda de destino (dividindo)
        valor_em_reais = valor * tabela_precos[moeda_de]
        resultado = valor_em_reais / tabela_precos[moeda_para]

        return render_template('index.html', valor_original=f"{valor:.2f}", moeda_origem=moeda_de, resultado=f"{resultado:.2f}", moeda_destino=moeda_para, imagem='congratulations.gif')
    
    except Exception as e:
        return f"Erro ao conectar com a API: {e}"
        

























if __name__ == '__main__':
    # O debug=True ajuda a ver erros no navegador enquanto desenvolvemos
    app.run(debug=True)
