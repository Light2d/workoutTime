from django import forms
from workoutTimeApp.models import CustomUser, Event, LastEvent, Article, SportGround, TeamMember

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'full_name', 'profile_photo', 'birth_date', 'is_active', 'is_staff']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        

class LastEventForm(forms.ModelForm):
    class Meta:
        model = LastEvent
        fields = '__all__'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        
class SportGroundForm(forms.ModelForm):
    class Meta:
        model = SportGround
        fields = '__all__'
        
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'