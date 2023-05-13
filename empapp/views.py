from django.shortcuts import render,redirect
from elasticsearch import Elasticsearch
from .models import Employee
from .form import MyForm
from django.contrib import messages
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch_dsl.connections import connections
from django.contrib import messages




def add_details(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Get the data from the form
            emp_id=form.cleaned_data['emp_id']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            mobileno = form.cleaned_data['mobileno']
            gender = form.cleaned_data['gender']
            created_at = form.cleaned_data['created_at']
            updated_at = form.cleaned_data['updated_at']

            # Insert the data into Elasticsearch
            es = Elasticsearch('http://localhost:9200/')
            doc = {
                'emp_id':emp_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'gender': gender,
                'mobileno': mobileno,
                'created_at': created_at,
                'updated_at': updated_at,

            }
            es.index(index='userinformation', body=doc,id=emp_id)
            messages.success(request, 'Employee added successfully.')
            return redirect('/')

            # Render a success message
            return render(request, 'display.html')

    else:
        form = MyForm()

    return render(request, 'display.html', {'form': form})

def getdetails(request):
    es = Elasticsearch('http://localhost:9200/')
    query = {
        "query": {
            "match_all": {}
        },"sort":[{"emp_id":"asc"}]
    }
    search_data = es.search(index='userinformation', body=query)
    results = [hit['_source'] for hit in search_data['hits']['hits']]
    print(results)
    context = {'results': results}
    return render(request, 'screen.html', context)

def update(request,emp_id):
    es = Elasticsearch('http://localhost:9200/')
    document = es.get(index='userinformation', id=emp_id)
    if request.method=='POST':
        form=MyForm(request.POST)
        if form.is_valid():
            document['_source']['emp_id']=form.cleaned_data['emp_id']
            document['_source']['first_name']=form.cleaned_data['first_name']
            document['_source']['last_name']=form.cleaned_data['last_name']
            document['_source']['email']=form.cleaned_data['email']
            document['_source']['gender']=form.cleaned_data['gender']
            document['_source']['mobileno']=form.cleaned_data['mobileno']
            document['_source']['created_at']=form.cleaned_data['created_at']
            document['_source']['updated_at']=form.cleaned_data['updated_at']
            es.index(index='userinformation', id=emp_id, body=document['_source'])
            messages.success(request, 'Profile updated successfully.')
            return redirect('home')
    else:
        form = MyForm(initial={
            'emp_id': document['_source']['emp_id'],
            'first_name':document['_source']['first_name'],
            'last_name': document['_source']['last_name'],
            'email': document['_source']['email'],
            'gender': document['_source']['gender'],
            'mobileno': document['_source']['mobileno'],
            'created_at': document['_source']['created_at'],
            'updated_at': document['_source']['updated_at']


        })

    return render(request,'update.html',{'form':form})


def deletedata(request,emp_id):
    es = Elasticsearch('http://localhost:9200/')
    """Delete Details"""
    if request.method=='POST':
        es.delete(index="userinformation", id=emp_id)
        messages.success(request, 'Employee deleted successfully.')
    return redirect('/')

es_client = connections.create_connection(hosts=[settings.ELASTICSEARCH_HOST])

def handle_data(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if es_client.ping():
                obj.indexing()
                messages.success(request, 'Data saved and indexed successfully')
            else:
                obj.save()
                messages.success(request, 'Data saved successfully')
            return redirect('home')
    else:
        form = MyForm()
    return render(request, 'display.html', {'form': form})


# @receiver(post_save,sender=Employee)
# def update_es(sender,instance,created,**kwargs):
#     print('update_es called')
#     if es_client.ping():
#         instance.indexing()
#         instance.delete()
#     else:
#         print('Elastic Search not available')
#
# post_save.connect(update_es, sender=Employee)
# print('update_es connected to post_save signal')










