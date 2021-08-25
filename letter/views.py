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
#from google.cloud import language_v1
#client = language_v1.LanguageServiceClient.from_service_account_json(r'C:\Users\samsung\Desktop\django_study\service_account.json')


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
            # emotionScore = int(sentiment_doc.score * 100)
            
            emotionScore=50

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

            receiveLetter = Receiveletter()
            receiveLetter.letterId = now_letter
            receiveLetter.receiverId = now_member
            receiveLetter.readCheck = False
            receiveLetter.save()

            messages.add_message(request, messages.INFO, '전송 성공.')
            return  redirect('/accounts', request.user.memberId)
    else:
        write_form = WriteForm()
        context = {'write_form': write_form}
    return render(request, 'letter/writeToMe.html', context)


# 타인에게 편지 쓰기 
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
                messages.add_message(request, messages.INFO, '받는 날짜를 현재 시간 이후로 설정해주세요.')
                context = {'write_form': write_form}
                return render(request, 'letter/writeToOthers.html', context)
            # 선택한 그룹에 속한 사용자가 0명이라, 편지를 보내지 않는 경우 
            is_user_exist = False

            all_members = Member.objects.all()
      
            for group in write_form.receiverGroup:
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

             
                if way_to_send == 'all' :  # 그룹 내 모든 사용자에게 보내기 
                    for group in write_form.receiverGroup:
                        for receiver in all_members.filter(job=group).exclude(memberId=memberId) : 
                            receiveLetter = Receiveletter()
                            receiveLetter.letterId = now_letter
                            receiveLetter.receiverId = receiver
                            receiveLetter.readCheck = False
                            receiveLetter.save()
                else : # 그룹 내 1명의 사용자에게 보내기 
                    for group in write_form.receiverGroup:
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
                return  redirect('/accounts', request.user.memberId)
        else:
            messages.error(request, '전송 실패. 다시 시도해주세요')
            return render(request, 'letter/writeToOthers.html',  {'write_form': WriteFormOthers})
    else:
        write_form = WriteForm()
        return render(request, 'letter/writeToOthers.html',  {'write_form': WriteFormOthers})



#나에게 보낸 메시지 목록
@login_required
def letterFrmMe(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
    if request.method=='GET':
        try:
            memberId=request.session.get('user')
            result=[]

            #멤버에 해당 로그인 사용자가 존재하는지
            if Member.objects.filter(memberId=memberId).exists():
                member=Member.objects.get(memberId=memberId)
                nickname=member.nickname

                if Receiveletter.objects.filter(receiverId=memberId):
                    receiveInfo=Receiveletter.objects.all().filter(receiverId=memberId) #수신자가 나인 편지 필터링
                    for recvLetter_col in receiveInfo:
                        letter_ids = recvLetter_col.letterId
                        letter_id = letter_ids.letterId
                        letter_obj = Letter.objects.get(letterId = letter_id)
                        recv_date=letter_obj.receiveDate
                        now_time=datetime.now()

                        if str(letter_obj.senderId) == str(memberId):
                            # 삭제된 거 전처리
                            if recvLetter_col.is_deleted == False :
                                # 뿌리는 내용 전처리 
                                if recvLetter_col.readCheck == False :
                                    letter_obj.content = "(읽지 않음)"
                                    
                                if recv_date <= now_time :
                                    result.append(letter_obj)
                            
            
        except member.DoesNotExist:
            raise Http404("Error!")

    return render(request, 'letter/letterFrmMe.html', {'result':result, 'nickname' : nickname })



# 타인에게 받은 목록 
@login_required
def letterFrmOthers(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')

    if request.method=='GET':
        try:
            memberId=request.session.get('user')
            result = []
            
            #멤버에 해당 로그인 사용자가 존재하는지
            if Member.objects.filter(memberId=memberId).exists():
                member=Member.objects.get(memberId=memberId)
                nickname=member.nickname

                if Receiveletter.objects.filter(receiverId=memberId):
                    receiveInfo=Receiveletter.objects.all().filter(receiverId=memberId) #수신자가 나인 편지 필터링
                    for recvLetter_col in receiveInfo:
                        letter_ids = recvLetter_col.letterId
                        letter_id = letter_ids.letterId
                        letter_obj = Letter.objects.get(letterId = letter_id)
                        recv_date=letter_obj.receiveDate
                        now_time=datetime.now()

                        if str(letter_obj.senderId) != str(memberId):
                            # 삭제된 거 전처리
                            if recvLetter_col.is_deleted == False :
                                # 뿌리는 내용 전처리 
                                if recvLetter_col.readCheck == False :
                                    letter_obj.content = "(읽지 않음)"
                                #시간비교 조건 넣기
                                if recv_date <= now_time :
                                    result.append(letter_obj)
                                
                               
        except member.DoesNotExist:
            raise Http404("Error!")

    return render(request, 'letter/letterFrmOthers.html', {'result':result, 'nickname' : nickname })    


# 받은 글 상세보기 
def recvletter_detail(request, letterId):
    memberId = request.session.get('user')
    letter = Letter.objects.get(letterId=letterId)

    recv_letter = Receiveletter.objects.all().filter(letterId=letterId).get(receiverId=memberId)
    recv_letter.readCheck = True
    recv_letter.save()

    context = {'letter': letter}
    return render(request, 'letter/letter_detail.html', context) 

# 보낸 글 상세보기
def sentletter_detail(request, letterId):
    memberId = request.session.get('user')
    letter = Letter.objects.get(letterId=letterId)
    context = {'letter': letter}

    return render(request, 'letter/letter_detail.html', context) 


# 내가 보낸 편지 목록 
def letterIsent (request):
    memberId = request.session.get('user')
    letters = Letter.objects.all().filter(senderId=memberId)
    # result = []
    # for letter in Letter.objects.all().filter(senderId=memberId): 
    #     result.append(letter)

    return render(request, 'letter/letterIsent.html', {'letters': letters })



#보낸 메시지 삭제 기능
def letter_delete_send(request, letterId):
    memberId = request.session.get('user')

    send_letter_delete=Sendletter.objects.get(letterId=letterId)
    send_letter_delete.is_deleted = True
    send_letter_delete.save()

    context = {'senddelete': send_letter_delete}
    messages.add_message(request, messages.INFO, '보낸 메시지 삭제 성공.')
    return render(request, 'letter/show_delete_list.html', context)

#받은 메시지 삭제 기능
def letter_delete_receive(request, letterId):
    memberId = request.session.get('user')

    receive_letter_delete=Receiveletter.objects.all().filter(receiverId=memberId).get(letterId=letterId)
    receive_letter_delete.is_deleted = True
    receive_letter_delete.save()

    context = {'receivedelelte': receive_letter_delete}
    messages.add_message(request, messages.INFO, '받은 메시지 삭제 성공.')
    return render(request, 'letter/show_delete_list.html', context)

#휴지통 목록
def show_delete_list(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
    if request.method=='GET':
        try:
            memberId=request.session.get('user')
            resultsend=[]
            resultreceive=[]

            #멤버에 해당 로그인 사용자가 존재하는지
            if Member.objects.filter(memberId=memberId).exists():
                member=Member.objects.get(memberId=memberId)
                nickname=member.nickname

                #보낸 메시지 중 삭제한 목록
                if Sendletter.objects.filter(senderId=memberId):
                    send_delete_list=Sendletter.objects.all().filter(is_deleted=True) #is_deleted가 True인 삭제된 메시지 필터링
                    for send_col in send_delete_list:
                        letter_ids = Sendletter.letterId
                        letter_id = letter_ids.letterId
                        letter_obj = Letter.objects.get(letterId = letter_id)
                        resultsend.append(letter_obj)
                
                #받은 메시지 중 삭제한 목록
                if Receiveletter.objects.filter(is_deleted=True):
                    receive_delete_list=Receiveletter.objects.all().filter(is_deleted=True)
                    for receive_col in receive_delete_list:
                        letter_ids = receive_col.letterId
                        letter_id = letter_ids.letterId
                        letter_obj = Letter.objects.get(letterId = letter_id)
                        resultreceive.append(letter_obj)

        except member.DoesNotExist:
            raise Http404("Error!")
    return render(request, 'letter/show_delete_list.html', {'resultsend':resultsend, 'resultreceive':resultreceive, 'nickname' : nickname })