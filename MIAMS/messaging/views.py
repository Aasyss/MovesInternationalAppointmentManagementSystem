from django.shortcuts import render, redirect
from messaging.models import Message
from userregistration.models import UserProfile

def send_message(request):
    if request.method == 'POST':
        sender = UserProfile.objects.get(user=request.user)
        recipient_id = request.POST.get('recipient')
        recipient = UserProfile.objects.get(id=recipient_id)
        content = request.POST.get('content')

        Message.objects.create(sender=sender, recipient=recipient, content=content)
        return redirect('message_history')

    # Provide a list of users for message recipient selection
    users = UserProfile.objects.exclude(user=request.user)
    return render(request, 'messaging/send_message.html', {'users': users})

def message_history(request):
    user = UserProfile.objects.get(user=request.user)
    messages = Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)
    messages = messages.order_by('timestamp')

    context = {
        'messages': messages,
    }
    return render(request, 'messaging/message_history.html', context)
