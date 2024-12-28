from generate_order.models import Trade, TradeSummary

# Delete all entries
Trade.objects.all().delete()
TradeSummary.objects.all().delete()

print("Tables cleared successfully!")
