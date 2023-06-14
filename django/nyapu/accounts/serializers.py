from accounts.models import CustomUser, Relationship
from rest_framework import serializers

from django.core.mail import EmailMessage


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class RelationshipSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer()
    following = CustomUserSerializer()

    class Meta:
        model = Relationship
        fields = ['id', 'follower', 'following']


class InquerySerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='お名前', max_length=30)
    email = serializers.EmailField(label='メールアドレス')
    title = serializers.CharField(label='タイトル', max_length=30)
    message = serializers.CharField(label='メッセージ', style={'widget': 'textarea'})

    def send_email(self):
        name = self.validated_data['name']
        email = self.validated_data['email']
        title = self.validated_data['title']
        message = self.validated_data['message']

        subject = 'お問い合わせ内容:{0}'.format(title)
        message = '送信者名:{0}\nメールアドレス:{1}\nメッセージ:\n{2}\n\n上記のお問い合わせを受け付けました。' \
                  '内容確認し返信いたしますので、暫くお待ちください。'.format(name, email, message)
        from_email = 'admin@nyapumap.com'
        to_list = ['nyapumail@outlook.com']
        cc_list = [email]
        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list,
                               cc=cc_list)
        message.send()
