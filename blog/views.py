from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .forms import BlogNoteForm
from .models import BlogNote
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.conf import settings


class BlogListView(LoginRequiredMixin, ListView):
    model = BlogNote
    context_object_name = "blog_note"

    def get_queryset(self, **kwargs):
        queryset = BlogNote.objects.filter(is_published=True)

        return queryset


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogNote
    form_class = BlogNoteForm
    success_url = reverse_lazy("blog:blog_list")

    def form_valid(self, form):
        user = self.request.user
        blog_note = form.save(commit=False)
        blog_note.owner = user
        blog_note.save()

        return super().form_valid(form)


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


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogNote

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context

    def get_success_url(self):
        success_url = reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})

        return success_url

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return BlogNoteForm
        else:
            raise PermissionDenied


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogNote
    success_url = reverse_lazy("blog:blog_list")

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user != self.object.owner:
            raise PermissionDenied
        return super().get_context_data(**kwargs)


@permission_required("blog.can_unpublish_blog_note", raise_exception=True)
def drop_blog_note(request, pk):
    blog_note = get_object_or_404(BlogNote, pk=pk)
    blog_note.is_published = False
    blog_note.save()

    return redirect("blog:blog_list")


@login_required()
def public_blog_note(request, pk):
    blog_note = get_object_or_404(BlogNote, pk=pk)
    if request.user == blog_note.owner:
        blog_note.is_published = True
        blog_note.save()
    else:
        raise PermissionDenied

    return redirect("blog:blog_list")


class UserBlogListView(LoginRequiredMixin, ListView):
    model = BlogNote
    context_object_name = "blog_note"

    def get_queryset(self, **kwargs):
        queryset = BlogNote.objects.filter(owner=self.request.user)

        return queryset
