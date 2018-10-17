from django.contrib.postgres.aggregates.general import StringAgg
from django.db.models import CharField as ModelCharField
from django.db.models.functions import Cast
from rest_framework.serializers import CharField, IntegerField, Serializer, ValidationError

from chat.models import Room, RoomMember
from users.models import User


class SendMessageSerializer(Serializer):
    room_id = IntegerField(required=False, allow_null=True)
    user_id = IntegerField(required=False, allow_null=True)
    text = CharField()

    def validate(self, data):
        room_id = data.get('room_id', None)
        user_id = data.get('user_id', None)

        if room_id is None and user_id is None:
            raise ValidationError({'room_id': 'One of this fields:room_id, user_id is required.'})

        if room_id:
            self.context['room'] = Room.objects.filter(room_id=room_id, owner=self.context['user']).first()
            if not self.context['room']:
                raise ValidationError({'room_id': 'Room was not found.'})

        if user_id:
            if user_id == self.context['user'].id:
                raise ValidationError({'user_id': 'You can\'t send message to yourself.'})

            user = User.objects.filter(id=user_id).first()
            if not user:
                raise ValidationError({'user_id': 'User was not found.'})

            room_ids = RoomMember.objects.filter(user=self.context['user']).values_list('room_id', flat=True)
            room_exist = RoomMember.objects.filter(room_id__in=room_ids) \
                .values('room_id') \
                .annotate(item=StringAgg(Cast('user_id', ModelCharField()), ',', ordering=('user_id',))) \
                .filter(item=','.join(sorted([str(user_id), str(self.context['user'].id)])))

            if len(room_exist):
                print('+++++++++++')

        return data
