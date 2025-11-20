from flask import Flask,render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('maas.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        isim = request.form['isim']
        tecrube = float(request.form['tecrube'])
        yazili = float(request.form['yazili'])
        mulakat = float(request.form['mulakat'])

        # Here you would typically preprocess the input and make a prediction
        # For demonstration, let's assume the model predicts based on the input directly
        tahmin = model.predict([[tecrube, yazili, mulakat]])
        
        # Format the prediction to be more professional
        maas = float(tahmin[0])
        maas_formatted = f"{maas:,.2f} TL"

        return render_template('index.html', tahmin=f"Sayın {isim}, tahmini maaşınız: {maas_formatted}")

if __name__ == '__main__':
    app.run(debug=True)
