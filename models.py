from django.db import models

# Create your models here.
class SspModels(models.Model):
    sspid=models.AutoField(primary_key=True)
    xmpzh=models.CharField(max_length=100)
    xmlb=models.CharField(max_length=30)
    xkfl=models.CharField(max_length=50)
    xmmc=models.CharField(max_length=300)
    lxsj=models.DateField()
    xmfzr=models.CharField(max_length=50)
    zyzw=models.CharField(max_length=30)
    gzdw=models.CharField(max_length=100)
    dwlb=models.CharField(max_length=50)
    szssq=models.CharField(max_length=100)
    ssxt=models.CharField(max_length=100)