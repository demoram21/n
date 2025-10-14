from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import os
import requests


app = Flask(__name__)
CORS(app, origins=["https://frontend-sigma-seven-58.vercel.app"])



MODEL_PATH = 'skin_disease_model.h5'
MODEL_URL = 'https://drive.google.com/uc?export=download&id=1k1wJY7mfBloaDEmqwD9Xpgs2f7z_Oeub' 

if not os.path.exists(MODEL_PATH):
    print(f"Model not found. Downloading from Google Drive...")
    r = requests.get(MODEL_URL, allow_redirects=True)
    with open(MODEL_PATH, 'wb') as f:
        f.write(r.content)
    print("Model downloaded successfully.")

model = tf.keras.models.load_model(MODEL_PATH)


CLASS_NAMES = [
    'Acne and Rosacea Photos', 'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 
    'Atopic Dermatitis Photos', 'Bullous Disease Photos', 'Cellulitis Impetigo and other Bacterial Infections', 
    'Eczema Photos', 'Exanthems and Drug Eruptions', 'Hair Loss Photos Alopecia and other Hair Diseases', 
    'Herpes HPV and other STDs Photos', 'Light Diseases and Disorders of Pigmentation', 
    'Lupus and other Connective Tissue diseases', 'Melanoma Skin Cancer Nevi and Moles', 
    'Nail Fungus and other Nail Disease', 'Poison Ivy Photos and other Contact Dermatitis', 
    'Psoriasis pictures Lichen Planus and related diseases', 'Scabies Lyme Disease and other Infestations and Bites', 
    'Seborrheic Keratoses and other Benign Tumors', 'Systemic Disease', 
    'Tinea Ringworm Candidiasis and other Fungal Infections', 'Urticaria Hives', 
    'Vascular Tumors', 'Vasculitis Photos', 'Warts Molluscum and other Viral Infections'
]

TREATMENT_DATABASE = {
    
    'Acne and Rosacea Photos': {
        'treatment': 'These are common inflammatory skin conditions...', 
        'recommendations': ['...'], 
        'critical': False
    },
    'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions': {
        'treatment': 'This category includes pre-cancerous and cancerous lesions that require immediate medical attention for diagnosis and treatment, which may include removal.',
        'recommendations': ['‼️ URGENT: Seek immediate consultation with a dermatologist.', '🔬 A biopsy is necessary for a definitive diagnosis.', '☀️ Practice rigorous sun protection.'],
        'critical': True
    },
    'Atopic Dermatitis Photos': {
        'treatment': 'A type of eczema causing dry, itchy, and inflamed skin. Management focuses on hydrating the skin, using medicated creams, and avoiding triggers.',
        'recommendations': ['💧 Keep skin well-moisturized at all times.', '🛀 Take short, lukewarm baths.', '🚫 Avoid harsh soaps and known allergens.'],
        'critical': False
    },
    'Bullous Disease Photos': {
        'treatment': 'A group of skin conditions that cause blisters. This requires diagnosis by a specialist, as treatment depends on the specific type and cause.',
        'recommendations': ['🧑‍⚕️ See a dermatologist for proper diagnosis.', '🚫 Do not pop or drain blisters yourself to avoid infection.', '🩹 Gently cover broken blisters with a non-stick bandage.'],
        'critical': True
    },
    'Cellulitis Impetigo and other Bacterial Infections': {
        'treatment': 'These are bacterial skin infections that typically require oral or topical antibiotics prescribed by a doctor.',
        'recommendations': ['🩺 See a doctor immediately for diagnosis and antibiotics.', '🧼 Keep the area clean and dry.', '🩹 Cover the affected skin to prevent spreading.'],
        'critical': True
    },
    'Eczema Photos': {
        'treatment': 'A condition causing dry, itchy, and inflamed skin. Treatment focuses on healing the damaged skin barrier with moisturizers and topical corticosteroids.',
        'recommendations': ['💧 Moisturize skin frequently, especially after bathing.', '🛀 Use lukewarm water and mild, fragrance-free soaps.', '👚 Wear soft, breathable fabrics.'],
        'critical': False
    },
    'Exanthems and Drug Eruptions': {
        'treatment': 'Widespread rashes often caused by viral infections or reactions to medication. Treatment involves identifying and stopping the cause if possible, and managing symptoms like itching.',
        'recommendations': ['🤔 If a new medication was started, contact your doctor.', ' antihistamines for itching.', '🧑‍⚕️ Consult a doctor to determine the cause.'],
        'critical': False
    },
    'Hair Loss Photos Alopecia and other Hair Diseases': {
        'treatment': 'Hair loss has many causes. A dermatologist or trichologist can diagnose the specific condition and recommend treatments, which can range from topical solutions to medications.',
        'recommendations': ['👨‍⚕️ Consult a dermatologist for an accurate diagnosis.', '🌿 Use gentle hair care products.', '💆 Avoid tight hairstyles that pull on the hair.'],
        'critical': False
    },
    'Herpes HPV and other STDs Photos': {
        'treatment': 'These are viral infections that require medical diagnosis and management with prescribed antiviral medications.',
        'recommendations': ['🩺 See a healthcare professional for confidential testing and treatment.', '💊 Take prescribed medication exactly as directed.', '🤝 Inform partners as advised by your doctor.'],
        'critical': True
    },
    'Light Diseases and Disorders of Pigmentation': {
        'treatment': 'This broad category includes conditions like vitiligo or melasma. Treatment varies widely and should be directed by a dermatologist.',
        'recommendations': ['☀️ Rigorous sun protection is essential.', '👨‍⚕️ A dermatologist can provide a specific diagnosis.', '💡 Treatments may include topical creams or light therapy.'],
        'critical': False
    },
    'Lupus and other Connective Tissue diseases': {
        'treatment': 'These are systemic autoimmune diseases that can manifest on the skin, often as rashes. They require management by a specialist like a rheumatologist.',
        'recommendations': ['🧑‍⚕️ See a specialist (rheumatologist or dermatologist).', '☀️ Sun exposure can trigger flare-ups; protect your skin.', ' takip a comprehensive treatment plan.'],
        'critical': True
    },
    'Melanoma Skin Cancer Nevi and Moles': {
        'treatment': 'This category includes both benign moles (nevi) and the most serious form of skin cancer (melanoma). Any suspicious mole requires immediate evaluation.',
        'recommendations': ['‼️ URGENT: See a dermatologist for any changing mole.', '🧐 Use the ABCDE rule to check your moles.', '☀️ Practice rigorous sun protection.'],
        'critical': True
    },
    'Nail Fungus and other Nail Disease': {
        'treatment': 'Conditions affecting fingernails and toenails. Fungal infections often require oral or topical antifungal medications.',
        'recommendations': ['👨‍⚕️ Consult a doctor or podiatrist for diagnosis.', '🍄 Antifungal treatments can take a long time to work.', '👟 Keep feet clean and dry.'],
        'critical': False
    },
    'Poison Ivy Photos and other Contact Dermatitis': {
        'treatment': 'An itchy rash caused by contact with an allergen or irritant. Treatment involves washing the skin, using soothing lotions like calamine, and topical steroids.',
        'recommendations': ['🌿 Identify and avoid the plant or substance that caused the rash.', '🧼 Gently wash the affected area with soap and water.', '🚫 Avoid scratching to prevent infection.'],
        'critical': False
    },
    'Psoriasis pictures Lichen Planus and related diseases': {
        'treatment': 'Chronic inflammatory conditions. Treatment aims to manage symptoms and can include topical creams, light therapy, and systemic medications.',
        'recommendations': ['🧴 Keep skin well-moisturized.', '👨‍⚕️ Work with a dermatologist to create a management plan.', '🌿 Avoid known triggers like stress.'],
        'critical': False
    },
    'Scabies Lyme Disease and other Infestations and Bites': {
        'treatment': 'These conditions are caused by bites or infestations (like mites) and require specific medical treatments to eliminate the cause.',
        'recommendations': ['🩺 See a doctor for diagnosis and prescribed medication.', '🧺 Wash all clothing and bedding in hot water.', '🚫 Avoid close contact to prevent spreading.'],
        'critical': True
    },
    'Seborrheic Keratoses and other Benign Tumors': {
        'treatment': 'Common non-cancerous skin growths. They do not require treatment but can be removed for cosmetic reasons or if they become irritated.',
        'recommendations': ['✅ These are typically harmless.', '🤔 Monitor for any significant changes.', '👨‍⚕️ A dermatologist can confirm the diagnosis.'],
        'critical': False
    },
    'Systemic Disease': {
        'treatment': 'This indicates a skin manifestation of an internal, body-wide disease. The underlying condition must be diagnosed and treated by a medical professional.',
        'recommendations': ['‼️ URGENT: See a medical doctor promptly.', '🩺 This requires a full medical workup to diagnose the internal cause.', ' takip the treatment plan from your specialist.'],
        'critical': True
    },
    'Tinea Ringworm Candidiasis and other Fungal Infections': {
        'treatment': 'Common fungal infections treated with over-the-counter or prescription antifungal creams or oral medications.',
        'recommendations': ['🍄 Apply topical antifungal medication as directed.', '🧼 Keep the affected area clean and dry.', '🚫 Avoid sharing towels, combs, or clothing.'],
        'critical': False
    },
    'Urticaria Hives': {
        'treatment': 'Itchy welts often caused by an allergic reaction. Usually treated with antihistamines and avoidance of the trigger.',
        'recommendations': ['🤧 Take over-the-counter antihistamines.', '🤔 Try to identify and avoid the trigger (food, pollen, etc.).', '🚨 Seek emergency care if you have trouble breathing.'],
        'critical': False
    },
    'Vascular Tumors': {
        'treatment': 'A broad category of growths made of blood vessels, most of which are benign (like cherry angiomas). Treatment is often not necessary.',
        'recommendations': ['😊 Most are harmless cosmetic issues.', '👨‍⚕️ Have any new or changing growth checked by a doctor.', '⚡ Laser treatment is a common option for removal.'],
        'critical': False
    },
    'Vasculitis Photos': {
        'treatment': 'Inflammation of the blood vessels, which can be serious. This requires diagnosis and management by a specialist.',
        'recommendations': ['🧑‍⚕️ See a specialist like a rheumatologist or dermatologist.', ' takip your prescribed treatment plan carefully.', '🩸 Report any new or worsening symptoms to your doctor.'],
        'critical': True
    },
    'Warts Molluscum and other Viral Infections': {
        'treatment': 'Common, benign skin growths caused by viruses. Can be treated with over-the-counter remedies or removed by a doctor.',
        'recommendations': ['🩹 Cover warts to prevent spreading the virus.', '🚫 Do not pick or scratch them.', '👨‍⚕️ Consult a doctor for persistent or numerous growths.'],
        'critical': False
    },
    'Default': {
        'treatment': 'Could not determine the specific condition with high confidence. It is essential to consult a healthcare professional for an accurate diagnosis.',
        'recommendations': ['❓ Low confidence prediction.', '👨‍⚕️ Please see a qualified dermatologist.', '🔬 Further tests may be required.'],
        'critical': True
    }
}

@app.route('/predict', methods=['POST'])
def predict():
    
    if 'image' not in request.files: return jsonify({'error': 'No image file provided'}), 400
    file = request.files['image']
    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB': image = image.convert('RGB')
        img = image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        predicted_disease = CLASS_NAMES[predicted_class_index]
        if confidence < 0.50:
            disease_info = TREATMENT_DATABASE['Default']
            predicted_disease = "Uncertain"
        else:
            disease_info = TREATMENT_DATABASE.get(predicted_disease, TREATMENT_DATABASE['Default'])
        result = {
            'disease': predicted_disease, 'confidence': confidence, 'treatment': disease_info['treatment'],
            'recommendations': disease_info['recommendations'], 'critical': disease_info['critical']
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/share-telegram', methods=['POST'])
def share_telegram():
    
    data = request.json
    disease = data.get('disease'); confidence = data.get('confidence'); treatment = data.get('treatment')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN'); chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not bot_token or not chat_id: return jsonify({'error': 'Server configuration for Telegram is missing.'}), 500
    message_text = (f"<b>🔬 AI Diagnosis Report</b>\n...\n<b>Disease Detected:</b> {disease}\n...")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        response = requests.post(url, json={'chat_id': chat_id, 'text': message_text, 'parse_mode': 'HTML'})
        response.raise_for_status()
        return jsonify({'message': 'Message sent successfully'}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to send message: {e}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)

