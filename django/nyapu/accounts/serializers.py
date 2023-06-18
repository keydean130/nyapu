from accounts.models import CustomUser, Relationship
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.core.mail import EmailMessage


class RelationshipSerializer(serializers.ModelSerializer):
    """ユーザー間のフォロー関係のシリアライザ"""
    def create(self, validated_data):
        """Relationship保存前の処理
        
        フォロー済みかどうかの検証を行い、未フォローであれば保存する。
        """
        # 一意性のバリデーションを行う
        follower = validated_data['follower']
        following = validated_data['following']
        # 既に存在するRelationshipであれば
        if Relationship.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError('既にフォロー済みです')
        # 存在しなければ保存
        return super().create(validated_data)
    
    class Meta:
        model = Relationship
        fields = ['id', 'follower', 'following']



class CustomUserSerializer(serializers.ModelSerializer):
    """カスタムユーザーのシリアライザ"""
    follows = RelationshipSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class InquirySerializer(serializers.Serializer):
    """お問い合わせ用シリアライザ"""

    name = serializers.CharField(label='お名前', max_length=30)
    email = serializers.EmailField(label='メールアドレス')
    title = serializers.CharField(label='タイトル', max_length=30)
    message = serializers.CharField(label='メッセージ', style={'widget': 'textarea'})

    def send_email(self):
        """お問い合わせメール送信"""
        name = self.validated_data.get('name')
        email = self.validated_data.get('email')
        title = self.validated_data.get('title')
        message = self.validated_data.get('message')
        subject = 'お問い合わせ内容: {0}'.format(title)
        email_body = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}\n\n上記のお問い合わせを受け付けました。' \
                     '内容確認し返信いたしますので、暫くお待ちください。'.format(name, email, message)
        from_email = 'admin@nyapumap.com'
        to_list = ['nyapumail@outlook.com']
        cc_list = [email]
        email_message = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=to_list, cc=cc_list)
        email_message.send()
        return True
