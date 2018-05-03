from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from  django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'index.html')
@login_required
def topics(request):
    topics=Topic.objects.filter(ower=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,'topics.html',context)
@login_required
def topic(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.ower!=request.user:
        raise Http404
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'topic.html',context)
@login_required
def new_topic(request):
    if request.method!='POST':
        form=TopicForm()
    else:
        form =TopicForm(request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.ower=request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs：topics'))
    context={'form':form}
    return render(request,'new_topic.html',context)
@login_required
def new_entry(request,entry_id):
    entry=Topic.objects.get(id=entry_id)
    topic=entry.topic
    if topic.ower!=request.user:
        raise Http404
    if request.method!='POST':
        form=EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learing_logs:topic',args=[topic_id]))
    context={'topic':topic,'form':form}
    return render(request,'new_entry.html',context)
@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if request.method!='POST':
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learing_logs:topic',args=[topic.id]))
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'edit_entry.html',context)


