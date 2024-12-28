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
from .models import Trade,TradeSummary
from datetime import datetime
from decimal import Decimal


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
                trade_type=request.POST.get('trade_type')
                bs_type=request.POST.get('bs_type')
                trade.bs_type = request.POST.get('bs_type')
                trade.limit_price = request.POST.get('limit_price')
                trade.quantity = request.POST.get('quantity')
                trade.time = datetime.now()  # Update timestamp   
                if trade_type == 'Mo':  # Market Order
                    if bs_type == 'B':  # Buy order
                        lowest_sell_price = Trade.objects.filter(bs_type='S').order_by('limit_price').first()
                        trade.limit_price = lowest_sell_price.limit_price if lowest_sell_price else 100
                    elif bs_type == 'S':  # Sell order
                        highest_buy_price = Trade.objects.filter(bs_type='B').order_by('-limit_price').first()
                        trade.limit_price = highest_buy_price.limit_price if highest_buy_price else 100

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


            if bs_type == 'B':
                lowest_sell_price = Trade.objects.filter(bs_type='S').order_by('limit_price').first()
                if(int(lowest_sell_price.limit_price)<int(limit_price)):
                    buyer_id=trader
                    seller_id=lowest_sell_price.trader_id
                    price=lowest_sell_price.limit_price
                    quantity_executed=min(int(lowest_sell_price.quantity),int(quantity))

                    q=int(lowest_sell_price.quantity-quantity_executed)
                    lowest_sell_price.quantity = str(q)
                    q=int(quantity)-quantity_executed
                    quantity=str(q)
                    lowest_sell_price.save()

                    if(int(lowest_sell_price.quantity)==0):
                        lowest_sell_price.delete()



                    executed_trade=TradeSummary(
                        buy_id=buyer_id,
                        sell_id=seller_id,
                        price=price,
                        quantity=quantity_executed,
                        time=datetime.now(),
                    )
                    if buyer_id != seller_id:
                        executed_trade.save()

            if bs_type == 'S':
                lowest_sell_price = Trade.objects.filter(bs_type='B').order_by('-limit_price').first()
                if(int(lowest_sell_price.limit_price)>int(limit_price)):
                    seller_id=trader
                    buyer_id=lowest_sell_price.trader_id
                    price=lowest_sell_price.limit_price
                    quantity_executed=min(int(lowest_sell_price.quantity),int(quantity))

                    q=int(lowest_sell_price.quantity-quantity_executed)
                    lowest_sell_price.quantity = str(q)
                    q=int(quantity)-quantity_executed
                    quantity=str(q)
                    lowest_sell_price.save()

                    if(int(lowest_sell_price.quantity)==0):
                        lowest_sell_price.delete()



                    executed_trade=TradeSummary(
                        buy_id=buyer_id,
                        sell_id=seller_id,
                        price=price,
                        quantity=quantity_executed,
                        time=datetime.now(),
                    )
                    if(buyer_id != seller_id):
                        executed_trade.save()

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
            if(int(quantity) != 0):
                trade.save()  # Save to the database

        return redirect('/generate_order/')  # Redirect to the home page or another page after form submission

    else:
        # Fetch all trades from the database for displaying in the table
        trades = Trade.objects.all()
        trade_summaries = TradeSummary.objects.all()

        return render(request, 'trade_form.html', {
            'trades': trades,
            'trade_summaries': trade_summaries,
        })




from django.shortcuts import render
from .models import Trade, TradeSummary

def current_progress(request):
    # Fetch unique trader IDs for the dropdown
    trader_ids = Trade.objects.values_list('trader_id', flat=True).distinct()

    # Fetch trades and trade summaries
    trades = Trade.objects.all()
    trade_summaries = TradeSummary.objects.all()

    # Handle filters for trades
    trade_type_filter = request.GET.get('trade_type', 'All')  # Trade Type filter
    bs_type_filter = request.GET.get('bs_type', 'All')  # Buy/Sell filter
    trader_filter = request.GET.get('trader_id', 'All')  # Trader ID filter

    if trade_type_filter != 'All':
        trades = trades.filter(trade_type=trade_type_filter)

    if bs_type_filter != 'All':
        trades = trades.filter(bs_type=bs_type_filter)

    if trader_filter != 'All':
        trades = trades.filter(trader_id=trader_filter)

    # Handle filters for trade summaries
    buyer_filter = request.GET.get('buyer_id', 'All')  # Buyer ID filter
    seller_filter = request.GET.get('seller_id', 'All')  # Seller ID filter

    if buyer_filter != 'All':
        trade_summaries = trade_summaries.filter(buy_id=buyer_filter)

    if seller_filter != 'All':
        trade_summaries = trade_summaries.filter(sell_id=seller_filter)

    # Render template with data
    return render(request, 'viewing.html', {
        'trades': trades,
        'trade_summaries': trade_summaries,
        'trader_ids': trader_ids,
        'trade_type_filter': trade_type_filter,
        'bs_type_filter': bs_type_filter,
        'trader_filter': trader_filter,
        'buyer_filter': buyer_filter,
        'seller_filter': seller_filter,
    })
