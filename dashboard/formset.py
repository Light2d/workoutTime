from django.forms import modelformset_factory
from workoutTimeApp.models import SportGroundImage

SportGroundImageFormSet = modelformset_factory(
    SportGroundImage,
    fields=('image',),
    extra=3,  # количество дополнительных форм
    can_delete=True  # если нужно удаление изображений
)
