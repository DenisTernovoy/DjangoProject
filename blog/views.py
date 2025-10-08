from django.urls import reverse_lazy

from .models import BlogNote
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class BlogListView(ListView):
    model = BlogNote
    context_object_name = "blog_note"

    def get_queryset(self, **kwargs):
        queryset = BlogNote.objects.filter(is_published=True)

        return queryset


class BlogCreateView(CreateView):
    model = BlogNote
    fields = ("title", "content", "preview")
    success_url = reverse_lazy("blog:blog_list")


class BlogDetailView(DetailView):
    model = BlogNote

    def get_object(self, **kwargs):
        note = super().get_object(**kwargs)
        note.views_counter += 1
        note.save()

        return note


class BlogUpdateView(UpdateView):
    model = BlogNote
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
    )

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
