from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from core.utils import translate_message

@receiver(post_save, sender=Message)
def translate_message_on_save(sender, instance, created, **kwargs):
    print("DEBUG: Signal Fired!")
    # Only translate if it's a newly created message or translated_text is intentionally empty
    if not instance.translated_text:
        # Use target language from the recipient's profile; default to English if not found
        try:
            target_lang = instance.recipient.profile.target_lang
            print(f"DEBUG: Signal retrieved target_lang = '{target_lang}' (recipient: {instance.recipient.username})")
        except AttributeError:
            target_lang = 'en'
            print(f"DEBUG: Signal defaulted target_lang = 'en' (recipient: {instance.recipient.username} has no profile)")
            
        # Optional: You could also have a source_lang field on the sender's profile
        # For now, let's assume we want to translate everything to target_lang
        # and we let DeepSeek auto-detect source language or pass a placeholder.
        source_lang = "auto"

        translated = translate_message(instance.original_text, source_lang, target_lang)

        # Avoid recursion by updating only the translated_text column without triggering Signals
        Message.objects.filter(pk=instance.pk).update(translated_text=translated)
