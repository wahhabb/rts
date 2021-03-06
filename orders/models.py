from django.db import models
from comix.models import Issue
from django.contrib.auth.models import User
from localflavor.us.models import USStateField


class CartItem(models.Model):
    """ model class containing information each Product instance in the customer's shopping cart """
    cart_id = models.CharField(max_length=50, db_index=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Issue, unique=False, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']

    @property
    def total(self):
        return self.quantity * self.product.price

    @property
    def name(self):
        return str(self.product)

    @property
    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        """ called when a POST request comes in for a Product instance already in the shopping cart """
        self.quantity=self.quantity + int(quantity)
        self.save()

class BaseOrderInfo(models.Model):

    class Meta:
        abstract=True

    # contact info
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # shipping information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=40)
    state = USStateField()
    zip = models.CharField(max_length=32)


class UserProfile(BaseOrderInfo):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return 'User Profile for: ' + self.user.username


class Order(BaseOrderInfo):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    cart_id = models.CharField(max_length=50)
    date_placed = models.DateTimeField(auto_now_add=True)
    date_shipped = models.DateTimeField(null=True)
    shipping_charge = models.DecimalField(max_digits=7, decimal_places=2)
    order_total = models.DecimalField(max_digits=7, decimal_places=2)
    payment_received = models.BooleanField(default=False)
    items = models.ManyToManyField(Issue, through='IssueInOrder')

    @classmethod
    def create(cls, user_profile, cart_id, shipping_charge, order_total):
        # ToDo: Keep these in sync with base class definition--any better way??
        order = cls(
            user=user_profile.user,
            email=user_profile.email,
            phone=user_profile.phone,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            address1=user_profile.address1,
            address2=user_profile.address2,
            city=user_profile.city,
            state=user_profile.state,
            zip=user_profile.zip,
            # items not from base class
            cart_id=cart_id,
            shipping_charge=shipping_charge,
            order_total=order_total,
            date_shipped=None)
        return order


class IssueInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    sale_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField()
    issue = models.ForeignKey(Issue, on_delete=models.PROTECT)

    def total(self):
        return self.sale_price * self.quantity


class WishList(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Wish list item for: ' + self.user.username + ' ' + str(self.issue)
