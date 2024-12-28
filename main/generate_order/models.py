from django.db import models

class Trade(models.Model):
    sno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)  # Automatically set to current time
    trader_id = models.CharField(max_length=50)
    trade_type = models.CharField(
        max_length=2,
        choices=[("Lo", "Limit Order"), ("Mo", "Market Order")]
    )
    action_type = models.CharField(
        max_length=3,
        choices=[("New", "New"), ("Mod", "Modify"), ("Can", "Cancel")]
    )
    bs_type = models.CharField(
        max_length=1,
        choices=[("B", "Buy"), ("S", "Sell")]
    )
    limit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Trade {self.sno} by {self.trader_id} ({self.trade_type}, {self.action_type})"


class TradeSummary(models.Model):
    sno = models.AutoField(primary_key=True)
    buy_id = models.CharField(max_length=50)
    sell_id = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TradeSummary {self.sno} (Buy: {self.buy_id}, Sell: {self.sell_id})"
