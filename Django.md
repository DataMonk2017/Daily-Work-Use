# 10.9.2017

## DoesNotExist Exception when getting object
There is no 'built in' way to do this. Django will raise the DoesNotExist exception every time. The idiomatic way to handle this in python is to wrap it in a try catch:
```python
try:
    go = SomeModel.objects.get(foo='bar')
except SomeModel.DoesNotExist:
    go = None
```    
What I did do, is to subclass models.Manager, create a safe_get like the code above and use that manager for my models. That way you can write: SomeModel.objects.safe_get(foo='bar').

This solution is four lines long. For me this is too much. With django 1.6 you can use SomeModel.objects.filter(foo='bar').first() this returns the first match, or None. It does not fail if there are several instances like queryset.get()

## django command to delete all tables

A. Delete all tables

manage.py sqlclear will print the sql statement to drop all tables

B. delete all data in all tables

manage.py flush returns the database to the state it was in immediately after syncdb was executed

C. Create all tables as defined in the model?

manage.py migrate Creates the database tables for all apps in INSTALLED_APPS whose tables have not already been created.

See this page for a reference of all commands: https://docs.djangoproject.com/en/dev/ref/django-admin/

But you should definitely look into using south as someone already mentioned. It's the best way to manage your database.

## Django ForeignKey whichi does not require referetial integrity
There is now a built in way to handle this by setting db_constraint=False on your ForeignKey:

https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.ForeignKey.db_constraint

customer = models.ForeignKey('Customer', db_constraint=False)
or if you want to to be nullable as well as not enforcing referential integrity:

customer = models.ForeignKey('Customer', null=True, blank=True, db_constraint=False) 
We use this in cases where we cannot guarantee that the relations will get created in the right order.

## Setting Django/MySQL site to use UTF-8
'OPTIONS':{'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci'}

## Get date from a Django DateTimeField

#### DateTimeField becomes a datetime.datetime object in Python

[StackOverflow](https://stackoverflow.com/questions/35300460/get-date-from-a-django-datetimefield)

If you need a date object to manipulate later on, you could pull the `datetime.date` object directly from your `DateTimeField()`, using `datetime.datetime.date()` like below:

```
class ApplicantData(models.Model):
    scheduled_at = models.DateTimeField(null=True, blank=True)

date = application_data.scheduled_at.date()
```
This works because Django will translate the DateTimeField into the Python type `datetime.datetime`, upon which we have called `date()`.

Format the `datetime.date` like you wish

Then from that, you get a `datetime.date` object, that you can format like you wish, using `datetime.date.strftime()`.

If you don't need a date object, you can also use `strftime` on your `datetime.datetime` object too, no problems with that. Except that your had a None field in your object.

Dealing with NULL/None fields

If you want to allow for NULL values in scheduled_at you can do:
```
if application_data.scheduled_at is not None:
      date = application_data.scheduled_at.date()
```

## Django override default form error messages

The easiest way is to provide your set of default errors to the form field definition. Form fields can take a named argument for it. For example:
```
my_default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value'
}

class MyForm(forms.Form):
    some_field = forms.CharField(error_messages=my_default_errors)
    ....
```    
    
Hope this helps.

## python text file busy
[StackOverflow](https://stackoverflow.com/questions/34170655/python-gives-oserror-text-file-busy-upon-trying-to-execute-temporary-file)

You need to close the binFileHandle before execution, similarily the code did for srcFileHandle.
```
...
from os import close, remove  # <---
...

print("Executing...")
close(binFileHandle)  # <---
call([binFileName])
...
```

## Difference between HttpResponseNotFound and Http404 in Django
[StackOverflow](https://stackoverflow.com/questions/7710444/whats-the-difference-between-returning-a-httpresponsenotfound-and-raising-a)
An HttpResponseNotFound is just like a normal HttpResponse except it sends error code 404. So it's up to you to render an appropriate 404 page in that view, otherwise the browser will display its own default.

Raising an Http404 exception will trigger Django to call its own 404 error view. Actually, this does little more than render the 404.html template and send it - using HttpResponseNotFound, in fact. But the convenience is that you're then specifying the template (and view, if you like) in one place.

## Check whether this user is anoymous or acutally a user on my system

[StackOverflow](https://stackoverflow.com/questions/4642596/how-do-i-check-whether-this-user-is-anonymous-or-actually-a-user-on-my-system)

[is_anonymous](https://docs.djangoproject.com/en/dev/topics/auth/#django.contrib.auth.models.User.is_anonymous)

## File Uploads

When Django handles a file upload, the file data ends up placed in request.FILES. There are security risks if you are accepting uploaded content from untrusted users!

```
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
```
So the data from the above form would be accessible as `request.FILES['file']` 

Note that `request.FILES` will only contain data if the request method was POST and the `<form>` that posted the request has the attribute `enctype="multipart/form-data"`. Otherwise, `request.FILES` will be empty.

### Serveal ways to upload files:

#### Binding uploaded files to a form
```
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
```

handle_uploaded_file should be like this

```
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
```
Looping over UploadedFile.chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.
[UploadedFile](https://docs.djangoproject.com/en/1.11/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile)

#### Handling uploaded files with a model

If you’re saving a file on a `Model` with a `FileField`, using a `ModelForm` makes this process much easier. The file object will be saved to the location specified by the `upload_to` argument of the corresponding `FileField` when calling `form.save()`:

```
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ModelFormWithFileField

def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return render(request, 'upload.html', {'form': form})
```
If you are constructing an object manually, you can simply assign the file object from request.FILES to the file field in the model:
```
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import ModelWithFileField

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = ModelWithFileField(file_field=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
```

#### Uploading multiple files

If you want to upload multiple files using one form field, set the multiple HTML attribute of field’s widget:

```
from django import forms

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
```

Then override the post method of your FormView subclass to handle multiple file uploads:

```
from django.views.generic.edit import FormView
from .forms import FileFieldForm

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
```

### Upload Handlers

When a user uploads a file, Django passes off the file data to an upload handler – a small class that handles file data as it gets uploaded. Upload handlers are initially defined in the `FILE_UPLOAD_HANDLERS` setting, which defaults to:
```
["django.core.files.uploadhandler.MemoryFileUploadHandler",
 "django.core.files.uploadhandler.TemporaryFileUploadHandler"]
```
Together `MemoryFileUploadHandler` and `TemporaryFileUploadHandler` provide Django’s default file upload behavior of reading small files into memory and large ones onto disk.

You can write custom handlers that customize how Django handles files. You could, for example, use custom handlers to enforce user-level quotas, compress data on the fly, render progress bars, and even send data to another storage location directly without storing it locally. See Writing custom upload handlers for details on how you can customize or completely replace upload behavior.

### Where uploaded data is stored

Before you save uploaded files, the data needs to be stored somewhere.

By default, if an uploaded file is smaller than 2.5 megabytes, Django will hold the entire contents of the upload in memory. This means that saving the file involves only a read from memory and a write to disk and thus is very fast.

However, if an uploaded file is too large, Django will write the uploaded file to a temporary file stored in your system’s temporary directory. On a Unix-like platform this means you can expect Django to generate a file called something like /tmp/tmpzfp6I6.upload. If an upload is large enough, you can watch this file grow in size as Django streams the data onto disk.

These specifics – 2.5 megabytes; /tmp; etc. – are simply “reasonable defaults” which can be customized as described in the next section.

[user uploaded content security](https://docs.djangoproject.com/en/1.11/topics/security/#user-uploaded-content-security)

### Modifying upload handlers on the fly

Sometimes particular views require different upload behavior. In these cases, you can override upload handlers on a per-request basis by modifying request.upload_handlers. By default, this list will contain the upload handlers given by `FILE_UPLOAD_HANDLERS`, but you can modify the list as you would any other list.

For instance, suppose you’ve written a ProgressBarUploadHandler that provides feedback on upload progress to some sort of AJAX widget. You’d add this handler to your upload handlers like this:

`request.upload_handlers.insert(0, ProgressBarUploadHandler(request))`

You’d probably want to use `list.insert()` in this case (instead of `append()`) because a progress bar handler would need to run before any other handlers. Remember, the upload handlers are processed in order.

If you want to replace the upload handlers completely, you can just assign a new list:

`request.upload_handlers = [ProgressBarUploadHandler(request)]`

Note

You can only modify upload handlers before accessing `request.POST` or `request.FILES` – it doesn’t make sense to change upload handlers after upload handling has already started. If you try to modify `request.upload_handlers` after reading from `request.POST` or `request.FILES` Django will throw an error.

Thus, you should always modify uploading handlers as early in your view as possible.

Also, `request.POST` is accessed by `CsrfViewMiddleware` which is enabled by default. This means you will need to use `csrf_exempt()` on your view to allow you to change the upload handlers. You will then need to use `csrf_protect()` on the function that actually processes the request. Note that this means that the handlers may start receiving the file upload before the CSRF checks have been done. Example code:
```
from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def upload_file_view(request):
    request.upload_handlers.insert(0, ProgressBarUploadHandler(request))
    return _upload_file_view(request)

@csrf_protect
def _upload_file_view(request):
    ... # Process request
```

## TextField in Form?

`TextField` in models should be implemented by `forms.CharField(widget=forms.Textarea)`

## Add text in the Placeholder of input

Look at the [widgets documentation](https://stackoverflow.com/questions/4101258/how-do-i-add-a-placeholder-on-a-charfield-in-django). Basically it would look like:
```
q = forms.CharField(label='search', 
                    widget=forms.TextInput(attrs={'placeholder': 'Search'}))
```
More writing, yes, but the separation allows for better abstraction of more complicated cases.

You can also declare a widgets attribute containing a <field name> => <widget instance> mapping directly on the Meta of your ModelForm sub-class.

```
class AuthorForm(ModelForm):
    class Meta:
        model = Author
        widgets = {
            'name': TextInput(attrs={'placeholder': 'name'}),
        }
```        
You could always create your own widget that derives from TextInput and includes the placeholder attribute, and use the widgets dictionary to simply map fields to your new widget without specifying the placeholder attribute for every field.

## Empty Label ChoiceField Django

[StackOverflow](https://stackoverflow.com/questions/14541074/empty-label-choicefield-django/14542916#14542916)

```
### forms.py
from django.forms import Form, ChoiceField

CHOICE_LIST = [
    ('', '----'), # replace the value '----' with whatever you want, it won't matter
    (1, 'Rock'),
    (2, 'Hard Place')
]

class SomeForm (Form):

    some_choice = ChoiceField(choices=CHOICE_LIST, required=False)
```

## django form with multiple file fields

```<form enctype="multipart/form-data" action="" method="post">
<input type="file" name="myfiles" multiple>
<input type="submit" name="upload" value="Upload">
</form>
```

```
for afile in request.FILES.getlist('myfiles'):
    # do something with afile
```

## Django ModelForm: What is save(commit=False) used for?

That's useful when you get most of your model data from a form, but need to populate some null=False fields with non-form data.

Saving with commit=False gets you a model object, then you can add your extra data and save it.
[a good example](https://stackoverflow.com/questions/569468/django-multiple-models-in-one-template-using-forms/575133#575133)


## Blank and Null

Here is the [difference](https://simpleisbetterthancomplex.com/tips/2016/07/25/django-tip-8-blank-or-null.html).

