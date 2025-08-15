from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from .comparison import Comparison

def comparison_detail(request: HttpRequest) -> HttpResponse:
    comparison = Comparison(request)
    
    # Собираем все уникальные группы характеристик и сами характеристики
    # для построения "умной" таблицы сравнения.
    all_char_groups = {}
    all_products = list(comparison)
    
    for product in all_products:
        if product.characteristics:
            for group, chars in product.characteristics.items():
                if group not in all_char_groups:
                    all_char_groups[group] = set()
                all_char_groups[group].update(chars.keys())
                
    # Сортируем ключи для стабильного отображения
    for group in all_char_groups:
        all_char_groups[group] = sorted(list(all_char_groups[group]))

    return render(request, 'comparison/detail.html', {
        'comparison': comparison,
        'products': all_products,
        'all_char_groups': all_char_groups,
    })

@require_POST
def comparison_clear(request: HttpRequest) -> HttpResponse:
    """
    Очищает список сравнения.
    """
    comparison = Comparison(request)
    comparison.clear()
    return redirect('comparison:comparison_detail')