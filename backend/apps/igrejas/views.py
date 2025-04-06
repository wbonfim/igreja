from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Igreja

def index(request):
    """
    Redireciona para o site da igreja principal
    """
    igreja = Igreja.objects.first()
    if igreja:
        return redirect('igrejas:igreja_site', igreja_id=igreja.id)
    return render(request, 'igrejas/sem_igreja.html')

def igreja_site(request, igreja_id):
    """
    Renderiza o site da igreja usando o template selecionado
    """
    igreja = get_object_or_404(Igreja, id=igreja_id)

    # Se a igreja tem um template personalizado, use-o
    if igreja.template:
        return render(request, 'base_igreja.html', {
            'igreja': igreja
        })

    # Caso contrário, use o template padrão
    return render(request, 'igrejas/padrao.html', {
        'igreja': igreja
    })

@login_required
def admin_igreja(request, igreja_id):
    """
    Página de administração da igreja
    """
    igreja = get_object_or_404(Igreja, id=igreja_id)
    return render(request, 'igrejas/admin.html', {
        'igreja': igreja
    })
