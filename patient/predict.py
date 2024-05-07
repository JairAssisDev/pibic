import io
import matplotlib
from flask import Blueprint,request, jsonify
import joblib
import lime
import lime.lime_tabular
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64

predict_bp = Blueprint('predict', __name__, url_prefix='/patient/predict')

matplotlib.use('Agg')


# Carregar o modelo e outros dados necessários
model = joblib.load("model/RF.joblib")
train = pd.read_csv("files/X_train.csv", usecols=range(1, 7)).to_numpy()
class_names = model.classes_
feature_names= model.feature_names_in_
explainer = lime.lime_tabular.LimeTabularExplainer(train, feature_names=feature_names, class_names=class_names, discretize_continuous=True)


def encode_categorical(sex, redo, cpb):
    sex = 1 if sex == "Male" else 0
    redo = 1 if redo == "Yes" else 0
    cpb = 1 if cpb == "Yes" else 0
    return sex, redo, cpb

def explain_instance(instance):
    exp = explainer.explain_instance(np.array(instance), model.predict_proba, num_features=6)
    return exp

def prepare_features_and_values(exp):
    exp_features = exp.as_list()
    features, values = zip(*exp_features)
    return features[::-1], values[::-1]

def assign_colors(values):
    colors = ['red' if val > 0 else 'green' for val in values]
    return colors

def create_plot(features, values, colors):
    fig, ax = plt.subplots()
    y_pos = np.arange(len(features))
    ax.barh(y_pos, values, color=colors, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features)
    ax.invert_yaxis()
    ax.set_xlabel('Feature Contribution')
    ax.set_ylabel('Features')
    ax.set_title('Feature Importance')
    return fig

def predict_and_explain(sex, redo, cpb, age, bsa, hb):
    sex, redo, cpb = encode_categorical(sex, redo, cpb)
    instance = [sex, age, bsa, redo, cpb, hb]
    prediction_proba = model.predict_proba([instance])[0]
    
    # Previsão da classe e suas probabilidades
    prediction = bool(model.predict([instance])[0])
    true_prob = prediction_proba[1]  # Probabilidade de Verdadeiro
    false_prob = prediction_proba[0]  # Probabilidade de Falso
    
    # Gráfico de probabilidades
    fig, ax = plt.subplots()
    labels = ['True', 'False']
    values = [true_prob, false_prob]
    ax.bar(labels, values, color=['green', 'red'])
    ax.set_ylabel('Probability')
    ax.set_title('Prediction Probabilities')
    image_data_probabilities = save_image_to_base64(fig, fig_size=(6, 4))
    plt.close(fig)
    
    # Gráfico de explicação
    exp = explain_instance(instance)
    features, values = prepare_features_and_values(exp)
    colors = assign_colors(values)
    fig = create_plot(features, values, colors)
    image_data_explanation = save_image_to_base64(fig, fig_size=(10, 6))
    plt.close(fig)
    
    return {
        "prediction": prediction,
        "true_probability": true_prob,
        "false_probability": false_prob,
        "probabilities_chart": image_data_probabilities["image_base64"],
        "lime_image": image_data_explanation["image_base64"]
    }





def save_image_to_base64(fig, fig_size=(8, 6)):
    fig.set_size_inches(fig_size)  # Definir o tamanho da figura
    fig.tight_layout()  # Ajustar layout para evitar cortes
    image_buffer = io.BytesIO()
    fig.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    image_bytes = image_buffer.read()
    plt.close()

    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    return {
        "image_base64": image_base64
    }

@predict_bp.route("/", methods=["GET"])
def index():
    return "Hello, World!"

@predict_bp.route("/", methods=["POST"])
def predict():
    try:
        data = request.json  # Suponha que você está enviando os dados JSON para a API
        sex = data["sex"]
        redo = data["redo"]
        cpb = data["cpb"]
        age = float(data["age"])  # Converter para float
        bsa = float(data["bsa"])  # Converter para float
        hb = float(data["hb"])  # Converter para float
        
        # Validação
        if age < 0 or age > 150:
            return jsonify({"error": "Age must be between 0 and 150."}), 400
        if bsa < 0.0 or bsa > 5.0:
            return jsonify({"error": "Body Surface Area (BSA) must be between 0.0 and 5.0."}), 400
        if hb < 0.0 or hb > 20.0:
            return jsonify({"error": "Hemoglobin (HB) must be between 0.0 and 20.0."}), 400

        return predict_and_explain(sex, redo, cpb, age, bsa, hb)

    except KeyError as e:
        missing_key = str(e)
        return jsonify({"error": f"Key '{missing_key}' is missing in the request."}), 400
    except ValueError as e:
        return jsonify({"error": "Invalid value type. Age, BSA, and HB must be numeric values."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Retorna um erro 500 com uma mensagem de erro JSON
