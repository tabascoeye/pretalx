from django import forms

from pretalx.common.forms import ReadOnlyFlag
from pretalx.submission.models import Feedback


class FeedbackForm(ReadOnlyFlag, forms.ModelForm):
    def __init__(self, talk=None, **kwargs):
        super().__init__(**kwargs)
        if not talk:
            raise Exception('Cannot provide feedback form without talk')
        self.instance.talk = talk
        self.fields['speaker'].queryset = self.instance.talk.speakers.all()

    def save(self, *args, **kwargs):
        if not self.cleaned_data['speaker'] and self.instance.talk.speakers.count() == 1:
            self.instance.speaker = self.instance.talk.speakers.first()
        return super().save(*args, **kwargs)

    class Meta:
        model = Feedback
        fields = [
            'speaker', 'review',
        ]