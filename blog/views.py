from django.urls import reverse_lazy

from .forms import BlogNoteForm
from .models import BlogNote
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.conf import settings


class BlogListView(ListView):
    model = BlogNote
    context_object_name = "blog_note"

    def get_queryset(self, **kwargs):
        queryset = BlogNote.objects.filter(is_published=True)

        return queryset


class BlogCreateView(CreateView):
    model = BlogNote
    form_class = BlogNoteForm
    success_url = reverse_lazy("blog:blog_list")


class BlogDetailView(DetailView):
    model = BlogNote

    def get_object(self, **kwargs):
        note = super().get_object(**kwargs)
        note.views_counter += 1
        note.save()

        if note.views_counter == 100:
            subject = "Достижение!"
            message = (
                f'Поздравляю. Объект с именем "{note.title}" посмотрели 100 раз!!!'
            )
            recipient_list = ["denis.ternovoi1@mail.ru"]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )

        return note


class BlogUpdateView(UpdateView):
    model = BlogNote
    form_class = BlogNoteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context

    def get_success_url(self):
        success_url = reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})

        return success_url


class BlogDeleteView(DeleteView):
    model = BlogNote
    success_url = reverse_lazy("blog:blog_list")
