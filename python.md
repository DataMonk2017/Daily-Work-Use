# Sea in python

## difference between abs and math.fabs
`math.fabs()` converts its argument to float if it can (if it can't, it throws an exception). It then takes the absolute 
value, and returns the result as a float.

In addition to floats, `abs()` also works with integers and complex numbers. Its return type depends on the type of its
 argument.
 
## Getting key with maximum value in dictionary?

```
import operator:
stats = {'a':1000, 'b':3000, 'c': 100}
max(stats.iteritems(), key=operator.itemgetter(1))[0]
No operator way:
max(stats, key=lambda key: stats[key])
```

## How to merge lists into a list of tuples?
```
zip(list_a, list_b) #zip function stops at the end of the shortest list, which may not be always what you want.
zip_longest() 
```
the itertools module defines a zip_longest() method which stops at the end of the longest list, filling missing values with something you provide as a paramete

## python class和class(object)用法区别

```python

# 经典类或者旧试类

class A:
    pass


a = A()


# 新式类

class B(object):
    pass


b = B()

# python2不支持
# print(A.__class__)
print(a.__class__)
print(type(A))
print(type(a))

# python2
# __main__.A
# <type 'classobj'>
# <type 'instance'>

# python3
# <class 'type'>
# <class '__main__.A'>
# <class 'type'>
# <class '__main__.A'>

print(B.__class__)
print(b.__class__)
print(type(B))
print(type(b))

# python2
# <type 'type'>
# <class '__main__.B'>
# <type 'type'>
# <class '__main__.B'>

# python3
# <class 'type'>
# <class '__main__.B'>
# <class 'type'>
# <class '__main__.B'>


# 旧式类的实现不够好，类是类，实例是实例，类的类型是classobj，实例的类型是instance，两者的联系只在于__class__，
# 这和内置对象是不同的，int对象的类型就是int，同时int()返回的也是int类型的对象，内置对象和自定义对象不同就对代码统一实现带来很大困难。
#
# 新式类
#
# 1. 所有类的类型都是type
# 2. 所有类调用的结果都是构造，返回这个类的实例
# 3. 所有类都是object的子类
# 4. 新式类不仅可以用旧类调用父类的方法，也可以用super方法。

```

## 使用virtualenv这样的虚拟环境，好处或者说必要性在哪里？

为了解决python包管理的一个设计缺陷，包不能装在项目目录，导致不同的项目会发生包版本冲突。 

如果你的一台服务器，能保证只运行一个服务的话，那么确实是可以直接装在系统上的。不是的话，就涉及到多个服务的依赖和兼容问题了。比如一个系统里同时部署两个服务，一个是Django 1.4的，一个是Django 1.7的，怎么办？上面这种还是比较直观的，有这种需求的时候，肯定就会知道去用virtualenv之类的，但是另外一种情况就更可怕。需要同时部署A和B两个项目，A项目要用到a这个库，而a这个库又依赖于c这个库的1.0版本。同时呢，B项目需要用到b这个库，b又依赖于c的2.0版本，这时候如果都安装在系统上的话， 就不一定是哪个坏掉了。为了不发生这种可能的情况，尽量的保证模块的独立性，会避免很多可能发生的并且是完全不必要的坑。

##  Why does python use 'else' after for and while loops?

A common construct is to run a loop until something is found and then to break out of the loop. The problem is that if I break out of the loop or the loop ends I need to determine which case happened. One method is to create a flag or store variable that will let me do a second test to see how the loop was exited.

For example assume that I need to search through a list and process each item until a flag item is found and then stop processing. If the flag item is missing then an exception needs to be raised.

Using the Python `for`...`else` construct you have

```python
for i in mylist:
    if i == theflag:
        break
    process(i)
else:
    raise ValueError("List argument missing terminal flag.")
```

Compare this to a method that does not use this syntactic sugar:
```python
flagfound = False
for i in mylist:
    if i == theflag:
        flagfound = True
        break
    process(i)

if not flagfound:
    raise ValueError("List argument missing terminal flag.")
```

n the first case the raise is bound tightly to the for loop it works with. In the second the binding is not as strong and errors may be introduced during maintenance.