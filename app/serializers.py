from .models import Agenda,Sponsor,ConferenseSection,User,Author,Paper,Home,Agenda,Direction
from rest_framework import serializers


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'



class SignInSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PaperSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Paper
        fields = '__all__'

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        paper = Paper.objects.create(**validated_data)
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            paper.authors.add(author)
        return paper
    
class HomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Home
        fields = '__all__'

class AgendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agenda
        fields = '__all__'

class ConferenseSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConferenseSection
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = '__all__'

class DirectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direction
        fields = '__all__'















