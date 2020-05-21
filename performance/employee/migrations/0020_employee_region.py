# Generated by Django 2.1.7 on 2019-03-25 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0019_employee_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='region',
            field=models.CharField(choices=[('Ahafo', 'Ahafo'), ('Ashanti', 'Ashanti'), ('Bono East', 'Bono East'), ('Bono', 'Bono'), ('Central', 'Central'), ('Eastern', 'Eastern'), ('Greater', 'Greater'), ('North East', 'Northen East'), ('Northen', 'Northen'), ('Oti', 'Oti'), ('Savannah', 'Savannah'), ('Upper East', 'Upper East'), ('Upper West', 'Upper West'), ('Volta', 'Volta'), ('Western North', 'Western North'), ('Western', 'Western')], default='Greater', help_text='what region of the country(Ghana) are you from ?', max_length=20, null=True, verbose_name='Region'),
        ),
    ]
