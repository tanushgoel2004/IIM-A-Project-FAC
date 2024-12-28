# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import Trade
# from datetime import datetime

# def trade_form(request):
#     if request.method == 'POST':
#         # Get form data
#         trader= request.POST.get('trader_id')
#         trade_type = request.POST.get('trade_type')
#         action_type = request.POST.get('action_type')
#         bs_type = request.POST.get('bs_type')
#         limit_price = request.POST.get('limit_price')
#         quantity = request.POST.get('quantity')

#         # For Market Order, set the price logic
#         if trade_type == 'Mo':  # Market Order
#             if bs_type == 'B':  # Buy order
#                 # Get the lowest price from all Buy orders
#                 lowest_buy_price = Trade.objects.filter(bs_type='S').order_by('limit_price').first()
#                 limit_price = lowest_buy_price.limit_price if lowest_buy_price else 100
#             elif bs_type == 'S':  # Sell order
#                 # Get the highest price from all Buy orders
#                 highest_buy_price = Trade.objects.filter(bs_type='B').order_by('-limit_price').first()
#                 limit_price = highest_buy_price.limit_price if highest_buy_price else 100

#         # Create a new trade entry
#         trade = Trade(

#             trader_id=trader,
#             trade_type=trade_type,
#             action_type=action_type,
#             bs_type=bs_type,
#             limit_price=limit_price,
#             quantity=quantity,
#             time=datetime.now(),  # Automatically set current time
#             # trader_id='user123'  # Replace this with actual trader ID if available
#         )
#         trade.save()  # Save to the database

#         return redirect('/generate_trade/')  # Redirect to the home page or another page after form submission

#     else:
#         # Fetch all trades from the database for displaying in the table
#         trades = Trade.objects.all()

#         return render(request, 'trade_form.html', {'trades': trades})




# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import Trade
# from datetime import datetime

# def trade_form(request):
#     if request.method == 'POST':
#         # Get form data
#         action_type = request.POST.get('action_type')
#         sno = request.POST.get('sno', None)  # Get sno if provided
#         trader = request.POST.get('trader_id')
#         trade_type = request.POST.get('trade_type')
#         bs_type = request.POST.get('bs_type')
#         limit_price = request.POST.get('limit_price')
#         quantity = request.POST.get('quantity')

#         if action_type == 'Mod' and sno:
#             # Modify an existing trade
#             try:
#                 trade = Trade.objects.get(sno=sno)  # Get the trade by sno
#                 trade.trader_id = trader
#                 trade.trade_type = trade_type
#                 trade.bs_type = bs_type
#                 trade.limit_price = limit_price
#                 trade.quantity = quantity
#                 trade.time = datetime.now()  # Update timestamp
#                 trade.save()  # Save changes
#             except Trade.DoesNotExist:
#                 return HttpResponse("Trade with given sno not found.", status=404)
#         else:
#             # For Market Order, set the price logic
#             if trade_type == 'Mo':  # Market Order
#                 if bs_type == 'B':  # Buy order
#                     # Get the lowest price from all Sell orders
#                     lowest_sell_price = Trade.objects.filter(bs_type='S').order_by('limit_price').first()
#                     limit_price = lowest_sell_price.limit_price if lowest_sell_price else 100
#                 elif bs_type == 'S':  # Sell order
#                     # Get the highest price from all Buy orders
#                     highest_buy_price = Trade.objects.filter(bs_type='B').order_by('-limit_price').first()
#                     limit_price = highest_buy_price.limit_price if highest_buy_price else 100

#             # Create a new trade entry
#             trade = Trade(
#                 trader_id=trader,
#                 trade_type=trade_type,
#                 action_type=action_type,
#                 bs_type=bs_type,
#                 limit_price=limit_price,
#                 quantity=quantity,
#                 time=datetime.now(),  # Automatically set current time
#             )
#             trade.save()  # Save to the database

#         return redirect('/generate_trade/')  # Redirect to the home page or another page after form submission

#     else:
#         # Fetch all trades from the database for displaying in the table
#         trades = Trade.objects.all()

#         return render(request, 'trade_form.html', {'trades': trades})






from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Trade
from datetime import datetime

def trade_form(request):
    if request.method == 'POST':
        # Get form data
        action_type = request.POST.get('action_type')
        sno = request.POST.get('sno', None)  # Get sno if provided

        if action_type == 'Cancel' and sno:
            # Cancel (delete) an existing trade
            try:
                trade = Trade.objects.get(sno=sno)  # Get the trade by sno
                trade.delete()  # Delete the trade
                return redirect('/generate_trade/')  # Redirect after deletion
            except Trade.DoesNotExist:
                return HttpResponse("Trade with given sno not found.", status=404)

        elif action_type == 'Mod' and sno:
            # Modify an existing trade
            try:
                trade = Trade.objects.get(sno=sno)  # Get the trade by sno
                trade.trader_id = request.POST.get('trader_id')
                trade.trade_type = request.POST.get('trade_type')
                trade.bs_type = request.POST.get('bs_type')
                trade.limit_price = request.POST.get('limit_price')
                trade.quantity = request.POST.get('quantity')
                trade.time = datetime.now()  # Update timestamp
                trade.save()  # Save changes
            except Trade.DoesNotExist:
                return HttpResponse("Trade with given sno not found.", status=404)

        else:
            # Handle new trade creation or Market Order logic
            trader = request.POST.get('trader_id')
            trade_type = request.POST.get('trade_type')
            bs_type = request.POST.get('bs_type')
            limit_price = request.POST.get('limit_price')
            quantity = request.POST.get('quantity')

            if trade_type == 'Mo':  # Market Order
                if bs_type == 'B':  # Buy order
                    lowest_sell_price = Trade.objects.filter(bs_type='S').order_by('limit_price').first()
                    limit_price = lowest_sell_price.limit_price if lowest_sell_price else 100
                elif bs_type == 'S':  # Sell order
                    highest_buy_price = Trade.objects.filter(bs_type='B').order_by('-limit_price').first()
                    limit_price = highest_buy_price.limit_price if highest_buy_price else 100

            # Create a new trade entry
            trade = Trade(
                trader_id=trader,
                trade_type=trade_type,
                action_type=action_type,
                bs_type=bs_type,
                limit_price=limit_price,
                quantity=quantity,
                time=datetime.now(),  # Automatically set current time
            )
            trade.save()  # Save to the database

        return redirect('/generate_trade/')  # Redirect to the home page or another page after form submission

    else:
        # Fetch all trades from the database for displaying in the table
        trades = Trade.objects.all()

        return render(request, 'trade_form.html', {'trades': trades})
