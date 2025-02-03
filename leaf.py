#Import necessary libraries
from flask import Flask, render_template, request

import numpy as np
import os

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

from flask import send_from_directory

# Create flask instance
app = Flask(__name__)
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")

app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload and stego folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


filepath = os.path.join(os.getcwd(), 'model.h5')
model = load_model(filepath)
print(model)

print("Model Loaded Successfully")

def pred_tomato_dieas(tomato_plant):
  test_image = load_img(tomato_plant, target_size = (128, 128)) # load image 
  print("@@ Got Image for prediction")
  
  test_image = img_to_array(test_image)/255 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # change dimention 3D to 4D
  
  result = model.predict(test_image) # predict diseased palnt or not
  print('@@ Raw result = ', result)
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      treatment=" Copper fungicides are the most commonly recommended treatment for bacterial leaf spot. Use copper fungicide as a preventive measure after you’ve planted your seeds but before you’ve moved the plants into their permanent homes. You can use copper fungicide spray before or after a rain, but don’t treat with copper fungicide while it is raining. If you’re seeing signs of bacterial leaf spot, spray with copper fungicide for a seven- to 10-day period, then spray again for one week after plants are moved into the field. Perform maintenance treatments every 10 days in dry weather and every five to seven days in rainy weather."
      return "Tomato - Bacteria Spot Disease", treatment
       
  elif pred==1:
      treatment="Tomatoes that have early blight require immediate attention before the disease takes over the plants. Thoroughly spray the plant (bottoms of leaves also) with Bonide Liquid Copper Fungicide concentrate or Bonide Tomato & Vegetable. Both of these treatments are organic.."
      return "Tomato - Early Blight Disease", treatment
        
  elif pred==2:
      treatment=" There is no disease on the Tomato leaf. The plant is healthy."
      return "Tomato - Healthy and Fresh",  treatment
        
  elif pred==3:
      treatment=" Tomatoes that have early blight require immediate attention before the disease takes over the plants. Thoroughly spray the plant (bottoms of leaves also) with Bonide Liquid Copper Fungicide concentrate or Bonide Tomato & Vegetable. Both of these treatments are organic.."
      return "Tomato - Late Blight Disease",  treatment
       
  elif pred==4:
      treatment=" Use drip irrigation and avoid watering foliage. Use a stake, strings, or prune the plant to keep it upstanding and increase airflow in and around it. Remove and destroy (burn) all plants debris after the harvest."
      return "Tomato - Leaf Mold Disease",  treatment
        
  elif pred==5:
    treatment="<b>Removing infected leaves: </b> Remove infected leaves immediately, and be sure to wash your hands and pruners thoroughly before working with uninfected plants. <br /> <b>Consider organic fungicide options:</b> Fungicides containing either copper or potassium bicarbonate will help prevent the spreading of the disease. Begin spraying as soon as the first symptoms appear and follow the label directions for continued management. <b>Consider chemical fungicides:</b> While chemical options are not ideal, they may be the only option for controlling advanced infections. One of the least toxic and most effective is chlorothalonil (sold under the names Fungonil and Daconil)."
    return "Tomato - Septoria Leaf Spot Disease",  treatment
        
  elif pred==6:
      treatment=" Remove and destroy infected leaves. Avoid overhead irrigation. Water early in the day so the foliage can dry before evening. Apply a copper fungicide every 7-10 days. Apply a thick layer of mulch to prevent spores from splashing from the soil onto the plant."
      return "Tomato - Target Spot Disease", treatment
        
  elif pred==7:
      treatment="Inspect plants for whitefly infestations two times per week. If whiteflies are beginning to appear, spray with azadirachtin (Neem), pyrethrin or insecticidal soap. For more effective control, it is recommended that at least two of the above insecticides be rotated at each spraying."
      return "Tomato - Tomoato Yellow Leaf Curl Virus Disease", treatment
  elif pred==8:
      treatment="There are no cures for viral diseases such as mosaic once a plant is infected. As a result, every effort should be made to prevent the disease from entering your garden."
      return "Tomato - Tomato Mosaic Virus Disease",  treatment
        
  elif pred==9:
      treatment=""" For control, use selective products whenever possible. Selective
              products which have worked well in the field include: bifenazate
              (Acramite): Group UN, a long residual nerve poison abamectin
              (Agri-Mek): Group 6, derived from a soil bacterium spirotetramat
              (Movento): Group 23, mainly affects immature stages spiromesifen
              (Oberon 2SC): Group 23, mainly affects immature stages OMRI-listed
              products include: insecticidal soap (M-Pede) neem oil (Trilogy)
              soybean oil (Golden Pest Spray Oil) With most miticides (excluding
              bifenazate), make 2 applications, approximately 5-7 days apart, to
              help control immature mites that were in the egg stage and
              protected during the first application. Alternate between products
              after 2 applications to help prevent or delay resistance."""
      return "Tomato - Two Spotted Spider Mite Disease", treatment

    


# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('uploads', filename)
        print("@@ Saving image to = ", file_path)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, treatment = pred_tomato_dieas(tomato_plant=file_path)
              
        return render_template("result.html", pred_output = pred, uploaded_image = file_path, treatment=treatment)
     
@app.route('/uploads/<filename>')
def stego_outputs(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        return f"Thank you, {name}! We received your message."
    return render_template("contact.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")
    
# For local system & cloud
if __name__ == "__main__":
    app.run(debug=True,port=8080) 
    
    
