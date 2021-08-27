from django.http.response import Http404
import accounts
from accounts.models import Member
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from letter.forms import NameForm, WriteForm, WriteFormOthers
from letter.models import Letter, Receiveletter, Sendletter
from django.contrib.auth.decorators import login_required
from accounts.models import Member
from django.db import transaction
from django.contrib.messages import constants as messages_constants
from django.contrib import messages
from random import *
from datetime import datetime
# from google.cloud import language_v1
# client = language_v1.LanguageServiceClient.from_service_account_json(r'C:\Users\samsung\Desktop\django_study\service_account.json')

@login_required
def writeToMe(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
    
    if request.method == 'POST':
       
        memberId = request.session.get('user')
       
        now_member = Member.objects.get(memberId=memberId)

        write_form = WriteForm(request.POST)

        if write_form.is_valid():
            receive_date=write_form.receiveDate

            if receive_date < datetime.now():
                messages.add_message(request, messages.INFO, '받는 날짜를 현재 시간 이후로 설정해주세요.')
                context = {'write_form': write_form}
                return render(request, 'letter/writeToMe.html', context)

            # document = language_v1.Document(content=write_form.content, type_=language_v1.Document.Type.PLAIN_TEXT)
            # sentiment_doc = client.analyze_sentiment(request={'document': document}).document_sentiment
            # emotionScore = int((sentiment_doc.score * 100 + 100) / 2)
            
            emotionScore=50

            letter = Letter(
                senderId = now_member,
                content=write_form.content,
                receiveDate=write_form.receiveDate,
                emotion=emotionScore,
            )

            letter.save()

            letter_id=letter.letterId
            now_letter=Letter.objects.get(letterId=letter_id)
            
            sendLetter = Sendletter()
            sendLetter.letterId = now_letter
            sendLetter.senderId = now_member
            sendLetter.save() 

            receiveLetter = Receiveletter()
            receiveLetter.letterId = now_letter
            receiveLetter.receiverId = now_member
            receiveLetter.readCheck = False
            receiveLetter.save()

            messages.add_message(request, messages.INFO, '전송 성공.')
            return  redirect('/letter/letterFrmMe', request.user.memberId)
    else:
        write_form = WriteForm()
        context = {'write_form': write_form}
    return render(request, 'letter/writeToMe.html', context)

@login_required
def writeToOthers(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
    
    if request.method == 'POST':
        memberId = request.session.get('user')
        now_member = Member.objects.get(memberId=memberId)

        write_form = WriteFormOthers(request.POST)

        if write_form.is_valid():
            receive_date=write_form.receiveDate

            if receive_date < datetime.now():
                messages.error(request, messages.INFO, '받는 날짜를 현재 시간 이후로 설정해주세요.')
                context = {'write_form': write_form}
                return render(request, 'letter/writeToOthers.html', context)
          
            is_user_exist = False

            all_members = Member.objects.all()
            group=write_form.receiverGroup
            if all_members.filter(job=group).exclude(memberId=memberId).count() != 0:
                is_user_exist = True   


            if is_user_exist == False: 
                messages.error(request, '해당 그룹에 속한 사용자가 없어, 전송이 취소되었습니다.')            
                return render(request, 'letter/writeToOthers.html',  {'write_form': WriteFormOthers})
            
            else :
                letter = Letter(
                    senderId = now_member,
                    content=write_form.content,
                    receiveDate=write_form.receiveDate,
                    emotion=1,
                )
                letter.save()

                letter_id=letter.letterId
                now_letter=Letter.objects.get(letterId=letter_id)
                
                sendLetter = Sendletter()
                sendLetter.letterId = now_letter
                sendLetter.senderId = now_member
                sendLetter.save() 
                
                way_to_send = request.POST.get('way_to_send')

             
                if way_to_send == 'all' : 
                    for receiver in all_members.filter(job=group).exclude(memberId=memberId) : 
                        receiveLetter = Receiveletter()
                        receiveLetter.letterId = now_letter
                        receiveLetter.receiverId = receiver
                        receiveLetter.readCheck = False
                        receiveLetter.save()


                else : 
                    grpMember_num = all_members.filter(job=group).exclude(memberId=memberId).count()
                    if grpMember_num != 0 :
                        random_idx = randint(0,grpMember_num-1)
                        receiver = all_members.filter(job=group).exclude(memberId=memberId)[random_idx]
                        receiveLetter = Receiveletter()
                        receiveLetter.letterId = now_letter
                        receiveLetter.receiverId = receiver
                        receiveLetter.readCheck = False
                        receiveLetter.save()

                messages.add_message(request, messages.INFO, '전송 성공.')
                return  HttpResponseRedirect('/letter/letterFrmMe', request.user.memberId)
        else:
            messages.error(request, 'Error! Try Again')
            return render(request, 'letter/writeToOthers.html',  {'write_form': WriteFormOthers})
    else:
        write_form = WriteForm()
        return render(request, 'letter/writeToOthers.html',  {'write_form': WriteFormOthers})



@login_required
def letterFrmMe(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')

    if request.method=='GET':
        try:
            memberId=request.session.get('user')
            result = []

            if Member.objects.filter(memberId=memberId).exists():
                member=Member.objects.get(memberId=memberId)
                nickname=member.nickname

                if Receiveletter.objects.filter(receiverId=memberId):
                    receiveInfo=Receiveletter.objects.all().filter(receiverId=memberId).order_by('-receiveCol')
                    for recvLetter_col in receiveInfo:
                        letter_ids = recvLetter_col.letterId
                        letter_id = letter_ids.letterId
                        letter_obj = Letter.objects.get(letterId = letter_id)
                        recv_date=letter_obj.receiveDate
                        now_time=datetime.now()

                        if str(letter_obj.senderId) == str(memberId):

                            if recvLetter_col.is_deleted == False :
                        
                                if recvLetter_col.readCheck == False :
                                    letter_obj.content = "(읽지 않음)"
                                    
                                if recv_date <= now_time :
                                    letter_obj.content=letter_obj.content[:30]
                                    result.append(letter_obj)
                            
            
        except member.DoesNotExist:
            raise Http404("Error!")

    return render(request, 'letter/letterFrmMe.html', {'result':result, 'nickname' : nickname })



@login_required
def letterFrmOthers(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')

    if request.method=='GET':
        try:
            memberId=request.session.get('user')
            result = []
            
      
            if Member.objects.filter(memberId=memberId).exists():
                member=Member.objects.get(memberId=memberId)
                nickname=member.nickname

                if Receiveletter.objects.filter(receiverId=memberId):
                    receiveInfo=Receiveletter.objects.all().filter(receiverId=memberId).order_by('-receiveCol')
                    for recvLetter_col in receiveInfo:
                        letter_ids = recvLetter_col.letterId
                        letter_id = letter_ids.letterId
                        letter_obj = Letter.objects.get(letterId = letter_id)
                        recv_date=letter_obj.receiveDate
                        now_time=datetime.now()

                        if str(letter_obj.senderId) != str(memberId):
                            
                            if recvLetter_col.is_deleted == False :
                               
                                if recvLetter_col.readCheck == False :
                                    letter_obj.content = "(읽지 않음)"
                               
                                if recv_date <= now_time :
                                    letter_obj.content=letter_obj.content[:30]
                                    result.append(letter_obj)

                                
                               
        except member.DoesNotExist:
            raise Http404("Error!")

    return render(request, 'letter/letterFrmOthers.html', {'result':result, 'nickname' : nickname })    



@login_required
def recvletter_detail(request, letterId):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('accounts/Index')

    try :
        memberId = request.session.get('user')
        letter = Letter.objects.get(letterId=letterId)


        recv_letter = Receiveletter.objects.all().filter(letterId=letterId).get(receiverId=memberId)

        if str(recv_letter.receiverId) != str(memberId) :
            raise Http404("Error!")

        recv_letter.readCheck = True
        recv_letter.save()
        context = {'letter': letter}
        return render(request, 'letter/letter_detail.html', context) 

    except :
        raise Http404("Error!")



@login_required
def sentletter_detail(request, letterId):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('accounts/Index')

    try :     
        memberId = request.session.get('user')
        letter = Letter.objects.get(letterId=letterId)

        if str(letter.senderId) != str(memberId) : 
            raise Http404("Error!")

        context = {'letter': letter}

        return render(request, 'letter/letter_detail.html', context) 

    except :
        raise Http404("Error!")

@login_required
def letterIsent (request):
    try : 
        memberId = request.session.get('user')
        letters = Letter.objects.all().filter(senderId=memberId)

        result= []
        
        for letter in letters:
            letter_id = letter.letterId
            sendletter_obj = Sendletter.objects.get(letterId=letter_id)
            if sendletter_obj.is_deleted == False:
                result.append(letter)

        return render(request, 'letter/letterIsent.html', {'letters': result })
        
    except :
        raise Http404("Error!")


@login_required
def letter_delete_send(request, letterId):
    try : 
        memberId = request.session.get('user')

        send_letter_delete=Sendletter.objects.get(letterId=letterId)
        send_letter_delete.is_deleted = True
        send_letter_delete.save()

        context = {'senddelete': send_letter_delete}
        messages.add_message(request, messages.INFO, '보낸 메시지 삭제 성공.')
        return HttpResponseRedirect("/letter/letterIsent/")
    except :
        raise Http404("Error!")


@login_required
def letter_delete_receive(request, letterId):
    try  : 
        memberId = request.session.get('user')

        receive_letter_delete=Receiveletter.objects.all().filter(receiverId=memberId).get(letterId=letterId)
        receive_letter_delete.is_deleted = True
        receive_letter_delete.save()
        sender_id = Sendletter.objects.get(letterId=letterId).senderId
    

        messages.add_message(request, messages.INFO, '받은 메시지 삭제 성공.')
    
        #타인에게 받은 편지와 내가 나에게 쓴 편지를 확인해야 함
        if str(sender_id)==str(memberId):
            return HttpResponseRedirect("/letter/letterFrmMe/")
        else:
            return HttpResponseRedirect("/letter/letterFrmOthers/")

    except:
        raise Http404("Error!")
    

@login_required
def show_delete_list(request, page):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
        
    if request.method=='GET':
        try:
            memberId=request.session.get('user')
            result=[]
         

            if Member.objects.filter(memberId=memberId).exists():
                member=Member.objects.get(memberId=memberId)
                nickname=member.nickname


                if str(page)=='send':
              
                    if Sendletter.objects.filter(senderId=memberId):
                        send_delete_list=Sendletter.objects.all().filter(is_deleted=True) 
                        for send_col in send_delete_list:
                            letter_ids = send_col.letterId
                            letter_id = letter_ids.letterId
                            letter_obj = Letter.objects.get(letterId = letter_id)
                            letter_obj.content=letter_obj.content[:30]
                            result.append(letter_obj)
                            
                if str(page)=='receive':
                   
                    if Receiveletter.objects.filter(is_deleted=True):
                        receive_delete_list=Receiveletter.objects.all().filter(is_deleted=True)
                        for receive_col in receive_delete_list:
                            letter_ids = receive_col.letterId
                            letter_id = letter_ids.letterId
                            letter_obj = Letter.objects.get(letterId = letter_id)
                            letter_obj.content=letter_obj.content[:30]
                            result.append(letter_obj)
               
        except member.DoesNotExist:
            raise Http404("Error!")
    return render(request, 'letter/show_delete_list.html', {'result':result, 'nickname' : nickname, 'page':page})