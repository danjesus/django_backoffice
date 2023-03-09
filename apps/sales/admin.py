from django.conf import settings
from admin_site import admin
from apps.sales.models import Seller, Order, OrderedProduct
from apps.tasks_pipeline.tasks import pipeline_runner


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class OrderedProductInLine(admin.TabularInline):
    model = OrderedProduct
    extra = 0
    min_num = 1
    autocomplete_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # listing view
    list_display = ('code', 'customer', 'status', 'seller',
                    'total_price', 'total_weight', 'total_seller_commission',
                    'packing_slip_file', 'order_created_at')
    search_fields = ('customer__name',)
    ordering = ('-id',)
    list_filter = ('status', 'seller')

    # listing actions
    actions = ('run_order_pipeline_again',)

    # create/edit view
    autocomplete_fields = ('customer', 'seller')
    inlines = (OrderedProductInLine,)

    def total_price(self, obj):
        return '${0:.2f}'.format(obj.order_total_price())

    def total_weight(self, obj):
        return '{0:.2f}lb'.format(obj.order_total_weight())

    def total_seller_commission(self, obj):
        return '{0:.2f}%'.format(obj.order_total_seller_commission())

    def order_created_at(self, obj):
        return obj.created_at.strftime(settings.DEFAULT_TIME_FORMAT)

    @admin.action(description='Run tasks from order pipeline again')
    def run_order_pipeline_again(self, request, queryset):
        for order in queryset.all():
            pipeline_runner.delay(model_class_ref='sales.Order', instance_pk=order.pk)
