from django.shortcuts import render, redirect
from django.conf import settings
from .models import Image
from .forms import ImageForm
from PIL import Image as PILImage
import os

def load_model():
    import tensorflow as tf
    return tf.keras.models.load_model('Animal_Recog_Model.h5')

def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            image_instance = form.save()
            
            try:
                # Load the model only when needed
                model = load_model()
                
                # Prepare the image for prediction
                img_path = image_instance.image.path
                img = PILImage.open(img_path)
                img = img.resize((224, 224))  # Adjust size according to your model's requirements
                
                import tensorflow as tf
                img_array = tf.keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)
                
                # Make prediction
                predictions = model.predict(img_array)
                predicted_class = "Animal"  # Replace with your class labels
                
                # Update the prediction
                image_instance.prediction = predicted_class
                image_instance.save()
            except Exception as e:
                image_instance.prediction = f"Error: {str(e)}"
                image_instance.save()
            
            return redirect('index')
    else:
        form = ImageForm()
    
    images = Image.objects.all().order_by('-uploaded_at')
    return render(request, 'classifier/index.html', {'form': form, 'images': images})
