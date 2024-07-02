import io
import matplotlib
import joblib
import lime
import lime.lime_tabular
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64

matplotlib.use('Agg')

model = joblib.load("model_ML/RF.joblib")
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
    
    prediction = bool(model.predict([instance])[0])
    true_prob = prediction_proba[1]
    
    return {
        "prediction": prediction,
        "true_probability": true_prob,
    }

def predict_and_explain_image(sex, redo, cpb, age, bsa, hb):
    sex, redo, cpb = encode_categorical(sex, redo, cpb)
    instance = [sex, age, bsa, redo, cpb, hb]
    prediction_proba = model.predict_proba([instance])[0]
    
    prediction = bool(model.predict([instance])[0])
    true_prob = prediction_proba[1]
    
    exp = explain_instance(instance)
    features, values = prepare_features_and_values(exp)
    colors = assign_colors(values)
    fig = create_plot(features, values, colors)
    image_data_explanation = save_image_to_base64(fig, fig_size=(10, 6))
    plt.close(fig)
    
    return {
        "prediction": prediction,
        "true_probability": true_prob,
        "lime_image": image_data_explanation["image_base64"]
    }

def save_image_to_base64(fig, fig_size=(8, 6)):
    fig.set_size_inches(fig_size) 
    fig.tight_layout()
    image_buffer = io.BytesIO()
    fig.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    image_bytes = image_buffer.read()
    plt.close()

    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    return {
        "image_base64": image_base64
    }