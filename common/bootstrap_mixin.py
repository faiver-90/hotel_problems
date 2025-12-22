from django import forms


class BootstrapFormMixin:
    """
    Автоматически добавляет bootstrap-классы ко всем полям формы.
    """

    def _init_bootstrap(self) -> None:
        for _name, field in self.fields.items():
            widget = field.widget

            # input / select / textarea
            if isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.PasswordInput,
                    forms.Select,
                    forms.Textarea,
                ),
            ):
                widget.attrs.setdefault("class", "form-control")

            # checkbox / radio
            elif isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                widget.attrs.setdefault("class", "form-check-input")

            # общие атрибуты
            widget.attrs.setdefault("placeholder", field.label)
