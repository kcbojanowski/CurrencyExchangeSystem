from datetime import datetime, timedelta
from decimal import Decimal
from nbpy import NBPClient
from nbpy.errors import APIError


class Invoice(object):
    """Invoice class with builtin currency converter."""

    def __init__(self, currency_code, date, amount):
        self.currency_code = currency_code
        self.date = date
        self.amount = Decimal("{:.2f}".format(amount))
        self._nbp = NBPClient(currency_code)

    @property
    def amount_in_pln(self):
        exchange_rate = None
        date = datetime.strptime(self.date, '%Y-%m-%d')
        while exchange_rate is None:
            # Get exchange rates until valid is found
            try:
                exchange_rate = self._nbp.date(date.strftime('%Y-%m-%d'))
                break
            except APIError:
                date -= timedelta(days=1)

        amount = (exchange_rate * self.amount)['mid']
        return round(amount, 2)


if __name__ == '__main__':
    euros = Invoice('EUR', '2022-08-05', 562.63)
    print(euros.amount_in_pln)
