from django.shortcuts import render, redirect
from Garage.models import Car, CarPhoto
from Garage.forms import UploadCarPhoto
from django.shortcuts import get_object_or_404


def main_view(request):
    return render(request, 'Garage/main.html')


def about(request):
    return render(request, 'Garage/about_us.html')


def add_image_to_model(request, car):
    car_photo = CarPhoto(
        image=request.FILES['image'],
        car=car
    )
    return car_photo


def upload_photo(request, car_id):
    car = get_object_or_404(Car, id=car_id, user_id=request.user.id)
    if request.method == 'POST':
        form = UploadCarPhoto(request.POST, request.FILES)
        if form.is_valid():
            try:
                car_photo = CarPhoto.objects.get(car_id=car_id)
                car_photo.delete()
                car_photo = add_image_to_model(request, car)
            except CarPhoto.DoesNotExist:
                car_photo = add_image_to_model(request, car)
            car_photo.save()
            return redirect(f'car/{{car.id}}/')
    else:
        form = UploadCarPhoto()
    context = {'form': form,
               'car': car}
    return render(request, 'Garage/upload_car_image.html', context)
