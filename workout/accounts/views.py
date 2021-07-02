from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import MyUser, Slot,Trainer,Member,Dietician
from django.contrib import messages
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from collections import defaultdict
import re
import razorpay

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
dict = {
			"5am-6am": "t5",
			"6am-7am": "t6",
            "7am-8am": "t7",
            "8am-9am": "t8",
            "9am-10am":"t9",
            "10am-11am": "t10",
			"11am-12noon": "t11",
			"12noon-1pm": "t12",
            "1pm-2pm": "t13",
            "2pm-3pm": "t14",
            "3pm-4pm": "t15",
            "4pm-5pm": "t16",
			"5pm-6pm": "t17",
            "6pm-7pm": "t18",
            "7pm-8pm": "t19",
            "8pm-9pm": "t20",
			"9pm-10pm": "t21",
		}
li =   {
			'5am-6am': 0,
			'6am-7am': 1,
            '7am-8am': 2,
            '8am-9am': 3,
            '9am-10am': 4,
            '10am-11am': 5,
			'11am-12noon': 6,
			'12noon-1pm': 7,
            '1pm-2pm': 8,
            '2pm-3pm': 9,
            '3pm-4pm': 10,
            '4pm-5pm': 11,
			'5pm-6pm': 12,
            '6pm-7pm': 13,
            '7pm-8pm': 14,
            '8pm-9pm': 15,
			'9pm-10pm': 16,
		}
dict_rev= {
			"t5":"5am-6am",
            "t6":"6am-7am",
            "t7":"7am-8am",
            "t8":"8am-9am",
            "t9":"9am-10am",
            "t10":"10am-11am",
            "t11":"11am-12noon",
            "t12":"12noon-1pm",
            "t13":"1pm-2pm",
            "t14":"2pm-3pm",
            "t15":"3pm-4pm",
            "t16":"4pm-5pm",
            "t17":"5pm-6pm",
            "t18":"6pm-7pm",
            "t19":"7pm-8pm",
            "t20":"8pm-9pm",
            "t21":"9pm-10pm"
}
def setTimes(available):
    time=[0]*17
    for i in available:
        print (i)
        val=li[i]
        time[val]= i
    return time

def resetTimes(val,avl,name):
    l=["0"]*17
    print(val.t5,val.t6)
    for i in li:
        idx=li[i]
        if i in avl:
            l[idx]=name
        else:
            elem=dict[i]
            print(elem)
            print(val)
    print(l)
    return l
    
def logoutUser(request):
    logout(request)
    return render(request,'registerNew.html')

def loginView(request):
    if request.method =="POST":
        username=request.POST.get('name')
        password=request.POST.get('password')
        try:
            user= MyUser.objects.get(username=username,password=password)
            if user is not None:
                login(request,user)
                print(request.user.is_trainer)
                print(request.user.is_member)
                print(request.user.is_dietician)
                if request.user.is_member:
                    print("Entered inside the profile")
                    return redirect('profile_member')
                elif(request.user.is_trainer):
                    return redirect('profile_trainer')
                elif(request.user.is_dietician):
                    print("Entered the dietician profile")
                    return redirect('profile_dietician')
        except:
            print("Incorrect")
            messages.info(request,'Username or Password is incorrect')
            return render(request,'registerNew.html')
    print("Not going inside the func")
    return render(request,'registration/login.html')
def about(request):
    return render(request,'about.html')
def profileTrainer(request):
    context={}
    return render(request,'profile_trainer.html',context)
def contact(request):
    return render(request,'contact.html')
def profileMember(request):
    return render(request,'profile_member.html')
def profileDietician(request):
    return render(request,'profile_dietician.html')
def trainer_register(request):
    '''if request.user.is_authenticated:
        return redirect('')'''
    if True:
        if request.method == 'POST':
            name = request.POST['name']
            exp = request.POST['exp']
            email = request.POST['email']
            age = request.POST['age']
            phone = request.POST['phone']
            workout = request.POST.getlist('workout')
            fees = request.POST['fees']
            available=request.POST.getlist('available')
            gender = request.POST.get('gender')
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                if(MyUser.objects.filter(username=name).exists()):
                    messages.info(request,"username already exists")
                elif(MyUser.objects.filter(email=email).exists()):
                    messages.info(request, 'Email already exists')
                else:
                    user = MyUser(
                        username=name,
                        email=email,
                        password=password1,
                        is_trainer=True,
                        is_member=False,
                        is_dietician=False,
                        age=age,
                        workout=workout,
                        gender=gender,
                        phone=phone,
                        )
                    user.save()
                    trainer=Trainer(user=user,
                        experience=exp,
                        fees=fees,
                        available=available
                        )
                    trainer.save()
                    slot=Slot(user=user)
                    l=setTimes(available)
                    print(l)
                    
                    slot=Slot(user=user,
                    t5=l[0],t6=l[1],t7=l[2],
                    t8=l[3],t9=l[4],t10=l[5],
                    t11=l[6],t12=l[7],t13=l[8],
                    t14=l[9],t15=l[10],t16=l[11],
                    t17=l[12],t18=l[13],t19=l[14],
                    t20=l[15],t21=l[16]
                    )
                    print(slot)
                    slot.save()
                    print('user saved')
                    return redirect('/')
            else:
                messages.info(request, 'Passwords not matching')
                return redirect('trainer_register')
            return redirect('/')
        else:
            return render(request,"registration/trainer_register.html")
def member_register(request):
    '''if request.user.is_authenticated:
        return redirect('frontpage')'''
    if True:
        if request.method=='POST':
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            workout=request.POST.getlist('workout')
            health=request.POST['health']
            age=request.POST['age']
            gender=request.POST.get('gender')
            password1=request.POST['password1']
            password2=request.POST['password2']
            if password1==password2:
                if MyUser.objects.filter(username=name).exists():
                    messages.info(request,"username already exists")
                elif MyUser.objects.filter(email=email).exists():
                    messages.info(request,'Email already exists')
                else:
                    user=MyUser(
                        username=name,
                        email=email,
                        password=password1,
                        is_trainer=False,
                        is_member=True,
                        is_dietician=False,
                        age=age,
                        workout=workout,
                        gender=gender,
                        phone=phone,
                        )
                    #user.password=make_password(user.password)
                    user.save()
                    member=Member(user=user,
                        health_issues=health
                        )
                    member.save()
                    print('user saved')
                    return redirect('login')
            else:
                messages.info(request,'Passwords not matching')
                return redirect('registerNew')
            return redirect('/')
        else:
            return render(request,"registration/register.html")
    
def trainer_detail(request):
    user=request.user
    trainer=Trainer.objects.get(user=user)
    context={
        'object':trainer
    }
    return render(request, "trainer_detail.html",context)

def member_detail(request):
    user=request.user
    member=Member.objects.get(user=user)
    context={
        'object':member
    }
    return render(request, "member_detail.html",context)
def dietician_detail(request):
    user=request.user
    dietician=Dietician.objects.get(user=user)
    context={
        'object':dietician
    }
    return render(request, "dietician_detail.html",context)


def edit_profile_trainer(request):
    context={}
    user=request.user
    trainer=Trainer.objects.get(user=user)
    context={
        'object':trainer
    }
    if request.method=="POST":
        username=request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        fees = request.POST['fees']
        exp= request.POST['exp']
        available=request.POST.getlist('available')
        #user=MyUser.objects.get(username=username)
        #trainer=Trainer.objects.get(user=user)
        print(user,trainer)
        try:
            u=MyUser.objects.get(email=email)
            print("Entered try block")
            if(user.username!=u.username):
                msg="Email already exists, try another email"
                return render(request,'edit_profile_trainer.html',context)
        except:
            pass
        msg="Changes Saved"
        context={
            'msg':msg,
            'object':trainer
        }
        user.email=email
        user.phone=phone
        user.save()
        trainer.fees=fees
        trainer.experience=exp
        trainer.available=available
        trainer.save()
        l=setTimes(available)
        slot=Slot(user=user,
            t5=l[0],t6=l[1],t7=l[2],
            t8=l[3],t9=l[4],t10=l[5],
            t11=l[6],t12=l[7],t13=l[8],
            t14=l[9],t15=l[10],t16=l[11],
            t17=l[12],t18=l[13],t19=l[14],
            t20=l[15],t21=l[16]
            )
        print(slot)
        slot.save()
        return render(request,'edit_profile_trainer.html',context)
    return render(request,'edit_profile_trainer.html',context)

def edit_profile_member(request):
    context={}
    user=request.user
    member=Member.objects.get(user=user)
    print(member.health_issues)
    context={
        "health":member.health_issues
    }
    if request.method=="POST":
        username=request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        health=request.POST['health']
        user=request.user
        

        #user=MyUser.objects.get(username=username)
        #trainer=Trainer.objects.get(user=user)
        try:
            u=MyUser.objects.get(email=email)
            print("Entered try block")
            if(user.username!=u.username):
                msg="Email already exists, try another email"
                return render(request,'edit_profile_member.html',context)
        except:
            pass
        msg="Changes Saved"
        context={
            'msg':msg
        }
        user.email=email
        user.phone=phone
        member.health_issues=health
        user.save()
        member.save()
        return render(request,'edit_profile_member.html',context)
    return render(request,'edit_profile_member.html',context)

def edit_profile_dietician(request):
    context={}
    user=request.user
    dietician=Dietician.objects.get(user=user)
    context={
        'object':dietician
    }
    if request.method=="POST":
        username=request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        fees = request.POST['fees']
        exp= request.POST['exp']
        available=request.POST.getlist('available')
        #user=MyUser.objects.get(username=username)
        #trainer=Trainer.objects.get(user=user)
        print(user,dietician)
        try:
            u=MyUser.objects.get(email=email)
            print("Entered try block")
            if(user.username!=u.username):
                msg="Email already exists, try another email"
                return render(request,'edit_profile_dietician.html',context)
        except:
            pass
        msg="Changes Saved"
        context={
            'msg':msg,
            'object':dietician
        }
        user.email=email
        user.phone=phone
        user.save()
        dietician.fees=fees
        dietician.experience=exp
        dietician.available=available
        dietician.save()
        l=setTimes(available)
        slot=Slot(user=user,
            t5=l[0],t6=l[1],t7=l[2],
            t8=l[3],t9=l[4],t10=l[5],
            t11=l[6],t12=l[7],t13=l[8],
            t14=l[9],t15=l[10],t16=l[11],
            t17=l[12],t18=l[13],t19=l[14],
            t20=l[15],t21=l[16]
            )
        print(slot)
        slot.save()
        return render(request,'edit_profile_dietician.html',context)
    return render(request,'edit_profile_dietician.html',context)

def trainer_list(request):
    queryset=MyUser.objects.filter(is_trainer=True,is_member=False)
    context={
        'obj_list':queryset
    }
    if request.method =="POST":
        username=request.POST.get('search1')
        if(len(username)!=0):
            u= MyUser.objects.all()
            if(u):
                for st in u:
                    if(st):
                        s=st.workout
                        if(s!='None'):
                            print(s,"set")
                            is_trainer=True
                            k=MyUser.objects.filter(workout__contains=username,is_trainer=True)
                            context={
                                'obj_list':k
                            }
                            print(k,"query")
    return render(request,"trainer_list.html",context)

def dietician_list(request):
    queryset=MyUser.objects.filter(is_dietician=True,is_member=False)
    dietician=Dietician.objects.all()
    context={
        'obj_list':queryset,
    }
    return render(request,"dietician_list.html",context)

def dietician_register(request):
    if True:
        if request.method == 'POST':
            name = request.POST['name']
            exp = request.POST['exp']
            email = request.POST['email']
            age = request.POST['age']
            phone = request.POST['phone']
            category = request.POST.getlist('category')
            fees = request.POST['fees']
            available=request.POST.getlist('available')
            gender = request.POST.get('gender')
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                if(MyUser.objects.filter(username=name).exists()):
                    messages.info(request,"username already exists")
                elif(MyUser.objects.filter(email=email).exists()):
                    messages.info(request, 'Email already exists')
                else:
                    user = MyUser(
                        username=name,
                        email=email,
                        password=password1,
                        is_trainer=False,
                        is_member=False,
                        is_dietician=True,
                        age=age,
                        gender=gender,
                        phone=phone,
                        )
                    #user.password = make_password(user.password)
                    user.save()
                    dietician=Dietician(user=user,experience=exp,
                        fees=fees,
                        available=available,
                        category=category
                        )
                    dietician.save()
                    slot=Slot(user=user)
                    l=setTimes(available)
                    print(l)
                    
                    slot=Slot(user=user,
                    t5=l[0],t6=l[1],t7=l[2],
                    t8=l[3],t9=l[4],t10=l[5],
                    t11=l[6],t12=l[7],t13=l[8],
                    t14=l[9],t15=l[10],t16=l[11],
                    t17=l[12],t18=l[13],t19=l[14],
                    t20=l[15],t21=l[16]
                    )
                    print(slot)
                    #setTimes(slot,available)
                    slot.save()
                    print('user saved')
                    return redirect('login')
            else:
                messages.info(request, 'Passwords not matching')
                return redirect('dietician_register')
            return redirect('/')
        else:
            return render(request,"registration/dietician_register.html")

def dynamic_lookup(request,my_name):
    context={}
    obj=MyUser.objects.get(username=my_name)
    trainer=Trainer.objects.all()
    ob={}
    for lineitems in trainer:
        print(lineitems)
        if(str(lineitems.user) == my_name):
            print(str(lineitems.user))
            
            context={
	            "object":obj ,
                "fees":lineitems.fees,
                "experience":lineitems.experience,
                "available":lineitems.available,
                "rating":lineitems.rating
	        }
    
    return render(request,"dynamic_lookup.html",context)

def dynamic_lookup_dietician(request,my_name):
    context={}
    obj=MyUser.objects.get(username=my_name)
    dietician=Dietician.objects.all()
    ob={}
    for lineitems in dietician:
        print(lineitems)
        if(str(lineitems.user) == my_name):
            print(str(lineitems.user))
            
            context={
	            "object":obj ,
                "fees":lineitems.fees,
                "experience":lineitems.experience,
                "available":lineitems.available,
                "rating":lineitems.rating,
                "category":lineitems.category,
	        }
    
    return render(request,"dynamic_lookup_dietician.html",context)

def bookslot(request,my_name):
    context={}
    trainer=Trainer.objects.all()
    obj=MyUser.objects.get(username=my_name)
    slot=Slot.objects.all()
    val={}
    for i in slot:
        if(str(i.user)==my_name):
            val=i
            print(val.t5)
            break
    for lineitems in trainer:
        print(lineitems.available)
        #print(lineitems.user_id,lineitems.user)
        if(str(lineitems.user) == my_name):
            print(str(lineitems.user))
            #ob=str(lineitems)
            print(obj.email)
            context={
                #"object":obj,
                "email1":obj.email,
                "availables":lineitems.available,
                "name1":lineitems.user,
                "obj":lineitems,
                "slot":val
                #"available":lineitems.available
	        }
            break
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        tname=request.POST['tname']
        temail=request.POST['temail']
        avl=request.POST.getlist('availables')
        meetinglink=request.POST['meetinglink']
        slot=Slot.objects.all()
        user=MyUser.objects.get(username=tname)
        val={}
        for i in slot:
            if(str(i.user)==tname):
                #val=i
                #print(val)
                for x in avl:
                    actualvalue=dict[x]
                    print(actualvalue)
                    slot=Slot.objects.get(user=user)
                    print(slot)
                    #slot.actualvalue =name
                    setattr(slot, actualvalue, name)
                    slot.save()
                    trainer=Trainer.objects.get(user=user)
                   # print(trainer.available)
                    input_str=trainer.available
                    input_str=input_str.replace('[','')
                    input_str=input_str.replace(']','')
                    list2=input_str.split(',')
                    print(list2)
                    
                    new_str=[]
                    for i in list2:
                        check=i.replace("'","").strip()
                        print(check,x)
                        if x!=check:
                            new_str.append(check)

                    print(new_str)
                    trainer.available=new_str
                    trainer.save()
                    
        subject =name+" has booked "+tname+"'s "+"slot"
        tmesg1="Hello "+tname+"\n"
        tmesg2="Your session is booked by "+name+"\n"
        tmesg3="Timings : "+str(avl)+"\n"
        tmesg4="Meeting Link : "+"\n"+str(meetinglink)+"\n"
        tmsg=tmesg1+tmesg2+tmesg3+tmesg4
        mesg1="Hello "+name+"\n"
        mesg2="You have booked "+tname+"'s "+ "session"+"\n"
        msg=mesg1+mesg2+tmesg3+tmesg4
        email_from=settings.EMAIL_HOST_USER
        recipient_list =[email,temail]
        send_mail(
            subject,msg,email_from,[email]
        )
        send_mail(
            subject,tmsg,email_from,[temail]
        )
        msg="Hurray, Your slot is booked!"
        context={
            "msg":msg,
         }
        return render(request,'profile_member.html',context)
    return render(request,'bookslot.html',context)

def bookslot_dietician(request,my_name):
    context={}
    dietician=Dietician.objects.all()
    obj=MyUser.objects.get(username=my_name)
    slot=Slot.objects.all()
    val={}
    for i in slot:
        if(str(i.user)==my_name):
            val=i
            break
    for lineitems in dietician:
        print(lineitems.available)
        if(str(lineitems.user) == my_name):
            print(str(lineitems.user))
            print(obj.email)
            context={
                #"object":obj,
                "email1":obj.email,
                "availables":lineitems.available,
                "name1":lineitems.user,
                "obj":lineitems,
                "slot":val
                #"available":lineitems.available
	        }
            break
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        tname=request.POST['tname']
        temail=request.POST['temail']
        avl=request.POST.getlist('availables')
        meetinglink=request.POST['meetinglink']
        slot=Slot.objects.all()
        user=MyUser.objects.get(username=tname)
        val={}
        for i in slot:
            if(str(i.user)==tname):
                #val=i
                #print(val)
                for x in avl:
                    actualvalue=dict[x]
                    print(actualvalue)
                    slot=Slot.objects.get(user=user)
                    print(slot)
                    #slot.actualvalue =name
                    setattr(slot, actualvalue, name)
                    slot.save()
                    dietician=Dietician.objects.get(user=user)
                   # print(trainer.available)
                    input_str=dietician.available
                    input_str=input_str.replace('[','')
                    input_str=input_str.replace(']','')
                    list2=input_str.split(',')
                    print(list2)
                    
                    new_str=[]
                    for i in list2:
                        check=i.replace("'","").strip()
                        print(check,x)
                        if x!=check:
                            new_str.append(check)

                    print(new_str)
                    dietician.available=new_str
                    dietician.save()
        subject =name+" has booked "+tname+"'s "+"slot"
        tmesg1="Hello "+tname+"\n"
        tmesg2="Your session is booked by "+name+"\n"
        tmesg3="Timings : "+str(avl)+"\n"
        tmesg4="Meeting Link : "+"\n"+str(meetinglink)
        tmsg=tmesg1+tmesg2+tmesg3+tmesg4
        mesg1="Hello "+name+"\n"
        mesg2="You have booked "+tname+"'s "+ "session"+"\n"
        msg=mesg1+mesg2+tmesg3+tmesg4
        email_from=settings.EMAIL_HOST_USER
        recipient_list =[email,temail]
        send_mail(
            subject,msg,email_from,[email]
        )
        send_mail(
            subject,tmsg,email_from,[temail]
        )
        msg="Hurray, Your slot is booked!"
        context={
            "msg":msg,
         }
        return render(request,'profile_member.html',context)
    return render(request,'bookslot_dietician.html',context)
    

def bookings(request):
    user=request.user
    slot=Slot.objects.all()
    q = Slot.objects.filter(user=request.user).values()
    print(q)
    dict1=defaultdict(list)
    for x in q:
        for key,value in x.items():
            if key=='user_id':
                pass
            elif value in dict:
                dict1[value]="Available"
            elif value not in dict and value!='0':
                dict1[value,dict_rev[key]]="Booked"
    print(dict1.keys())
    print(dict1.values())
    actualslot=zip(dict1.keys(),dict1.values())
    context={
        'slot':actualslot

        
    }
    
    return render(request,'bookings.html',context)


def registerNew(request):
    if request.method =="POST":
        username=request.POST.get('ghost')
        if(len(username)!=0):
         try:
            u= MyUser.objects.all()
            if(u):
                for st in u:
                    if(st):
                        s=st.workout
                        if(s!='None'):
                            print(s,"set")
                            k=MyUser.objects.filter(workout__contains=username)
                            print(k,"query")
                            if(len(k)!=0):
                                for i in range(len(k)):
                                    user= MyUser.objects.get(username=k[i])
                                    if user is not None:
                                        login(request,user)
                                        print(request.user.is_trainer)
                                        print(request.user.is_member)
                                        print(request.user.is_dietician)
                                        if request.user.is_trainer:
                                             return redirect('trainer_list')
                            else:
                                        print("not trainer")
                                        us=Dietician.objects.all()
                                        for st in us:
                                            if(st):
                                                s=st.category
                                                print(s,"nutrition")
                                                print(username)
                                                print(Dietician.objects.all())
                                                k=Dietician.objects.filter(category__contains=username)
                                                print(k[0].user,"app")
                                                print(k,"in direician")
                                                print(len(k))
                                                for i in range(len(k)):
                                                    user= MyUser.objects.get(username=k[i].user)
                                                    print(request.user.is_dietician)
                                                    return redirect('dietician_list')
            else:
                print("Dietician")
                us= Dietician.objects.all()
                for st in us:
                    if(st):
                            s=st.category
                            print(s)
                            k=Dietician.objects.filter(workout__contains=username)
                            print(k)
                            for i in range(len(k)):
                                user= MyUser.objects.get(username=k[i])
                                if user is not None:
                                    login(request,user)
                                    print(request.user.is_trainer)
                                    print(request.user.is_member)
                                    print(request.user.is_dietician)
                                    if request.user.is_member:
                                        print("Entered inside the profile")
                                        return redirect('profile_member')
                                    elif(request.user.is_trainer):
                                        return redirect('profile_trainer')
                                    elif(request.user.is_dietician):
                                        print("Entered the dietician profile")
                                        return redirect('profile_dietician')

                    else:
                        print("no")
         except:
            print("Incorrect")
            messages.info(request,'Username or Password is incorrect')
            return render(request,'registerNew.html')
    return render (request,"registerNew.html")
def payment(request):
    if request.method=='POST':
      amount = 50000
      order_currency = 'INR'
      client=razorpay.Client(auth=('rzp_test_bQBeJB9sMBAN7P','TbqHxE7KwOK2QoTM1pEDf7eE'))
      payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})  
    return render(request,'payment.html')
def success(request):
    return render(request,'bookslot.html')
     # OPTIONALclient.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes)

