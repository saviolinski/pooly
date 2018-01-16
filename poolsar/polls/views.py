from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import Q

from .forms import QuestionForm, ChoiceForm
from .models import Question, Choice, Voted
from django.contrib.auth import get_user_model

User = get_user_model

def get_chart(request):
    data = {
        'labels': [],
        'default': []
    }

    question_list = Question.objects.order_by('-timestamp')

    for question in question_list:
        labels = "labelsof{}".format(question.question_text)
        votes = "votesof{}".format(question.question_text)
        items = {}
        items[labels] = []
        items[votes] = []
        for answer in question.choice_set.order_by('-votes').all():
            items[labels].append(answer.choice_text)
        for answer in question.choice_set.order_by('-votes').all():
            votes_count = answer.voted_set.count()
            items[votes].append(votes_count)
        taglab = "labels{}".format(question.id)
        tagdef = "default{}".format(question.id)
        data[taglab] = items[labels]
        data[tagdef] = items[votes]


    return JsonResponse(data)


@login_required
def vote(request, slug):
    # if not request.user.is_authenticated():
    #     raise Http404

    question = get_object_or_404(Question, slug=slug)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])

        # for choices in question.choice_set.all():
        #     if request.user in question.voters:
        #         raise Http404("You have already voted")
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        choice_vote = Voted(user=request.user, choice=selected_choice)
        choice_vote.save()
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:detail', args=(question.slug,)))


@login_required
def add_choice(request, slug):
    obj = get_object_or_404(Question, slug=slug)
    try:
        choice_text = request.POST["choicetext"]
        new_choice = Choice(question=obj, choice_text=choice_text, user=request.user)
        new_choice.save()

    except (KeyError, Question.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': obj,
            'error_message': "Question does not exists.",
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:detail', args=(obj.slug,)))


def polls_index(request):
    question_list = Question.objects.order_by('-timestamp')
    query = request.GET.get("q")
    if query:
        question_list = Question.objects.filter(
                Q(question_text__icontains=query) |
                Q(choice__choice_text__icontains=query)
            ).distinct()
    title = "Pollsar"
    context = {
        'latest_question_list': question_list,
        'title': title
    }
    return render(request, "list_view.html", context)


def polls_detail(request, slug):
    obj = get_object_or_404(Question, slug=slug)
    choiceset = obj.choice_set.order_by('-votes').all()
    if request.user.is_authenticated():
        user_asked = obj.choice_set.filter(user=request.user)
        user_voted = False
        for choice in choiceset:
            if choice.voted_set.filter(user=request.user):
                user_voted = True
    else:
        user_voted = False
        user_asked = obj

    context = {
        "question": obj,
        "choiceset": choiceset,
        "user_asked": user_asked,
        "user_voted": user_voted,
    }
    return render(request, "polls/detail.html", context)


def polls_results(request, slug):
    obj = get_object_or_404(Question, slug=slug)
    context = {
        "question": obj
    }
    return render(request, "polls/results.html", context)

@login_required
def polls_create(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        choice = form.cleaned_data.get('choice')
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        new_choice = Choice(question=instance, choice_text=choice)
        new_choice.save()
        instance.choice = new_choice
        instance.save()
        messages.success(request, "zrobiono")
        return HttpResponseRedirect(reverse("polls:index"))
    context = {
        "form": form,
    }
    return render(request, "polls/create.html", context)


@login_required
def polls_edit(request, slug):
    obj = get_object_or_404(Question, slug=slug)
    form = QuestionForm(request.POST or None, instance=obj)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return HttpResponseRedirect(reverse("polls:index"))
    context = {
        "question": obj,
        "form": form
    }
    return render(request, "polls/create.html", context)


@login_required
def polls_delete(request, slug):
    obj = get_object_or_404(Question, slug=slug)
    obj.delete()
    messages.success(request, "usunieto")
    return redirect("polls:index")


