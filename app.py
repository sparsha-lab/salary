from flask import Flask,render_template,request
import pickle

app=Flask(__name__)

with open("rf_salary_model.pkl", "rb") as file:
    salary_model = pickle.load(file)

with open("lb_salary.pkl", "rb") as file:
    lb_salary = pickle.load(file)

with open("lb1_salary.pkl", "rb") as file:
    lb1_salary = pickle.load(file)


def salaryPrediction(Age=33, Gender="Female", Education_Level="Bachelor's Degree", Job_Title="Software Engineer", Years_of_Experience=3):
    lst = []

    lst = lst + [Age]

    if Gender == "Female":
        lst = lst + [0]
    elif Gender == "Male":
        lst = lst + [1]
    elif Gender == "Other":
        lst = lst + [2]

    # Handle unknown education levels
    if Education_Level not in lb1_salary.classes_:
        Education_Level = lb1_salary.classes_[0]
    Education_Level = lb1_salary.transform([Education_Level])
    lst = lst + list(Education_Level)

    # Handle unknown job titles
    if Job_Title not in lb_salary.classes_:
        Job_Title = lb_salary.classes_[0]
    Job_Title = lb_salary.transform([Job_Title])
    lst = lst + list(Job_Title)

    lst = lst + [Years_of_Experience]

    result = salary_model.predict([lst])
    return result[0]



@app.route("/",methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method=="POST":
        Age=float(request.form.get("age"))
        Gender=request.form.get("gender")
        Education_Level=request.form.get("education")
        Job_Title=request.form.get("job_title")
        Years_of_Experience=float(request.form.get("experience"))
        result=salaryPrediction(Age=Age, Gender=Gender, Education_Level= Education_Level, Job_Title=Job_Title, Years_of_Experience=Years_of_Experience)
        return render_template("prediction.html",prediction=result)
    return render_template("prediction.html")

@app.route("/contact",methods=["GET"])
def contact():
    return render_template("contact.html")
if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)
