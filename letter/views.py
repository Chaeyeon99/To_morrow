from django.http.response import Http404
import accounts
from accounts.models import Member
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from letter.forms import NameForm, WriteForm, WriteForm_toOthers
from letter.models import Letter, Receiveletter, Sendletter
from django.contrib.auth.decorators import login_required
from accounts.models import Member
from django.db import transaction
from django.contrib.messages import constants as messages_constants
from django.contrib import messages
from random import *
#from google.cloud import language_v1
#client = language_v1.LanguageServiceClient.from_service_account_json(r'C:\Users\samsung\Desktop\django_study\service_account.json')



def emotion_result(request):

    return redirect('letter/emotion_result')


def writeToMe(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
    
    if request.method == 'POST':
        memberId = request.session.get('user')
        now_member = Member.objects.get(memberId=memberId)

        write_form = WriteForm(request.POST)
        if write_form.is_valid():

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

        write_form = WriteForm_toOthers(request.POST)
    
        if write_form.is_valid():
            # 선택한 그룹에 속한 사용자가 0명이라, 편지를 보내지 않는 경우 
            is_user_exist = False

            all_members = Member.objects.all()
      
            for group in write_form.receiverGroup:
                if all_members.filter(job=group).exclude(memberId=memberId).count() != 0:
                    is_user_exist = True   

            if is_user_exist == False: 
                messages.error(request, '해당 그룹에 속한 사용자가 없어, 전송이 취소되었습니다.')            
                return render(request, 'letter/writeToOthers.html',  {'write_form': WriteForm_toOthers})
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
            return render(request, 'letter/writeToOthers.html',  {'write_form': WriteForm_toOthers})
    else:
        write_form = WriteForm()
        return render(request, 'letter/writeToOthers.html',  {'write_form': WriteForm_toOthers})





#남이 나에게 보낸 메시지 목록
@login_required
def receive(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
    if request.method=='GET':
        try:
            memberId=request.session.get('user')

            if Member.objects.filter(memberId=memberId).exists():
                # member=Member.objects.get(memberId=memberId)
                # nickname=member.nickname

                if Receiveletter.objects.filter(receiverid=memberId).exists():
                    tmp= Receiveletter.objects.all(receiverid=memberId)
                    for receiveLetter in tmp :
                        letter_content = Letter.objects.get(receiveLetter.letterId).content
                        print(letter_content)
                    # receiveletter=Receiveletter.objects.get()
                    # contents=Letter.content

                # if Member.objects.filter(nickname=nickname).exists():
                #     member=Member.objects.get(nickname=nickname)
                #     context={'member':member, 'nickname':nickname, 'letter':Letter}
        except member.DoesNotExist:
            raise Http404("Error!")

    return render(request, 'letter/receive.html')

    #context={'letter':Letter, 'receiveletter':Receiveletter, 'member':Member}
    #letter={'letter': Letter.objects.all()}
    #receiveletter={'receiveletter': Receiveletter.objects.all()}
    #return render(request, 'letter/receive.html', context)

#나에게 보낸 메시지 목록
def to_me(request):
    letter={'letter': Letter.objects.all()}
    receiveletter={'receiveletter': Receiveletter.objects.all()}
    sendletter={'sendletter':Letter.objects.all()}
    return render(request, 'letter/to_me.html')

#메시지 상세 페이지
def message_detail(request, letter_id):
    letter = get_object_or_404(Letter, pk=letter_id)
    return render(request, 'letter/message_detail.html', {'letter':letter})

#남이 나에게 보낸 메시지 목록 삭제
def delete_from_other(request, letter_id):
    letter=Letter.objects.get(pk=letter_id)
    letter.delete()
    return redirect('receive')

#내가 나에게 보낸 메시지 목록 삭제
def delete_from_me(request, letter_id):
    letter=Letter.objects.get(pk=letter_id)
    letter.delete()
    return redirect('to_me')