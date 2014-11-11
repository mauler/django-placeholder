from django import forms


def get_model_image_upload_form(model_class, field):

    class ImageUploadForm(forms.ModelForm):

        class Meta:
            fields = [field]
            model = model_class

    return ImageUploadForm
