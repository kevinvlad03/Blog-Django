from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import Post

# Create your views here.
def post_list(request):
    query = request.GET.get('q')  # Preluăm termenul de căutare din query string
    if query:
        posts = Post.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts, 'query': query})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def contact(request):
    return render(request, 'blog/contact.html')

def export_post_pdf(request, pk):
    # Obținem articolul curent
    post = Post.objects.get(pk=pk)

    # Configurăm răspunsul HTTP ca un fișier PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{post.title}.pdf"'

    # Generăm PDF-ul
    pdf = canvas.Canvas(response)
    pdf.setTitle(post.title)

    # Adăugăm logo-ul
    logo_path = settings.BASE_DIR / 'blog/static/blog/logo.png'  # Calea absolută către logo
    logo = ImageReader(logo_path)
    pdf.drawImage(logo, 50, 750, width=100, height=50)  # Poziția și dimensiunea logo-ului

    # Adăugăm titlul articolului
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 700, post.title)

    # Adăugăm conținutul articolului
    pdf.setFont("Helvetica", 12)
    text = pdf.beginText(50, 650)
    text.textLines(post.content)

    pdf.drawText(text)
    pdf.showPage()
    pdf.save()

    return response
