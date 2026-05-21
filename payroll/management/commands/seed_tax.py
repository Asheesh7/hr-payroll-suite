from django.core.management.base import BaseCommand
from payroll.models import TaxConfig
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed Australian tax brackets for 2025-26'

    def handle(self, *args, **kwargs):
        TaxConfig.objects.all().delete()
        brackets = [
            (0, 18200, 0),
            (18201, 45000, 19),
            (45001, 120000, 32.5),
            (120001, 180000, 37),
            (180001, 999999999, 45),
        ]
        for min_i, max_i, rate in brackets:
            TaxConfig.objects.create(
                financial_year='2025-26',
                min_income=Decimal(str(min_i)),
                max_income=Decimal(str(max_i)),
                tax_rate=Decimal(str(rate))
            )
            self.stdout.write(f'Added bracket: {min_i} - {max_i} @ {rate}%')
        self.stdout.write(self.style.SUCCESS('Tax brackets seeded successfully.'))
