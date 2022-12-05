

from statistics import quantiles
from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView
import questions
from questions.forms import AnswerForm, QuestionForm, RegistrationForm,LoginForm,AnswerForm
from django.views.generic import CreateView,FormView,ListView,DetailView
from questions.models import Answers, Myuser
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from questions.models import Questions

class IndexView(CreateView,ListView):
    template_name="home.html"
    form_class=QuestionForm
    model=Questions
    success_url=reverse_lazy("index")
    context_object_name="questions"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user   )

class SignupView(CreateView):
    model=Myuser
    form_class=RegistrationForm
    template_name='register.html'
    success_url=reverse_lazy("register")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,self.template_name,{"form":form})
            
class QuestionDetailView(DetailView,FormView):
    model=Questions
    template_name="question-detail.html"
    pk_url_kwarg: str="id"
    context_object_name: str="question"
    form_class=AnswerForm



def add_answer(request,*args,**kw):
   form=AnswerForm(request.POST)
   if form.is_valid():
    answer=form.cleaned_data.get("answer")
    qid=kw.get("id")
    ques=Questions.objects.get(id=qid)
    Answers.objects.create(question=ques,user=request.user,answer=answer)
    #message
    return redirect("index")
   else:
    #message
    return redirect("index")

        

def upvote_view(request,*args,**kw):
    ans_id=kw.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.upvote.add(request.user)
    ans.save()
    return redirect("index")

def remove_answer(request,*args,**kw):
    ans_id=kw.get("id")
    Answers.objects.get(id=ans_id).delete()
    return redirect("index")

def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("signin")



