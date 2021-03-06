## chapter 20 属性描述符

**主要内容**

- [x] 描述符

#### 1、什么是描述符？

* 描述符是对多个属性运行相同存储逻辑的一种方式；
* 描述符是是实现了特定协议的类，这个协议包括`__get__`、`__set__`和`__delete__`方法；
* 描述符是Python独有的特征，不仅在应用层使用，在语言的基础设施中也运用到；
* Python中使用描述符的地方包括：特性（Property类，实现了完整的描述符协议，属于覆盖性描述符）、方法(实例方法只实现了`__get__`方法，属于非覆盖性描述符)以及classmethod、staticmethod装饰器。

#### 2、描述符相关使用介绍

```
class Quantity:
    """
    descriptor 描述符类
    """

    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem:
    """
    托管类
    """

    weight = Quantity('weight')  # 描述符实例 weight
    price = Quantity('price')  # 描述符实例price

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
```

* 描述符类：实现描述符协议的类，在代码中为Quantity类；
* 托管类： 把描述符类实例声明为类属性的类，在代码中为LineItem类；
* 描述符实例：描述符类的各个实例，声明为托管类的类属性；
* 托管实例：托管类的实例，代码中指的是LineItem类的属性；
* 储存属性：托管实例中储存自身托管属性的属性，在代码中为LineItem实例的weight和price属性。这种属性与描述符属性的weight和price不同，它们为类属性。
* 托管属性：托管类中由描述符实例处理的公开属性，值存储在储存属性中。也就是说，描述符实例i和储存属性为托管属性建立了基础。

#### 3、覆盖性描述符与非覆盖性描述符对比

> 概述：Python存取属性的方式特别不对等，通过实例读取属性时，通常返回的是实例中定义的属性；但是如果实例中没有指定的属性，那么会获取类属性。而为实例的属性赋值时，通常会在实例中创建属性，根本不影响类。

01、描述符如何进行分类？

根据是否定义`__set__`方法，描述符可分为两大类，定义了`__set__`方法的为覆盖性描述符，否则为非覆盖性描述符。

覆盖型描述符也叫数据描述符或强制描述符，非覆盖型描述符也叫非数据描述符或遮盖型描述符。


02、两种描述符使用中由什么区别?

* 覆盖型描述符(实现`__set__`和`__get__`方法)，不管是通过托管类访问属性还是实例访问属性都会通过描述符类的`__get__`方法，而且通过实例设置同名描述符类实例属性会通过描述符类的`__set__`方法；
* 覆盖型描述符(只实现`__set__`方法)，通过实例设置同名描述符类实例属性会通过描述符类的`__set__`方法，访问属性返回的均为描述符类对象本身，读取时只要由同名实例属性，描述符就会被遮盖；
* 非覆盖型描述符，描述符实例与托管实例存在同名属性，读取同名实例属性时描述符就会被遮盖，通过托管类读取描述符实例属性时，依然会通过描述符类。

03、在类中覆盖描述符

不管描述符是覆盖型还是非覆盖型，只要为类属性赋值都能覆盖描述符。

04、方法是描述符

在类中定义的函数属于绑定方法（bound method），因为 用户定义的函数都有`__get__`方法，所以依附到类上时，就相当于描述符。

#### 4、描述符使用建议

* 01、使用特性保持简单：内置的property类创建的都是覆盖型描述符。特性的`__set__`方法默认抛出`Attribute: can't set attribute`。因此创建只读属性最简单的方式是使用特性。
* 02、只读描述符必须有`__set__`方法：因为如果不实现，实例的同名属性会覆盖描述符。只读属性的`__set__`方法只需抛出`AttributeError`异常，并提供合适的错误消息。
* 03、用于验证的描述符可以只有`__set__`方法：对仅用于验证的描述符来说，`__set__`方法应该检查value参数获得的值，如果有效，使用描述符实例的名称为键，直接在实例的`__dict__`属性中设置。
* 04、仅有`__get__`方法的描述符可以实现高效缓存：这种描述符可用于执行某些耗费资源的计算，然后为实例设置同名属性缓存结果。由于同名属性会遮盖描述符，因此后续访问会直接从实例的`__dict__`属性中获取值，而不会触发描述符的`__get__`方法。
* 05、非特殊的方法可以被实例属性覆盖：由于函数或方法只实现了`__get__`方法，所以它们不会处理同名实例属性的赋值操作。

```
—— 整理人Fenghui
—— 整理时间：2019-03-21
```