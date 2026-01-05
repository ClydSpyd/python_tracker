from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Movie, Series, PinnedItem, Book, Quote, Link

# Auto-delete PinnedItem when a Movie is deleted
@receiver(post_delete, sender=Movie)
def delete_pinneditem_for_movie(sender, instance, **kwargs):
    PinnedItem.objects.filter(item_type="movie", item_id=instance.id).delete()

# Auto-delete PinnedItem when a Series is deleted
@receiver(post_delete, sender=Series)
def delete_pinneditem_for_series(sender, instance, **kwargs):
    PinnedItem.objects.filter(item_type="series", item_id=instance.id).delete()

@receiver(post_delete, sender=Book)
def delete_pinneditem_for_book(sender, instance, **kwargs):
    PinnedItem.objects.filter(item_type="book", item_id=instance.id).delete()   

@receiver(post_delete, sender=Quote)
def delete_pinneditem_for_quote(sender, instance, **kwargs):
    PinnedItem.objects.filter(item_type="quote", item_id=instance.id).delete()

@receiver(post_delete, sender=Link)
def delete_pinneditem_for_link(sender, instance, **kwargs):
    PinnedItem.objects.filter(item_type="link", item_id=instance.id).delete()