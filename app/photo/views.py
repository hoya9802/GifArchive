from typing import Any
from .forms import PostSearchForm, GifUpdateForm, GifArchiveForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Q, Count
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from photo.models import GifArchive, Like, Category
from customauth.models import MyUser, Subscriber
from django.conf import settings

class GifArchiveLV(LoginRequiredMixin, ListView):
    model = GifArchive
    login_url = "customauth:login"

class GifArchiveDV(LoginRequiredMixin, DetailView):
    model = GifArchive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        current_date = timezone.now().date()
        days_difference = (current_date - obj.create_dt).days
        context["df"] = (days_difference)
        context['like'] = Like.objects.filter(gif=obj).count()
        print(context)
        # add DISQUS
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.pk}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.name}"
        return context
    
    def post(self, request, *args, **kwargs):
        liker = request.user
        gif = self.get_object()

        check = Like.objects.filter(liker=liker, gif=gif)
        if check:
            # Delete Record if like is already existed 
            check.delete()
            messages.success(request, 'You have unliked this GIF.')
        else:
            # Add Record if like is not existed
            Like.objects.create(liker=liker, gif=gif)
            messages.success(request, 'You liked this GIF!')
        
        return redirect('photo:photo_detail', pk=gif.pk)
    
class LikeLV(LoginRequiredMixin, ListView):
    model = Like
    template_name = 'photo/liked_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        '''
        It is a function that optimizes performance by pre-loading foreign keys or objects
        with one-to-one relationships to reduce the number of queries.
        '''
        return Like.objects.filter(liker=self.request.user).select_related('gif')

class SearchFormView(LoginRequiredMixin, FormView):
    form_class = PostSearchForm
    template_name = 'photo/GifArchive_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']

        gif_list = GifArchive.objects.filter(
            Q(name__icontains=searchWord) |
            Q(owner__nick_name__icontains=searchWord)
        ).distinct()

        owners_list = MyUser.objects.all()
        owner_list = []
        for i in owners_list:
            if len(i.nick_name) == len(searchWord) and i.nick_name == searchWord:
                owner_list.append(i)
        sub_count = -1
        for owner in owner_list:
            # 각 owner에 대해 Subscriber 테이블에서 구독자 수를 카운트
            sub_count = Subscriber.objects.filter(following__user_id=owner).count()

        context = {
            'serach_term': searchWord,
            'object_list': gif_list,
            'owner_list': owner_list,
            'sub_count': sub_count,
        }
        
        return render(self.request, self.template_name, context)
    
class SubGifArchiveLV(LoginRequiredMixin, ListView):
    model = GifArchive
    template_name = 'photo/sub_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        current_user = self.request.user

        following_profiles = Subscriber.objects.filter(current_user=current_user).values_list('following', flat=True)

        return GifArchive.objects.filter(owner__in=following_profiles)
    
class ManagementLV(LoginRequiredMixin, ListView):
    model = GifArchive
    template_name = 'photo/GifArchive_management.html'

    def get_queryset(self) -> QuerySet[Any]:
        return GifArchive.objects.filter(owner=self.request.user).annotate(like_count=Count('like')).order_by('-like_count')
    
class GifArchiveDelV(LoginRequiredMixin, DeleteView):
    model = GifArchive
    success_url = reverse_lazy('photo:management')

class GifArchiveUV(LoginRequiredMixin, UpdateView):
    model = GifArchive
    template_name = 'photo/GifArchive_update.html'
    form_class = GifUpdateForm
    
    def get_success_url(self) -> str:
        print(self.object)
        return reverse_lazy('photo:photo_detail', kwargs={'pk': self.object.pk})
    
class CategoryGifArchiveLV(LoginRequiredMixin, ListView):
    model = GifArchive
    template_name = 'photo/GifArchive_category_list.html'
    context_object_name = 'gif_list'

    def get_queryset(self) -> QuerySet[Any]:
        category_name = self.kwargs.get('category_name')
        category = get_object_or_404(Category, name=category_name)
        print(category)
        return GifArchive.objects.filter(category=category)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.kwargs.get('category_name')
        return context

class GifArchiveCV(CreateView):
    model = GifArchive
    form_class = GifArchiveForm  # Use a form to customize fields and widgets if necessary
    template_name = 'photo/GifArchive_create.html'  # Your HTML file name
    success_url = reverse_lazy('photo:index')  # Redirect after successful submission

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Set the current user as the owner
        return super().form_valid(form)