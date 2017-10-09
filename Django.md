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
