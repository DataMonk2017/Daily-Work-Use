# 10.9.2017

There is no 'built in' way to do this. Django will raise the DoesNotExist exception every time. The idiomatic way to handle this in python is to wrap it in a try catch:
```python
try:
    go = SomeModel.objects.get(foo='bar')
except SomeModel.DoesNotExist:
    go = None
```    
What I did do, is to subclass models.Manager, create a safe_get like the code above and use that manager for my models. That way you can write: SomeModel.objects.safe_get(foo='bar').
