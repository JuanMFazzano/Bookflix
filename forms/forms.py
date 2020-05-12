import datetime
from django import forms
from django.contrib.auth.models import User
from modelos.models import Suscriptor,Tarjeta,Tipo_Suscripcion

def clean_campo(clase,atributo,longitud):
    campo = clase.cleaned_data[atributo] #Si no es un numero, esto levanta excepcion.
    if campo.isdigit(): #verifica si un string tiene unicamente digitos
        if len(campo) != longitud:
            raise forms.ValidationError("Deben ingresarse {} digitos en el campo {}".format(str(longitud),atributo))
    else:
        raise forms.ValidationError(" En {} solo debe ingresarse digitos numericos".format(atributo))
    return clase.cleaned_data[atributo]

class FormularioRegistro(forms.Form):
    def __init__(self,*args,**kwargs):
        super(FormularioRegistro,self).__init__(*args,**kwargs)

    tipo_suscripcion=[
        ('regular','Regular(2 perfiles maximo)'),
        ('premium','Premium(4 perfiles maximo)')
    ]

    DNI = forms.CharField(max_length = 8)
    Nombre = forms.CharField(max_length = 25)
    Apellido =forms.CharField(max_length = 25)
    Email = forms.EmailField(max_length = 254)
    Contrasena = forms.CharField(widget=forms.PasswordInput,max_length = 20)
    Numero_de_tarjeta = forms.CharField(max_length = 16)
    Fecha_de_vencimiento = forms.DateField(widget = forms.SelectDateWidget(years = [x for x in range(1990,2051)]))
    DNI_titular = forms.CharField(max_length = 8)
    Empresa= forms.CharField(max_length = 7)
    Codigo_de_seguridad = forms.CharField(max_length = 3)
    Suscripcion=forms.CharField(widget=forms.Select(choices=tipo_suscripcion))

    def clean_Email(self):
        email = self.cleaned_data['Email']
        if (User.objects.values('username').filter(username = email).exists()):
            raise forms.ValidationError('El Email ya esta registrado en el sistema')
        return email

    def clean_DNI(self):
        campo = clean_campo(self,'DNI',8)
        if (Suscriptor.objects.values('dni').filter(dni = campo).exists()):
            raise forms.ValidationError('El DNI ya esta registrado en el sistema')
        return campo

    def clean_DNI_titular(self):
        return clean_campo(self,'DNI_titular',8)

    def clean_Codigo_de_seguridad(self):
        return clean_campo(self,'Codigo_de_seguridad',3)

    def clean_Numero_de_tarjeta(self):
        return clean_campo(self,'Numero_de_tarjeta',16)

    def clean_Fecha_de_vencimiento(self):
        fecha_vencimiento = (self.cleaned_data['Fecha_de_vencimiento'])
        fecha_hoy = ((datetime.datetime.now()).date())
        vencida = (fecha_hoy >= fecha_vencimiento)
        if vencida:
            raise forms.ValidationError('Tarjeta vencida')
        return self.cleaned_data['Fecha_de_vencimiento']

class FormularioIniciarSesion(forms.Form):
    email = forms.EmailField(max_length=254)
    clave = forms.CharField(widget=forms.PasswordInput)

class FormularioModificarDatosPersonales(forms.Form):
    def __init__(self,*args,**kwargs):
        super(FormularioModificarDatosPersonales,self).__init__(*args,**kwargs)


    Email = forms.EmailField(max_length = 254,show_hidden_initial=True)
    DNI = forms.CharField(max_length = 8,show_hidden_initial=True)
    Nombre = forms.CharField(max_length = 25,show_hidden_initial=True)
    Apellido =forms.CharField(max_length = 25,show_hidden_initial=True)
    Numero_de_tarjeta = forms.CharField(max_length = 16,show_hidden_initial=True)
    Fecha_de_vencimiento = forms.DateField(widget = forms.SelectDateWidget(years = [x for x in range(1990,2051)]),show_hidden_initial=True)
    DNI_titular = forms.CharField(max_length = 8,show_hidden_initial=True)
    Empresa= forms.CharField(max_length = 7,show_hidden_initial=True)
    Codigo_de_seguridad = forms.CharField(max_length = 3,show_hidden_initial=True)
    Suscripcion=forms.CharField(disabled = True,show_hidden_initial=True)

# [X] Validar DNI que no exista en otras tuplas
# [X] Validar Email que no exista en otras tuplas
# [] Que la tarjeta ingresada no exista en otras tuplas para no volver a crearla
    def __cambio(self,valor_inicial,valor_nuevo):
        return valor_inicial != valor_nuevo

    def clean_Email(self):
        field_email = self.visible_fields()[0] #Me devuelve una instancia del EmailField --> campo Email
        valor_email_inicial = field_email.initial
        valor_email_actual = self.cleaned_data['Email']
        if  self.__cambio(valor_email_inicial,valor_email_actual):
            if (User.objects.values('username').filter(username = valor_email_actual).exists()):
                raise forms.ValidationError('El Email ya esta registrado en el sistema')
        return valor_email_actual

    def clean_DNI(self):
        field_DNI = self.visible_fields()[1] #Me devuelve una instancia del CharField --> campo DNI
        valor_dni_inicial = field_DNI.initial
        valor_dni_actual = self.cleaned_data['DNI']
        if self.__cambio(valor_dni_inicial,valor_dni_actual):
            clean_campo(self,'DNI',8)
            if (Suscriptor.objects.values('dni').filter(dni = valor_dni_actual).exists()):
                raise forms.ValidationError('El DNI ya esta registrado en el sistema')
        return valor_dni_actual

    def clean_DNI_titular(self):
        return clean_campo(self,'DNI_titular',8)

    def clean_Codigo_de_seguridad(self):
        return clean_campo(self,'Codigo_de_seguridad',3)

    def clean_Numero_de_tarjeta(self):
        return clean_campo(self,'Numero_de_tarjeta',16)

    def clean_Fecha_de_vencimiento(self):
        fecha_vencimiento = (self.cleaned_data['Fecha_de_vencimiento'])
        fecha_hoy = ((datetime.datetime.now()).date())
        vencida = (fecha_hoy >= fecha_vencimiento)
        if vencida:
            raise forms.ValidationError('Tarjeta vencida')
        return self.cleaned_data['Fecha_de_vencimiento']
