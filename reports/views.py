import datetime
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Message, Station
from .forms import MessageForm


def is_observer(user):
    return user.groups.filter(name="observer").exists()


def is_operator(user):
    return user.groups.filter(name="operator").exists()


@login_required
@user_passes_test(is_observer)
def submit_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.observer = request.user
            # ensure station is assigned to this observer
            if msg.station not in request.user.stations.all():
                form.add_error("station", "You are not assigned to this station.")
            else:
                msg.save()
                return redirect("my_messages")
    else:
        form = MessageForm()
        form.fields["station"].queryset = request.user.stations.all()
    return render(
        request,
        "reports/submit_message.html",
        {
            "form": form,
            "is_operator": is_operator(request.user),
            "is_observer": is_observer(request.user),
        },
    )


@login_required
@user_passes_test(is_operator)
def monitor_messages(request):
    # Get ?date=YYYY-MM-DD from query string
    date_str = request.GET.get("date")
    if date_str:
        try:
            selected_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            selected_date = now().date()  # fallback if invalid
    else:
        selected_date = now().date()

    # Filter messages for the selected day
    messages = Message.objects.filter(
        created_at__date=selected_date
    ).order_by("-created_at")

    return render(
        request,
        "reports/monitor_messages.html",
        {
            "messages": messages,
            "selected_date": selected_date,
            "is_operator": is_operator(request.user),
            "is_observer": is_observer(request.user),
        },
    )


@login_required
def my_messages(request):
    messages = Message.objects.filter(observer=request.user)
    return render(
        request,
        "reports/my_messages.html",
        {
            "messages": messages,
            "is_operator": is_operator(request.user),
            "is_observer": is_observer(request.user),
        },
    )
