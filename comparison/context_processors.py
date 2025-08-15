from .comparison import Comparison

def comparison(request):
    """
    Делает объект Comparison доступным во всех шаблонах.
    """
    return {'comparison': Comparison(request)}