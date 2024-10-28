from photo.models import GifArchive
from .models import MyUser, Profile, Subscriber
from django.views import View
from django.http import HttpResponse
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import login
from customauth.forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm

class RegisterView(FormView):
    template_name="registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('customauth:register_done')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class VerifyEmailView(View):
    def get(self, request, user_id):
        user = get_object_or_404(MyUser, id=user_id)
        user.email_verified = True
        user.save()
        return HttpResponse("Email verified successfully!")

class VerifyEmailView(View):
    def get(self, request, user_id):
        user = get_object_or_404(MyUser, id=user_id)
        user.email_verified = True
        user.save()
        return HttpResponse("Email verified successfully!")

class CustomLoginView(LoginView):
    success_url = reverse_lazy('photo:index')

    def get_success_url(self):
        print('redirecting to:', self.success_url)
        return self.success_url

class RegisterDoneView(TemplateView):
    template_name = "registration/register_done.html"

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

class CustomChangeView(UpdateView):
    model = MyUser
    form_class = UserUpdateForm
    template_name = 'registration/change_info.html'
    success_url = reverse_lazy('photo:index')

    def get_object(self):
        return self.request.user

class MyProfileDV(DetailView):
    model = Profile
    template_name = 'registration/my_profile.html'
    
    def get_object(self):
        nickname = self.kwargs['nickname']
        user = get_object_or_404(MyUser, nick_name=nickname)
        return get_object_or_404(Profile, user_id = user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(type(context["object"]))
        # print(type(self.object.user_id))
        # 주석 처리된 코드는 Profile의 객체이기 때문에 오류 발생
        # context['gif_list'] = GifArchive.objects.filter(owner = context["object"])
        context['gif_list'] = GifArchive.objects.filter(owner = self.object.user_id)
        context['sub'] = Subscriber.objects.filter(following=kwargs['object']).count()
        try: 
            if Subscriber.objects.get(current_user=self.request.user, following=kwargs['object']):
                context['sub_check'] = True
        except:
            context['sub_check'] = False
        
        return context

    def post(self, request, *args, **kwargs):
        current_user = request.user
        following = self.get_object()

        check = Subscriber.objects.filter(current_user=current_user, following=following)
        if check:   check.delete()
        else:       Subscriber.objects.create(current_user=current_user, following=following)

        return redirect('customauth:my_profile', nickname=kwargs['nickname'])

class UpdateProfile(UpdateView):
    model = Profile
    template_name = 'registration/update_profile.html'
    form_class = ProfileUpdateForm

    def get_object(self):
        nickname = self.kwargs.get('nickname')
        user = get_object_or_404(MyUser, nick_name=nickname)
        return user.profile

    def form_valid(self, form):
        # Get the existing profile image before the form is saved
        old_profile_image = self.get_object().profile_image

        # Check if profile_image is in FILES
        if 'profile_image' in self.request.FILES:
            # Set the new profile iamge
            form.instance.profile_image = self.request.FILES['profile_image']

            # Delete the old profile image if it exists and is different from the new one
            if old_profile_image and old_profile_image.url != form.instance.profile_image.url:
                old_profile_image.delete(save=False)

        return super().form_valid(form)

    def get_success_url(self) -> str:
        nickname = self.kwargs.get('nickname')
        return reverse_lazy('customauth:my_profile', kwargs={"nickname": nickname})
    
class PasswordCV(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('photo:index')