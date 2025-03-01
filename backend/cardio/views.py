from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from users.models import CustomUser
from cardio.models import Predictions

from users.utils import auth_user, jwt_decode

import json
import requests

from joblib import load

from pathlib import Path
from django.conf import settings

classifier = load(Path(settings.BASE_DIR) / 'data_notebook' / 'classifier.joblib')

@require_http_methods(["POST"])
@csrf_exempt
def predict(request):
    try:
        bearer = request.headers.get('Authorization')
        if not bearer:
            return JsonResponse({'success': False, 'message': 'Authentication header is required.'}, status=401)

        token = bearer.split()[1]
        if not auth_user(token):
            return JsonResponse({'success': False, 'message': 'Invalid token data.'}, status=401)

        decoded_token = jwt_decode(token)
        email = decoded_token.get('email')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
        
        data = json.loads(request.body)
        prediction_data = {field: data.get(field) for field in [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
            'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]}

        if not all(value is not None for value in prediction_data.values()):
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

        prediction = classifier.predict([[int(prediction_data['age']), int(prediction_data['sex']), int(prediction_data['cp']), int(prediction_data['trestbps']), int(prediction_data['chol']), int(prediction_data['fbs']), int(prediction_data['restecg']), int(prediction_data['thalach']), int(prediction_data['exang']), float(prediction_data['oldpeak']), int(prediction_data['slope']), int(prediction_data['ca']), int(prediction_data['thal'])]])
        try:
            Predictions.objects.create(user=user, prediction=int(prediction[0]), **prediction_data)
            if prediction[0] == 0:
                prediction = "Congratulations! Our model predicts that you are not likely to have heart disease. Please consult with a doctor to confirm."
            else:
                prediction = "Our model predicts that you are likely to have heart disease. Please consult with a doctor for further evaluation."
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"Error saving prediction: {str(e)}"}, status=500)
            
        return JsonResponse({'success': True, 'message': 'Prediction made successfully.', 'prediction': prediction}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Error: {str(e)}"}, status=500)
        
@require_http_methods(["POST"])
@csrf_exempt
def find_nearby_hospitals(request):
    try:
        bearer = request.headers.get('Authorization')
        if not bearer:
            return JsonResponse({'success': False, 'message': 'Authentication header is required.'}, status=401)

        token = bearer.split()[1]
        if not auth_user(token):
            return JsonResponse({'success': False, 'message': 'Invalid token data.'}, status=401)

        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            return JsonResponse({'success': False, 'message': 'Latitude and Longitude are required.'}, status=400)

        google_maps_api_key = 'AIzaSyDIIydfxdqoslmjtw_tdYjO4Fo4zRp1DwE'
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=hospital&keyword=heart&key={google_maps_api_key}'
        response = requests.get(url)
        hospitals = response.json().get('results', [])

        return JsonResponse({'success': True, 'hospitals': hospitals}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f"Error: {str(e)}"}, status=500)