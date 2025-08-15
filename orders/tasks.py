from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created_email(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Заказ #{order.id} - Domus Aurea'
    message = f'Уважаемый {order.first_name},\n\n' \
              f'Вы успешно разместили заказ.\n' \
              f'Номер вашего заказа: {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'noreply@domusaurea.com',
                          [order.email])
    return mail_sent