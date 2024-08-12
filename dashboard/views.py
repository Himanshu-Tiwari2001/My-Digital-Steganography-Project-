from django.shortcuts import render,redirect
from django.views import View
from .forms import ImageForm
from .models import Image
from otp.models import CustomUser
# Create
# from django.shortcuts import render, redirect
from .forms import ImageForm



def dashboard(request):
    user = request.user
    user_details = CustomUser.objects.get(user=user)
    profile_image_form = ImageForm()

    if request.method == 'POST':
        profile_image_form = ImageForm(request.POST, request.FILES)
        if profile_image_form.is_valid():
            profile_image = profile_image_form.save(commit=False)
            profile_image.user = user
            profile_image.save()
            return redirect('dashboard')

    # try:
    #     profile_image = UserProfileImage.objects.get(user=user)
    # except UserProfileImage.DoesNotExist:
    #     profile_image = None

    return render(request, 'dashboard.html', {'user_details': user_details, 'profile_image': profile_image, 'profile_image_form': profile_image_form})

# class DashboardView(View):
#     def get(self, request, pk=None):
#         form = ImageForm()
#         img = Image.objects.all()
#         user = None
#         if pk is not None:
#             user = CustomUser.objects.get(pk=pk)
#         return render(request, 'dashboard.html', {'img': img, 'form': form, 'user': user})

#     def post(self, request, pk=None):
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('userprofile')
#         else:
#             # Handle form errors here, if any
#             # You can add error messages to the context and render the template with errors
#             pass
# class DashboardView(View):
#     def get(self, request, pk=None):
#         form = ImageForm()
#         img = Image.objects.all()
#         if pk is not None:
#             candidate = CustomUser.objects.get(pk=pk)
#             return render(request, 'dashboard.html', {'candidate': candidate, 'img': img, 'form': form})
#         else:
#             return render(request, 'dashboard.html', {'img': img, 'form': form})

#     def post(self, request, pk=None):
#         if request.method == "POST":
#             form = ImageForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#         return redirect('userprofile')  # Redirect to the same page after form submission

