# Generated by Django 4.2.6 on 2023-10-25 11:32

import appapi.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('profile_image', models.FileField(upload_to='buyer-img-store')),
                ('wallet_balance', models.FloatField(default=0.0, max_length=8)),
                ('street_address', models.TextField(default=None)),
                ('land_mark', models.TextField(default=None)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('LGA', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=15)),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('time_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'permissions': [('view_category_custom', 'Can view categories'), ('add_category_custom', 'Can add categories'), ('change_category_custom', 'Can change categories'), ('delete_category_custom', 'Can delete categories')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=350)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('image', models.FileField(upload_to='Product-img-store')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('product_description', models.TextField(default='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.category')),
            ],
            options={
                'ordering': ['-date_created'],
                'permissions': [('view_product_custom', 'Can view products'), ('add_product_custom', 'Can add products'), ('change_product_custom', 'Can change products'), ('delete_product_custom', 'Can delete products')],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appapi.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('SUCCESSFUL', 'Successful'), ('PENDING', 'Pending'), ('FAILED', 'Failed')], default='PENDING', max_length=50)),
                ('type', models.CharField(choices=[('DEBIT', 'Debit'), ('CREDIT', 'Credit')], max_length=50)),
                ('reference', models.CharField(default=appapi.models.generate_reference, max_length=50)),
                ('platform_reference', models.CharField(blank=True, max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appapi.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.FileField(upload_to='seller-img-store')),
                ('Identity', models.CharField(choices=[('School', 'SCHOOL-ID-CARD'), ('Faculty', 'FACULTY-ID-CARD')], default='SCHOOL-ID-CARD', max_length=10)),
                ('id_image', models.FileField(upload_to='ID-img-store')),
                ('phone_number', models.CharField(max_length=15)),
                ('matric_number', models.CharField(default='', max_length=50, unique=True)),
                ('university_name', models.CharField(max_length=300)),
                ('faculty', models.CharField(max_length=300)),
                ('department', models.CharField(max_length=300)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('last_login_timestamp', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sold', models.PositiveIntegerField()),
                ('total_sales', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_sold', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.seller')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.seller'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('reference', models.CharField(default=appapi.models.generate_reference, max_length=50)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=50)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appapi.product')),
                ('transaction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='appapi.transaction')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_purchase', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_purchased', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.buyer')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appapi.buyer'),
        ),
        migrations.CreateModel(
            name='CardDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(choices=[('VISA', 'VISA-CARD'), ('MASTERCARD', 'MASTERCARD')], default=None, max_length=10)),
                ('card_name', models.CharField(max_length=30)),
                ('card_number', models.IntegerField()),
                ('cvc', models.IntegerField()),
                ('pin', models.IntegerField()),
                ('card_owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='appapi.buyer')),
            ],
        ),
    ]
