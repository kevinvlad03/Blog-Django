import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import textwrap
from .models import Post
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
font_path = os.path.join(BASE_DIR, 'blog/static/fonts/DejaVuSans.ttf')

pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))


# Create your views here.
def post_list(request):
    query = request.GET.get('q')  
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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
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
    post = Post.objects.get(pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{post.title}.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setTitle(post.title)

    # Font și logo
    pdf.setFont("DejaVuSans", 12)
    logo_path = settings.BASE_DIR / 'blog/static/blog/logo.png'
    logo = ImageReader(logo_path)
    pdf.drawImage(logo, 50, 750, width=100, height=50)

    # Titlu
    pdf.setFont("DejaVuSans", 16)
    pdf.drawString(100, 700, post.title)

     # Adaugă imaginea articolului, dacă există
    if post.image:
        image_path = settings.MEDIA_ROOT / post.image.name  # Obține calea completă a imaginii
        try:
            pdf.drawImage(ImageReader(image_path), 50, 200, width=500, height=300)  # Poziționează imaginea
        except Exception as e:
            pdf.drawString(50, 500, "Imaginea nu a putut fi încărcată.")

    # Conținut împărțit în linii multiple
    content = post.content
    text_object = pdf.beginText(30, 650)  # Poziția inițială pentru text
    text_object.setFont("DejaVuSans", 10)

    # Împarte textul în linii pentru o lățime specifică
    wrapped_text = textwrap.wrap(content, width=110)  # Ajustează `width` după cum este nevoie
    for line in wrapped_text:
        text_object.textLine(line)

    pdf.drawText(text_object)
    pdf.showPage()
    pdf.save()

    return response
