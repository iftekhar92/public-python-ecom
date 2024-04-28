from django.http import HttpResponse
from django.shortcuts import render, redirect
from categoryMgt.forms import CategoryForm
from categoryMgt.models import Category
from django.contrib.auth.decorators import login_required, permission_required
  
#Create your views here.

@login_required
@permission_required('categoryMgt.get_category')
def getCategory(request):
    categories = Category.objects.all()
    return render(request, "categoryMgt/list.html", {"categories":categories})

@login_required
@permission_required('categoryMgt.create')
def create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return redirect('/category/list')
    else:
        form = CategoryForm()
    return render(request, 'categoryMgt/form.html', {'form' : form, 'title': 'Create Category'})

@login_required
@permission_required('categoryMgt.update')
def update(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            form.save()
            return redirect('/category/list')

    return render(request, 'categoryMgt/form.html', {'form':form, 'title': 'Update Category'})

@login_required
@permission_required('categoryMgt.delete')
def delete(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('/category/list')

    return render(request, 'categoryMgt/confirm.html', {'category':category})

def getOurCategory(request):
    categories = Category.objects.all()
    return render(request, "categoryMgt/our-category.html", {"categories":categories})
