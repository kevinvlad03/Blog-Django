from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import Post

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

    logo_path = settings.BASE_DIR / 'blog/static/blog/logo.png'  
    logo = ImageReader(logo_path)
    pdf.drawImage(logo, 50, 750, width=100, height=50)  

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, 700, post.title)

    pdf.setFont("Helvetica", 12)
    text = pdf.beginText(50, 650)
    text.textLines(post.content)

    pdf.drawText(text)
    pdf.showPage()
    pdf.save()

    return response
