from main.models import *
from vendor.models import *
from nabl.models import *
from tkc.models import *
from rca.models import *
from django import template

register = template.Library()


@register.filter(name='contractor_class')
def contractor_class(data, name):
    for name in name:
        if int(data.Oyt) == name.id:
            return name.Name
    return False;


@register.filter(name='reg_date')
def reg_date(data, name):
    for name in name:
        if int(data.Oyt) == name.id:
            return name.Name
    return False;


@register.filter(name='last_date',new_data=0)
def last_date(data, name):
    for name in name:
        if int(data.User_Id) == int(name.user_id):
            return name.Doc_expiry_date
    return False;

# @register.filter(name='cart_quantity')
# def cart_quantity(product, cart):
#     keys = cart.keys()
#     for id in keys:
#         if int(id) == product.Product_id:
#             return cart.get(id)
#     return 0;
#
#
# @register.filter(name='cart_length')
# def cart_length(product, cart):
#     return len(cart);
#
#
# @register.filter(name='cart_subtotal')
# def cart_subtotal(product, cart):
#     keys = cart.keys()
#     subtotal = 0;
#     for key in keys:
#         for p_id in product:
#             if int(key) == p_id.Product_id:
#                 quantity = cart.get(key)
#                 subtotal = subtotal + p_id.Product_Sale_Price * int(quantity)
#     return subtotal;
#
#
# @register.filter(name='cart_total_saving')
# def cart_total_saving(product, cart):
#     keys = cart.keys()
#     total_saving = 0;
#     for key in keys:
#         for p_id in product:
#             if int(key) == p_id.Product_id:
#                 quantity = cart.get(key)
#                 total_saving = total_saving + (p_id.Product_MRP - p_id.Product_Sale_Price) * int(quantity)
#     return total_saving;
#
#
# @register.filter(name='cart_total')
# def cart_total(product, cart):
#     keys = cart.keys()
#     total = 0;
#     for key in keys:
#         for p_id in product:
#             if int(key) == p_id.Product_id:
#                 quantity = cart.get(key)
#                 total = total + p_id.Product_Sale_Price * int(quantity)
#     return total;
#
#
# @register.filter(name='item_price')
# def item_price(product, cart):
#     keys = cart.keys()
#     total = 0;
#     for key in keys:
#         for p_id in product:
#             if int(key) == p_id.Product_id:
#                 quantity = cart.get(key)
#                 total = p_id.Product_Sale_Price * int(quantity)
#     return total;

@register.filter
def modulo(num, val):
    return num % val
