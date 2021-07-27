from django.shortcuts import render
from .models import Product, Category
from .utils import get_products_by_category, get_all_parents, get_category_tree
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404


def index(request):
    categories = Category.objects.filter(parent=None)
    query_search = request.GET.get('search', '')
    if query_search:
        products = Product.objects.filter(name__icontains=query_search)
    else:
        products = Product.objects.all()

    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 2)
    page = paginator.get_page(page_number)

    context = {
        'products': page.object_list,
        'page_obj': page,
        'categories': categories,
        'query_search': query_search
    }

    template = 'store/index.html'

    return render(request, template, context)


def category_detail(request, hierarchy=None):
    categories = Category.objects.filter(parent=None)
    query_search = request.GET.get('search', '')

    slug = hierarchy.split('/')[-1]
    category = get_object_or_404(Category, slug=slug)
    all_parent_categories = get_all_parents(category)

    if hierarchy.split('/') == [c.slug for c in all_parent_categories]:
        if query_search:
            products = [p for p in get_products_by_category(category) if query_search in p.name]
        else:
            products = get_products_by_category(category)

    else:
        raise Http404('Invalid url')

    page_number = request.GET.get('page', 1)
    paginator = Paginator(products, 2)
    page = paginator.get_page(page_number)

    context = {
        'products': page.object_list,
        'category': category,
        'page_obj': page,
        'all_parent_categories': all_parent_categories,
        'categories': categories,
        'query_search': query_search
    }

    template = 'store/index.html'

    return render(request, template, context)
