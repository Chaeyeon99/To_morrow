from django.http.response import Http404
import accounts
from accounts.models import Member
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from letter.forms import NameForm, WriteForm
from letter.models import Letter, Receiveletter
from django.contrib.auth.decorators import login_required
from accounts.models import Member
from django.db import transaction
#from google.cloud import language_v1
#client = language_v1.LanguageServiceClient.from_service_account_json(r'C:\Users\samsung\Desktop\django_study\service_account.json')


def test(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        if form.is_valid():
            #content = form.cleaned_data['letter']
            #document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)
            #sentiment_doc = client.analyze_sentiment(request={'document': document}).document_sentiment
            #sent_score = sentiment_doc.score
            sent_score=5

            #return render(request, 'letter/emotion_result.html', {'letter': content, 'sentiment':sent_score})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'letter/test.html', {'form': form})


def emotion_result(request):

    return redirect('letter/emotion_result')

#원본 write
# def write(request):
#     if not request.session.get('user'): 
#         return redirect('/accounts/login')
    
#     if request.method == 'POST':
#         memberId=request.session.get('user')
#         member = Member.objects.get(memberId=memberId)

#         write_form = WriteForm(request.POST)
#         if write_form.is_valid():
#             letter = Letter(
#                 senderId = member,
#                 content=write_form.content,
#                 receiveDate=write_form.receiveDate,
#                 emotion=1,
#             )

#             letter.save()
#             return  redirect('/accounts', request.user.memberId)
#     else:
#         write_form = WriteForm()
#         context = {'write_form': write_form}
#     return render(request, 'letter/write.html', context)

def write(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')
    
    if request.method == 'POST':
        memberId = request.session.get('user')
        member = Member.objects.get(memberId=memberId)

        write_form = WriteForm(request.POST)
        if write_form.is_valid():
            letter = Letter(
                senderId = member,
                content=write_form.content,
                receiveDate=write_form.receiveDate,
                emotion=1,
            )
            letter.save()
            
            letter_id = Letter.objects.get(letterId=6)

            receiveLetter = Receiveletter()
            receiveLetter.letterId = letter_id
            receiveLetter.receiverId = member
            receiveLetter.readCheck = False
            receiveLetter.save()
            
            return  redirect('/accounts', request.user.memberId)
    else:
        write_form = WriteForm()
        context = {'write_form': write_form}
    return render(request, 'letter/write.html', context)
# def write(request):
#     if not request.session.get('user'): 
#         return redirect('/accounts/login')
    
#     if request.method == 'POST':
#         memberId=request.session.get('user')
#         member = Member.objects.get(memberId=memberId)

#         write_form = WriteForm(request.POST)
#         if write_form.is_valid():
#             letter = Letter(
#                 senderId = member,
#                 content=write_form.content,
#                 receiveDate=write_form.receiveDate,
#                 emotion=1,
#             )

#             receive_letter = Receiveletter(
#                 receiverId 
#                 readCheck

#             )

#             letter.save()
#             return  redirect('/accounts', request.user.memberId)
#     else:
#         write_form = WriteForm()
#         context = {'write_form': write_form}
#     return render(request, 'letter/write.html', context)

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