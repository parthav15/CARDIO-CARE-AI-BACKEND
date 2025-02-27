from django.db import models
from users.models import CustomUser

class Predictions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="predictions")
    age = models.PositiveIntegerField(help_text="Age of the patient", default="", blank=True, null=True)
    sex = models.IntegerField(
        help_text="Sex of the patient (1 for Male, 0 for Female)",
        default=0,
        blank=True,
        null=True,
    )
    cp = models.PositiveIntegerField(help_text="Chest pain type", default="", blank=True, null=True)
    trestbps = models.PositiveIntegerField(help_text="Resting blood pressure", default="", blank=True, null=True)
    chol = models.PositiveIntegerField(help_text="Serum cholesterol", default="", blank=True, null=True)
    fbs = models.PositiveIntegerField(help_text="Fasting blood sugar", default="", blank=True, null=True)
    restecg = models.PositiveIntegerField(help_text="Resting electrocardiographic results", default="", blank=True, null=True)
    thalach = models.PositiveIntegerField(help_text="Maximum heart rate achieved", default="", blank=True, null=True)
    exang = models.PositiveIntegerField(help_text="Exercise induced angina", default="", blank=True, null=True)
    oldpeak = models.FloatField(help_text="ST depression induced by exercise relative to rest", default="", blank=True, null=True)
    slope = models.PositiveIntegerField(help_text="Slope of the peak exercise ST segment", default="", blank=True, null=True)
    ca = models.PositiveIntegerField(help_text="Number of major vessels (0-3) colored by flourosopy", default="", blank=True, null=True)
    thal = models.CharField(
        max_length=1,
        choices=[("N", "Normal"), ("Y", "Yes"), ("R", "Reversible defect")],
        help_text="Thalassemia",
        default="",
        blank=True,
        null=True,
    )
    prediction = models.IntegerField(null=True, blank=True, help_text="The prediction made by the model")