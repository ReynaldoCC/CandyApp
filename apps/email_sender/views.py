from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import ContactForm, EmailForm
from django.core.exceptions import ValidationError


# Create your views here.
def contactview(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Mensaje enviado desde app"
            message = form.cleaned_data.get('message')
            from_email = form.cleaned_data.get('email')
            email = EmailMessage(subject=subject, body=message, to=["gestor_ventas@byt.lan"], from_email=from_email)
            email.send(fail_silently=False)
            success = "su mensage ha sido enviado"
            form = ContactForm()
            return render(request, 'email_sender/contact.html', {'form': form, 'success': success})
        else:
            return render(request, 'email_sender/contact.html', {'form': form, 'success': None})
    else:
        return render(request, 'email_sender/contact.html', {'form': form, 'success': None})


def emailview(request):
    form = EmailForm()
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data.get("recipients_email")
            body = form.cleaned_data.get("body_email")
            from_e = form.cleaned_data.get("from_email")
            cc = form.cleaned_data.get("cc_email")
            bcc = form.cleaned_data.get("bcc_email")
            subject = form.cleaned_data.get("subject_email")
            mail = EmailMessage(subject=subject, body=body, from_email=from_e, cc=cc, bcc=bcc, to=recipient)
            email.send(fail_silently=False)
            success = "su mensage ha sido enviado"
            form = ContactForm()
            return render(request, 'email_sender/email_send.html', {'form': form, 'success': success})
        else:
            return render(request, 'email_sender/email_send.html', {'form': form, 'success': None})
    else:
        return render(request, 'email_sender/email_send.html', {'form': form, 'success': None})

