from .models import Category

def categories(request):
    cate_list = Category.objects.all()
    return {
        "cate_list": cate_list
    }