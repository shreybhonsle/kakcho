
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np
import os
from django.http import HttpResponse
import zlib
import zipfile
from pathlib import Path
import shutil
from django.http import HttpResponse, Http404

def home(request):
    if request.method == 'POST':
        uploaded_file  = request.FILES['document']
        #save file 
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        messages.success(request,"Successfully Uploaded File")


    return render(request,'home/home.html')

def process(request):
        #get first file from media
        path = os.path.join(settings.MEDIA_ROOT)
        f= os.listdir(path)[0]
        path += '/'
        path += f
        fp = open(path,'+r')
        os.remove(path)
        df = pd.read_csv(fp)
        df1 = df[df['Type']=='Free']
        df2 = df[df['Type']=='Paid']
        df1.columns = [c.replace(' ', '_') for c in df1.columns]
        df2.columns = [c.replace(' ', '_') for c in df2.columns]
        df.columns = [c.replace(' ', '_') for c in df1.columns]

        cr = set(df.Content_Rating.unique())
        FilterOnCR = {}
        for x in cr:
            FilterOnCR[x]=df[df['Content_Rating']==x]
        df.fillna(method='backfill',axis=1)
        df['Rating Roundoff'] = df.Rating.apply(np.round)
        names = []
        
        df1.to_csv('df1.csv')
        names.append('df1.csv')
        df2.to_csv('df2.csv')
        names.append('df2.csv')
        df.to_csv('df.csv')
        names.append('df.csv')
        i=3
        #iterating through the dictionary
        for key,value in FilterOnCR.items():
            value.to_csv('df'+str(i)+'.csv')
            names.append('df'+str(i)+'.csv')
            i+=1
            
        path = os.getcwd()+'/'
        with zipfile.ZipFile('final.zip','w') as zipF:
            for file in names:
                zipF.write(file,compress_type=zipfile.ZIP_DEFLATED)
        for x in names:
            os.remove(x)
        shutil.move('COMBINED_SOLUTIONS.zip','./media')

        return render(request,'home/home.html')

        
    

def handlelogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return render(request,'home/home.html')


def download(request):
    file_path = os.path.join(settings.MEDIA_ROOT)
    f= os.listdir(file_path)[0]
    file_path += '/'
    file_path += f
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404