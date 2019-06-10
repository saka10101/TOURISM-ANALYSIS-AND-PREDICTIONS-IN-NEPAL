from django.shortcuts import render
from django.views.generic import ListView , DetailView


from django.http import HttpRequest , HttpResponse ,request
import pandas as pd 
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import pylab
from pylab import *
import io
from io import *
import base64
from .models import Predictions
from django.template.response import TemplateResponse
from math import sqrt
from .models import Predictions
from .utils import render_to_pdf
from django.template.loader import get_template
dic=[]
# Create your views here.

def predict_view(request):
    all_notifications_list=Predictions.objects.order_by('created_at')[:10]
    context = {
        'all_notifications_list':all_notifications_list
    }
    return render(request,'PredictionEngine/predict_list.html',context)

def predict_view2(request):
    all_notifications_list=Predictions.objects.order_by('created_at')[:10]
    context = {
        'all_notifications_list':all_notifications_list
    }
    return render(request,'PredictionEngine/predict_list.html',context)


def PDFF(request,id,*args, **kwargs):
    
    template = get_template('pdf_format.html')

    all_details=Predictions.objects.get(id=id)
    title=all_details.title
    #print(id)
    #print(all_details)
    response=predict_detail(request,id)
    html_table=response.context_data['html_table']
    image_base64=response.context_data['image_base64']
    #image_base64g=response.context_data['image_base64g']
    #print(html_table)
   
    context = {
    'all_details': all_details ,
    'html_table': html_table ,
    'image_base64': image_base64 ,
    
     
    } 
    html = template.render(context)
    pdf = render_to_pdf('pdf_format.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = title+".pdf"
        content =" inline; filename=%s "%(filename)
        download = request.GET.get("download")
        if download:
                content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response

    return HttpResponse("Not found")

    return redirect(predict_view)


def predict_detail(request,id):
    if (id==1):
        #data collecting...converting dataset to html....
        data=pd.read_csv("F:\\ANACONDAA\\input\\gross foreign exchange earning from tourism.csv",header=0)
        df=data.iloc[:5]
        html_table_template = df.to_html(index=False)
        html_table=data.to_html(index=False)
        #data plotting/visualizing........
        #data.pivot(index='Subsector', columns='Disaster effect', values='value( NPR Million)').plot(kind='bar')
        
        data.plot()

        #storing plots in bytes
        f = io.BytesIO()
        plt.savefig(f, format="png", dpi=600,bbox_inches='tight')
        image_base64 = base64.b64encode(f.getvalue()).decode('utf-8').replace('\n', '')
        f.close()
        plt.clf()
        # getting details of id
        all_details=Predictions.objects.get(id=id)

        # Calculate the mean value of a list of numbers
        def mean(values):
            return sum(values) / float(len(values))
        
        # Calculate the variance of a list of numbers
        def variance(values, mean):
            return sum([(x-mean)**2 for x in values])
        
        # Calculate covariance between x and y
        def covariance(x, mean_x, y, mean_y):
            covar = 0.0
            for i in range(len(x)):
                covar += (x[i] - mean_x) * (y[i] - mean_y)
            return covar
        # Calculate regression coefficients
        def coefficients(X,Y):	
            x_mean, y_mean = mean(X), mean(Y)
            b1 = covariance(X, x_mean, Y, y_mean) / variance(X, x_mean)
            b0 = y_mean - b1 * x_mean
            return [b0, b1]

        # Split a dataset into a train and test set
        def train_test_split(dataset, split):
            train_size = int(split * len(dataset))
            dtrain=dataset.iloc[0:train_size].values
            dtest=dataset.iloc[train_size:].values
            return dtrain, dtest
        
        # Calculate root mean squared error
        def rmse_metric(actual, predicted):
            sum_error = 0.0
            for i in range(len(actual)):
                prediction_error = predicted[i] - actual[i]
                sum_error += (prediction_error ** 2)
            mean_error = sum_error / float(len(actual))
            return sqrt(mean_error)
        
        # Evaluate an algorithm using a train/test split
        def evaluate_algorithm(dataset, algorithm, split, *args):
            train, test = train_test_split(dataset, split)
            test_set = list()
            for row in test:
                row_copy = list(row)
                row_copy[-1] = None
                test_set.append(row_copy)
            predicted = algorithm(train, test_set, *args)
            actual = [row[-1] for row in test]
            rmse = rmse_metric(actual, predicted)
            return rmse


        # Simple linear regression algorithm
        def simple_linear_regression(train, test):
            predictions = list()
            x_train=train[:, [0]]
            y_train=train[:, [1]]
            #x_test=test.iloc[:,0]
            #y_test=train.iloc[:,1]
            b0,b1 = coefficients(x_train,y_train)
            for row in test:
                yhat = b0 + b1 * row[0] 
                predictions.append(yhat)
            return predictions

        #next step prediction in full model

        def linear_reg_perdict(Dataset,test_x):
            X=dataset.iloc[:,0].values
            Y=dataset.iloc[:,1].values
            b0,b1 = coefficients(X,Y)
            y_predict= b0 + b1 * test_x
            return y_predict


        dataset = pd.read_csv("F:\\ANACONDAA\\input\\gross foreign exchange earning from tourism.csv",skiprows=0)
        dataset.head(5)
        X=dataset.iloc[:,0].values
        Y=dataset.iloc[:,1].values



        x_mean, y_mean = mean(X), mean(Y)
        var_x, var_y = variance(X, x_mean), variance(Y, y_mean)
        covar = covariance(X, x_mean, Y, y_mean)
        b0, b1 = coefficients(X,Y)

        #showing regression graphically 
        x = X
        y1 = b0 + b1 * x
        y2= Y

        dataset.plot.line(x='starting fiscal  year ', y='Net received foreign exchange earning(NRs in million)')
        plt.plot(x,y1,color='red')

        plt.scatter(x,y2,color='k')
        plt.show()
         #storing plots in bytes
        g = io.BytesIO()
        #fig.savefig(f, format="png", dpi=600,bbox_inches='tight')
        plt.savefig(g, format="png", dpi=800,bbox_inches='tight')
        image_base64g = base64.b64encode(g.getvalue()).decode('utf-8').replace('\n', '')
        g.close()
        plt.clf()
        x=2018
        nexts=linear_reg_perdict(dataset,x)







         #parsing suitable context for redering...
        context = {
        'all_details':all_details ,
        'html_table':html_table ,
        'html_table_template': html_table_template,
        'image_base64':image_base64 ,
        'image_base64g':image_base64g ,
        'next_year_value':nexts ,
       
        }
        return TemplateResponse(request,'PredictionEngine/predict_detail.html',context)


    if (id==2):
        #data collecting...converting dataset to html....
        data=pd.read_csv("assets/predicts.csv")
        df=data.iloc[:5]
        html_table_template = df.to_html(index=False)
        html_table=data.to_html(index=False)
        
        message=""

        place=request.POST.get("place")
        purpose=request.POST.get("Major purpose of visit")
        ACCESSIBILITY=request.POST.get("ACCESSIBILITY STATUS")
        ACCOMODATION=request.POST.get("ACCOMODATION STATUS")
        MEDICAL=request.POST.get("MED STATUS")
        ACTIVITIES_C1=request.POST.get("C1")
        ACTIVITIES_C2=request.POST.get("C2")
        ACTIVITIES_C3=request.POST.get("C3")
        ACTIVITIES_C4=request.POST.get("C4")
        ACTIVITIES_C5=request.POST.get("C5")
        ACTIVITIES_C6=request.POST.get("C6")
        ACTIVITIES_C7=request.POST.get("C7")
        ACTIVITIES_C8=request.POST.get("C8")
        ACTIVITIES_C9=request.POST.get("C9")
        ACTIVITIES_C10=request.POST.get("C10")
        ACTIVITIES_C11=request.POST.get("C11")
        ACTIVITIES_C12=request.POST.get("C12")
        ACTIVITIES_C13=request.POST.get("C13")
        ACTIVITIES_C14=request.POST.get("C14")
        ACTIVITIES_C15=request.POST.get("C15")
        count=0

        SPOTS=request.POST.get("spots")
        submitt=request.POST.get("S")

        if (ACCESSIBILITY=='p'):
            a_status=1
        elif(ACCESSIBILITY=='f'):
            a_status=2
        elif(ACCESSIBILITY=='g'):
            a_status=3
        elif(ACCESSIBILITY=='b'):
            a_status=4


        if (ACCOMODATION=='p'):
            am_status=1
        elif(ACCOMODATION=='f'):
            am_status=2
        elif(ACCOMODATION=='g'):
            am_status=3
        elif(ACCOMODATION=='b'):
            am_status=4    

        if (MEDICAL=='p'):
            m_status=1
        elif(MEDICAL=='f'):
            m_status=2
        elif(MEDICAL=='g'):
            m_status=3
        elif(MEDICAL=='b'):
            m_status=4 


        if(purpose=='Treeking'):
            z=7
        elif(purpose=='Treeking and Mountaineering'):
            z=6
        elif(purpose=='holiday and pleasure'):
            z=0
        elif(purpose=='Pilgrimage visit'):
            z=37

        
           
        




        #count=ACTIVITIES_C1+ACTIVITIES_C2+ACTIVITIES_C3+ACTIVITIES_C4+ACTIVITIES_C5+ACTIVITIES_C6+ACTIVITIES_C7+ACTIVITIES_C8+ACTIVITIES_C9+ACTIVITIES_C10+ACTIVITIES_C11+ACTIVITIES_C12+ACTIVITIES_C13+ACTIVITIES_C14

        new_prediction_value=0

       

        #################################################################################################################

        # -*- coding: utf-8 -*-
        """
        Created on Mon Jun  3 10:10:14 2019

        @author: sakar
        """
        if(submitt=='PREDICT THE PERCENTAGE OF TOURIST ARRIVALS '):
            

            # Importing the dataset and separating dependent/independent variables

            dataset = pd.read_csv("assets/predicts.csv")
            
            

            print(dataset.dtypes)
            #count=ACTIVITIES_C1+ACTIVITIES_C2+ACTIVITIES_C3+ACTIVITIES_C4+ACTIVITIES_C5+ACTIVITIES_C6+ACTIVITIES_C7+ACTIVITIES_C8+ACTIVITIES_C9+ACTIVITIES_C10+ACTIVITIES_C11+ACTIVITIES_C12+ACTIVITIES_C13+ACTIVITIES_C14
            if( ACTIVITIES_C1 is not None ):count+=1 
            if (ACTIVITIES_C2 is not None): count+=1
            if (ACTIVITIES_C3 is not None ):   count+=1
            if (ACTIVITIES_C4 is not None):count+=1
            if (ACTIVITIES_C5 is not None):  count+=1 
            if (ACTIVITIES_C6 is not None):count+=1 
            if (ACTIVITIES_C7 is not None):count+=1 
            if (ACTIVITIES_C8 is not None):count+=1 
            if (ACTIVITIES_C9 is not None):count+=1 
            if (ACTIVITIES_C10 is not None):count+=1 
            if (ACTIVITIES_C11 is not None):count+=1 
            if (ACTIVITIES_C12 is not None):count+=1 
            if (ACTIVITIES_C13 is not None):count+=1 
            if (ACTIVITIES_C14 is not None):count+=1 
            if (ACTIVITIES_C15 is not None):count+=1
             


            dataset['Main purpose of visit'].value_counts()
            dataset['Accessibility status'].value_counts()
            dataset['Accomodation status'].value_counts()
            dataset['health services status'].value_counts()

            cleanup_nums = {"Accessibility status":{"Poor": 1, "Fair": 2,"Good":3,"Better":4},
                            "Accomodation status": {"Poor": 1, "Fair": 2,"Good":3,"Better":4},
                            "health services status":{"Poor": 1, "Fair": 2,"Good":3,"Better":4},
                            }
            dataset.replace(cleanup_nums, inplace=True)
            dataset.head(5)



            print(dataset.head(5))
            X = dataset.iloc[:,1:8].values
            print(X[:,3])

            y = dataset.iloc[:,10].values
            print(y)
            # Encoding categorical data
            from sklearn.preprocessing import LabelEncoder, OneHotEncoder
            labelencoder_X_3 = LabelEncoder()
            X[:, 3] = labelencoder_X_3.fit_transform(X[:, 3])

            list(labelencoder_X_3.inverse_transform([0, 1, 2, 3]))

            X[:, 3]
            X[:,0:4]
            print(X)


            onehotencoder = OneHotEncoder(categorical_features = [3] )
            X = onehotencoder.fit_transform(X).toarray()

            X = X[:, 1:]

            print('\n'.join([''.join(['{:9}'.format(item) for item in row]) 
                for row in X]))


            # Splitting the dataset into the Training set and Test set
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


            a=y_test
            b=y_train

            # Feature Scaling //escaping
            from sklearn.preprocessing import StandardScaler
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)

            # Part 2 - Now let's make the ANN!

            # Importing the Keras libraries and packages
            import keras
            from keras import backend as K
            from keras import losses
            from keras.models import Sequential
            from keras.layers import Dense
            
            # Initialising the ANN for regression
    


            #Creating regression model
            REG = Sequential()

            # Adding the input layer and the first hidden layer with dropout if required
            REG.add(Dense(units=20,input_dim=9 ,kernel_initializer="normal", activation = 'relu'))
            #REG.add(Dropout(p=0.1))
            # Adding the second hidden layer
            REG.add(Dense(units =20,kernel_initializer="normal", activation = 'relu'))
            #REG.add(Dropout(p=0.1))
            # Adding the output layer
            REG.add(Dense(units = 1, kernel_initializer="normal"))

            # Compiling the ANN
            #def root_mean_squared_error(y_true, y_pred):
            #        return K.sqrt(K.mean(K.square(y_pred - y_true))) 
                
            REG.compile(optimizer = 'adam', loss= 'mean_squared_error')

            # Fitting the ANN to the Training set
            REG.fit(X_train, y_train, batch_size = 10, epochs = 200)

            # Part 3 - Making the predictions and evaluating the model
            X_test



            # Predicting the Test set results
            y_pred = REG.predict(X_test)



            




            # Predicting a single new observation
            """Predict if the location with the following informations involves certain percentage of total tourist arrivals:
            place:    
            Year: 2018
            No.of other tourist attraction spots(within 25km radius): 2
            No. of available major tourist activities  nearby: 3
            Main purpose of visit:holiday/Pleasure 
            Accessibility status: Good
            Accomodation status: Better
            health services status:fair 
            n
            0=> holiday/pleasure
            6=>treeking&mountaineering
            7=>treeking
            37=>pilgrimage
            """
            v=X[[0,6,7,37],:][:, [0,1,2]]

            

            

                


            

            def get_hot_enc_val(n,v):
                A=X[[0,6,7,37],:][:, [0,1,2]]
                if ((n==0) or (n==6) or (n==7) or (n==37)):
                    if(n==0):
                        n=0
                    elif n==6 :
                        n=1
                    elif n==7 :
                        n=2
                    else :
                        n=3
                    v1=np.asscalar(A[[n],:][:, [0]])
                    v2=np.asscalar(A[[n],:][:, [1]])
                    v3=np.asscalar(A[[n],:][:, [2]])
                    if v==1 :
                        return v1
                    elif v==2 :
                        return v2
                    elif v==3:
                        return v3
            
            v1=get_hot_enc_val(z,1)
            v2=get_hot_enc_val(z,2)
            v3=get_hot_enc_val(z,3)
            




            new_prediction = REG.predict(sc.transform(np.array([[v1,v2,v3,2018,SPOTS,count,a_status,am_status,m_status]])))
            #new_prediction = REG.predict(sc.transform(np.array([[v1,v2,v3,2018,4,3,3,2,3]])))
            new_prediction_value=abs(np.asscalar(new_prediction))
            print(new_prediction_value)

            #dic[place]=new_prediction_value
            dic.append({place:new_prediction_value})

       

        




        

        

        context = {
        'new_prediction' :new_prediction_value ,  
        'place':place ,
        'html_table':html_table ,
        'html_table_template': html_table_template,
        'predicks':dic ,
        'message':message ,

       
        }


        return TemplateResponse(request,'PredictionEngine/predicts.html',context)



