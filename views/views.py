from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from django.core.mail import BadHeaderError, send_mail

from Garage.models import Car, CarPhoto
from Garage.forms import UploadCarPhoto
from django.shortcuts import get_object_or_404
from Garage.settings import EMAIL_HOST_USER


def main_view(request):
    return render(request, 'Garage/main.html')


def about(request):
    return render(request, 'Garage/about_us.html')


def add_image_to_model(request, car):
    try:
        image = request.FILES['image']
    except MultiValueDictKeyError:
        image = '/Users/olga/projects/Garage/user_data/default.png'
    car_photo = CarPhoto(
        image=image,
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
            return redirect(f'/car/{car.id}')
    else:
        form = UploadCarPhoto()
    context = {'form': form,
               'car': car}
    return render(request, 'Garage/upload_car_image.html', context)


def get_car_image(car_id):
    try:
        car_image = CarPhoto.objects.get(car_id=car_id)
    except CarPhoto.DoesNotExist:
        car_image = None
    return car_image


def contacts(request):
    if request.method == "POST":
        message = send_email(request)
        return render(request, 'Garage/contacts.html', {'message': message})
    else:
        return render(request, 'Garage/contacts.html')


def send_email(request):
    name = request.POST.get('name', '')
    subj = request.POST.get('subject', '')
    subject = f"{name} {subj}"
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [EMAIL_HOST_USER])
            message = 'Ваш запрос успешно отправлен'
            return message
        except BadHeaderError:
            error_message = 'Найден некорректный заголовок'
            return error_message
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        error_message = 'Убедитесь, что все поля формы заполнены'
        return error_message
