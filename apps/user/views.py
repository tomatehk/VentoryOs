from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
# importamos para login y redireccionar
from django.contrib.auth import authenticate, login, logout
# autenticacion
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# importamos para crear los usuario
from django.contrib.auth.models import Permission, User
# veificar password
from django.contrib.auth.hashers import check_password
# importamos Sale para poder borrar todo el registro
from ..shopping_cart.models import Sale, Client


def active(request):
    # creamos los usuarios
    admin = User.objects.create_user('admin', 'brandomhk@gmail.com', '123456')
    work = User.objects.create_user('work', 'quiensabeluis@gmail.com', '123456')

    # guardamos los usuarios
    admin.save()
    work.save()

    # buscamos un periso y lo asignamos a admin
    permission = Permission.objects.get(codename='add_section')
    admin.user_permissions.add(permission)
    admin.save()

    return JsonResponse({"data": "heco"}, status=200)


class Login(View):
    template_name = 'user/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('default'))

        return render(request, self.template_name, {'error': ''})

    def post(self, request, *args, **kwargs):
        # obtenemos el usuario y contraseña
        user = request.POST['user']
        password = request.POST['password']
        user_login = authenticate(username=user, password=password)

        if user_login is not None:
            login(request, user_login)

            return HttpResponseRedirect(reverse('default'))
        else:
            return render(request, self.template_name,
                          {'error':
                           {'message': '¡Error contraseña invalida!',
                            'user': user}})


def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('user:login'))


class Config(PermissionRequiredMixin, LoginRequiredMixin, View):
    template_name = 'user/config.html'
    permission_required = 'section.add_section'

    def get(self, request):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Verificamos la accion que se realizara
        action = request.POST['action']
        user = request.user

        try:
            if action == 'change-password-admin' and user.username == 'admin':
                password_act = request.POST['pwd-admin']
                # comprobamos la contraseña del admin
                if check_password(password_act, user.password):
                    # obtenemos la nueva contraseña
                    new_pass = request.POST['pwd-new-admin']
                    request.user.set_password(new_pass)
                    request.user.save()

                    # volvemos a conectar el usuario porque si no la aplicacion lo sacara
                    user_login = authenticate(username=user.username, password=new_pass)

                    if user_login is not None:
                        login(request, user_login)

                    # creamos el mensaje que se realizo con satisfaccion
                    message = 'Contraseña cambiada con exito'
                else:
                    message = 'Contraseña invalida'
                    return render(request, self.template_name, {'messsage': message, 'error': True})

            elif action == 'change-password-work':
                password_act = request.POST['pwd-admin']
                # obtenemos el usuario trabajador
                user_work = User.objects.get(username='work')
                # comprobamos la contraseña del admin
                if check_password(password_act, user.password):
                    # hacemos los cambios al usuairo
                    new_pass = request.POST['pwd-new-work']
                    user_work.set_password(new_pass)
                    user_work.save()

                    # mensaje de confirmacion
                    message = 'Perfecto contraseña cambiada'
                else:
                    message = 'Error contraseña invalida'
                    return render(request, self.template_name, {'messsage': message, 'error': True})

            elif action == 'clear-registry':
                # obtenemos todas las ventas y las borramos
                Sale.objects.all().delete()
                Client.objects.all().delete()

                return JsonResponse(status=200)
        except Exception as e:
            return render(request, self.template_name, {'messsage': str(e)})

        return render(request, self.template_name, {'messsage': message})
