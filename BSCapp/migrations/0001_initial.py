# Generated by Django 2.0 on 2018-03-08 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=20)),
                ('admin_pwd', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField()),
                ('timestamp', models.CharField(max_length=32)),
                ('block_size', models.FloatField()),
                ('tx_number', models.IntegerField()),
                ('block_hash', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('coin_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('owner_id', models.CharField(max_length=64)),
                ('is_spent', models.BooleanField(default=False)),
                ('timestamp', models.CharField(max_length=32)),
                ('coin_credit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('data_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=64)),
                ('data_name', models.CharField(max_length=64)),
                ('data_info', models.CharField(max_length=200)),
                ('timestamp', models.CharField(max_length=32)),
                ('data_source', models.CharField(max_length=20)),
                ('data_type', models.CharField(max_length=20)),
                ('data_tag', models.CharField(max_length=100)),
                ('data_status', models.IntegerField(default=0)),
                ('data_md5', models.CharField(max_length=64)),
                ('data_size', models.FloatField()),
                ('data_download', models.IntegerField(default=0)),
                ('data_purchase', models.IntegerField(default=0)),
                ('data_price', models.FloatField()),
                ('data_address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_id', models.CharField(max_length=64)),
                ('user_name', models.CharField(max_length=20)),
                ('ratio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('notice_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('sender_id', models.CharField(max_length=64)),
                ('receiver_id', models.CharField(max_length=64)),
                ('notice_type', models.IntegerField()),
                ('notice_info', models.CharField(max_length=200)),
                ('if_check', models.BooleanField(default=False)),
                ('timestamp', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=64)),
                ('data_id', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Recharge',
            fields=[
                ('recharge_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=64)),
                ('timestamp', models.CharField(max_length=32)),
                ('credits', models.FloatField()),
                ('before_account', models.FloatField()),
                ('after_account', models.FloatField()),
                ('coin_id', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_id', models.CharField(max_length=64)),
                ('data_id', models.CharField(max_length=64)),
                ('review_status', models.IntegerField()),
                ('timestamp', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('buyer_id', models.CharField(max_length=64)),
                ('seller_id', models.CharField(max_length=64)),
                ('data_id', models.CharField(max_length=64)),
                ('timestamp', models.CharField(max_length=32)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('user_pwd', models.CharField(max_length=20)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_realName', models.CharField(max_length=20)),
                ('user_phone', models.CharField(max_length=20)),
                ('user_idcard', models.CharField(max_length=20)),
                ('user_company', models.CharField(max_length=64)),
                ('user_title', models.CharField(max_length=20)),
                ('user_addr', models.CharField(default='China', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('user_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('account', models.FloatField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('reviewer_id', 'data_id')},
        ),
        migrations.AlterUniqueTogether(
            name='purchase',
            unique_together={('user_id', 'data_id')},
        ),
        migrations.AlterUniqueTogether(
            name='income',
            unique_together={('data_id', 'user_name')},
        ),
    ]
