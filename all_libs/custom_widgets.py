from django.forms import ClearableFileInput, BaseFormSet, CheckboxInput, BaseModelFormSet, BooleanField
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'all_libs/widgets/customclearableentryimageinput.html'


class CustomCheckboxInput(CheckboxInput):
    template_name = "all_libs/widgets/custominput.html"


class CustomBaseFormSet(BaseFormSet):
    deletion_widget = CustomCheckboxInput

    def add_fields(self, form, index):
        super().add_fields(form, index)
        if self.can_delete and (
            self.can_delete_extra or (index is not None and index < self.initial_form_count())
        ):
            form.fields[DELETION_FIELD_NAME] = BooleanField(
                label=_(""),
                required=False,
                widget=self.get_deletion_widget(),
            )


class CustomBaseModelFormSet(CustomBaseFormSet, BaseModelFormSet):
    pass

