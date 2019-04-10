#!/usr/bin/python3
# -*- coding:utf-8 -*- 
# @author FH
# @email: capricorn1203@126.com
# @time: 2019/3/23 10:18
import abc


class AutoStorage:

    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):

    def validate(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value


class NonBlank(Validated):

    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError('value cannot be empty or blank')
        return value


class EntityMeta(type):
    """元类，用于创建带有验证字段的业务尸体"""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in cls.__dict__.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)


class Entity(metaclass=EntityMeta):
    """"带有验证字段的业务实体"""
