from django.shortcuts import render, redirect
from .forms import *
import requests
from youtubesearchpython import VideosSearch
import wikipedia
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic

def home(request):
    return render(request, 'learnapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username}!')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request,'learnapp/register.html',context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished = False, user = request.user)
    todos = Todo.objects.filter(is_finished = False, user = request.user)
    homeworks_done = True if len(homeworks) == 0 else False
    todos_done = True if len(todos) == 0 else False
    context = {'homeworks': zip(homeworks,range(1,len(homeworks)+1)),
    'todos': zip(todos,range(1,len(todos)+1)),
    'homeworks_done': homeworks_done,
    'todos_done': todos_done}
    return render(request,'learnapp/profile.html',context)

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user = request.user, title = request.POST['title'], description = request.POST['description'])
            notes.save()
            messages.success(request,f'Notes Added from {request.user.username}!')
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user = request.user)
    context = {'form': form, 'notes':notes}
    return render(request,'learnapp/notes.html',context)

@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                finished = True if finished == 'on' else False
            except:
                finished = False
        homeworks = Homework(user = request.user, subject = request.POST['subject'],
        title = request.POST['title'], description = request.POST['description'],
        due = request.POST['due'], is_finished = finished)
        homeworks.save()
        messages.success(request,f'Homework Added from {request.user.username}!')
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user = request.user)
    homeworks_done = True if len(homeworks) == 0 else False
    context = {'form':form, 'homeworks': zip(homeworks, range(1,len(homeworks)+1)), 'homeworks_done': homeworks_done}
    return render(request,'learnapp/homework.html',context)

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                finished = True if finished == 'on' else 'False'
            except:
                finished = False
            todos = Todo(user = request.user, title = request.POST['title'], is_finished = finished)
            todos.save()
            messages.success(request,f'Todo Added from {request.user.username}!')
    else:
        form = TodoForm()
    todos = Todo.objects.filter(user = request.user)
    todos_done = True if len(todos)==0 else False
    context = {'form':form, 'todos':zip(todos,range(1,len(todos)+1)), 'todos_done':todos_done}
    return render(request,'learnapp/todo.html',context)

# eg. for https://api.dictionaryapi.dev/api/v2/entries/en_US/apple
# [{"word":"apple",
# "phonetic":"ˈap(ə)l",
# "phonetics":[{"text":"ˈap(ə)l","audio":"//ssl.gstatic.com/dictionary/static/sounds/20200429/apple--_gb_1.mp3"}],
# "origin":"Old English æppel, of Germanic origin; related to Dutch appel and German Apfel .",
# "meanings":[{"partOfSpeech":"noun",
# "definitions":[{"definition":"the round fruit of a tree of the rose family, which typically
# has thin green or red skin and crisp flesh.","synonyms":[],"antonyms":[]},
# {"definition":"the tree bearing apples, with hard pale timber that is used in carpentry
# and to smoke food.","synonyms":[],"antonyms":[]}]}]}]

def dictionary(request):
    if request.method == 'POST':
        txt = request.POST['text']
        form = DashboardForm(request.POST)
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+txt
        answer = requests.get(url).json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {'form':form,'input':txt,'phonetics':phonetics,'audio':audio,
            'definition':definition, 'example':example, 'synonyms':synonyms}
        except:
            context = {'form':form, 'input': ''}
        return render(request,'learnapp/dictionary.html',context)
    else:
        form = DashboardForm()
    return render(request, 'learnapp/dictionary.html', {'form': form})

def wiki(request):
    if request.method == 'POST':
        txt = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(txt)
        context = {'form':form, 'title': search.title, 'link': search.url, 'details': search.summary}
        return render(request,'learnapp/wiki.html',context)
    else:
        form = DashboardForm()
    return render(request,'learnapp/wiki.html', {'form': form})

def youtube(request):
    if request.method == 'POST':
        txt = request.POST['text']
        form = DashboardForm(request.POST)
        videos = VideosSearch(txt, limit = 5)
        result_list = []
        print(videos.result())
        for v in videos.result()['result']:
            result_dict = {'input':txt, 'title': v['title'], 'duration': v['duration'], 'thumbnail': v['thumbnails'][0]['url'],
            'channel': v['channel']['name'],'link': v['link'],'views': v['viewCount']['short'],'published': v['publishedTime']}
            descript = ''
            for j in v['descriptionSnippet']:
                descript += j['text']
            result_dict['descriptionSnippet'] = descript
            result_list.append(result_dict)
        context = {'form': form, 'results': result_list}
        return render(request,'learnapp/youtube.html',context)
    else:
        form = DashboardForm()
    return render(request,'learnapp/youtube.html',{'form': form})


def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            next_form = ConversionLengthForm()
            context = {'form': form, 'm_form': next_form, 'input': True}
            if 'input' in request.POST:
                m1 = request.POST['measure1']
                m2 = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    answer = f'{input} yard = {int(input)*3} foot' if m1=='yard' and m2 == 'foot' else f'{input} foot = {int(input)/3} yard'
                context = {'form': form, 'm_form': next_form, 'input': True, 'answer': answer}

        if request.POST['measurement'] == 'mass':
            next_form = ConversionMassForm()
            context = {'form': form, 'm_form': next_form, 'input': True}
            if 'input' in request.POST:
                m1 = request.POST['measure1']
                m2 = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    answer = f'{input} pound = {int(input)*0.453592} kilogram' if m1=='pound' and m2 == 'kilogram' else f'{input} kilogram = {int(input)/0.453592} pound'
                context = {'form': form, 'm_form': next_form, 'input': True, 'answer': answer}
    else:
        form = ConversionForm()
        context = {'form': form, 'input': False}
    return render(request,'learnapp/conversion.html',context)

def books(request):
    if request.method == 'POST':
        txt = request.POST['text']
        form = DashboardForm(request.POST)
        url = "https://www.googleapis.com/books/v1/volumes?q="+txt
        answer = requests.get(url).json()
        result_list = []
        # get top 10 item
        for i in range(10):
            ans = answer['items'][i]['volumeInfo']
            result_dict = {'title': ans.get('title'), 'subtitle': ans.get('subtitle'),
            'description': ans.get('description'),'count': ans.get('pagecount'),
            'categories': ans.get('categories'), 'rating': ans.get('averageRating'),
            'thumbnail': ans.get('imageLinks').get('thumbnail')}
            result_list.append(result_dict)
        context = {'form': form, 'results': result_list}
        return render(request,'learnapp/books.html',context)
    else:
        form = DashboardForm()
        return render(request,'learnapp/books.html',{'form':form})


def delete_homework(request, pk = None):
    Homework.objects.get(id = pk).delete()
    if 'profile' in request.META['HTTP_REFERER']:
        return redirect('profile')
    return redirect('homework')

def delete_note(request, pk = None):
    Notes.objects.get(id = pk).delete()
    return redirect('notes')

def delete_todo(request, pk = None):
    Todo.objects.get(id = pk).delete()
    if 'profile' in request.META['HTTP_REFERER']:
        return redirect('profile')
    return redirect('todo')

def update_homework(request, pk = None):
    homework = Homework.objects.get(id = pk)
    homework.is_finished = True if homework.is_finished == False else False
    homework.save()
    if 'profile' in request.META['HTTP_REFERER']:
        return redirect('profile')
    return redirect('homework')

def update_todo(request, pk = None):
    todo = Todo.objects.get(id = pk)
    todo.is_finished = True if todo.is_finished == False else False
    todo.save()
    if 'profile' in request.META['HTTP_REFERER']:
        return redirect('profile')
    return redirect('todo')

class NotesDetailView(generic.DetailView):
    model = Notes
