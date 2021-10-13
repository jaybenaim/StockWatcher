from datetime import datetime, timedelta
import json
import re
from django.core import serializers
from django.db.models.fields import mixins
from StockWatcher.lib.helpers.stockWatcher.Autocomplete import TickerAutocomplete
from StockWatcher.lib.helpers.stockWatcher.LiveUpdate import LivePriceUpdate
from StockWatcher.lib.helpers.stockWatcher.Messaging.twilio_notifications.middleware import (
    MessageClient,
)
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import SendMessageForm, TickrAutocomplete, WatchStockForm
from .models import Image, Profile, Ticker, TickerWatcher
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, permissions, mixins
from mainApp.serializers import (
    ImageSerializer,
    ProfileSerializer,
    TickerSerializer,
    TickerWatcherSerializer,
    UserSerializer,
    GroupSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API - Users
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Create a user and profile in the django db and return the User"""
        # print(request.data)
        # is_login = request.data['is_login']
        data = request.data

        email = data["email"]
        username = data["username"]
        # Get or Create the user
        user = User.objects.get_or_create(email=email)[0]

        new_profile = Profile.objects.get_or_create(user_id=user.id)[0]

        new_profile_serializer = ProfileSerializer(
            new_profile, many=False, context={"request": request}
        )

        if not new_profile.display_name:
            new_profile.display_name = username

        if "avatar" in data.keys():
            avatar = data["avatar"]

            if "as_url" in avatar.keys():
                new_profile.avatar = Image.objects.get_or_create(
                    as_url=avatar["as_url"]
                )[0]

        new_profile.save()

        return JsonResponse(
            {
                "id": user.id,
                "email": user.email,
                "profile": new_profile_serializer.data,
            }
        )


# Create your views here.
class ImageViewSet(viewsets.ModelViewSet):
    """
    API - Image Upload
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Image upload"""
        print(request)

        return JsonResponse({})


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API - Profiles
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get Profiles by user id"""
        query_param = self.request.query_params.get("user")

        if query_param:
            return Profile.objects.filter(user__id=query_param)
        else:
            return Profile.objects.all()

    def update(self, request, *args, **kwargs):
        profile_id = kwargs["pk"]
        profile = get_object_or_404(Profile, pk=profile_id)
        profile_serializer = ProfileSerializer(
            profile, many=False, context={"request": request}
        )

        data = request.data
        if "avatar" in data.keys():
            avatar = data["avatar"]

            if "as_url" in avatar.keys():
                profile.avatar = Image.objects.get_or_create(as_url=avatar["as_url"])[0]

            profile.save()

            return JsonResponse(profile_serializer.data)
        else:

            for property_to_update in data.keys():
                if property_to_update == "username":
                    print("username", data["username"])
                    profile.display_name = data["username"]
                if property_to_update == "email":
                    user = User.objects.get(id=profile.user.id)
                    user.email = data["email"]
                    user.save()
                    profile.user = user
                if property_to_update not in ["username", "email"]:
                    setattr(profile, property_to_update, data[property_to_update])
            print("username2", profile.display_name)

            profile.save()
            print("username2", profile.display_name)
            return JsonResponse(profile_serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API - Groups
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# class TickerviewSet(viewsets.ModelViewSet):
#   """
#   API - Ticker
#   """

#   queryset = Ticker.objects.all()
#   serializer_class = TickerSerializer
#   permission_classes = [permissions.IsAuthenticated]

# class RecentTickerView(generics.ListAPIView):
#   serializer_class = TickerSerializer

#   def get_queryset(self):
#     """Return the most recently updated tickers from the past 24 hours"""
#     yesterday = datetime.now() - timedelta.days(1)
#     return Ticker.objects.filter(updated_at__gt=yesterday)


class TickerviewSet(viewsets.ModelViewSet):
    """
    API - Ticker
    """

    serializer_class = TickerSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Return 20 tickers from the most recently updated tickers"""

        if self.request.method == "GET":
            if self.request.query_params.get("all") == "true":
                return Ticker.objects.all()
            else:
                tickers = []
                for ticker in Ticker.objects.all():
                    if ticker.is_recent():
                        tickers.append(ticker)
                if len(tickers) == 0:
                    return Ticker.objects.all().order_by("-updated_at")
                return tickers

    def create(self, request, *args, **kwargs):
        return HttpResponseBadRequest("Cannot create tickers.")

    def update(self, request, *args, **kwargs):
        return HttpResponseBadRequest("Cannot update tickers.")

    def destroy(self, request, *args, **kwargs):
        return HttpResponseBadRequest("Cannot destroy tickers.")


class TickerWatcherViewSet(viewsets.ModelViewSet):
    """
    API - All Ticker Watchers
    """

    permission_classes = [permissions.AllowAny]
    queryset = TickerWatcher.objects.all()
    serializer_class = TickerWatcherSerializer

    def get_queryset(self):
        email = self.request.GET.get("email")
        symbol = self.request.GET.get("symbol")

        if symbol:
            symbol = symbol.strip()

        if symbol == None and email:
            watchers = TickerWatcher.objects.filter(user__email=email)
        if symbol and email:
            print("getting both")
            watchers = TickerWatcher.objects.filter(
                ticker__symbol__icontains=symbol, user__email=email
            )
        else:
            watchers = TickerWatcher.objects.all()

        return watchers


class TickrAutocomplete(FormView):
    template_name = "./index.html"
    form_class = TickrAutocomplete
    ticks = []

    def set_ticks(self):
        ticker_watchers = TickerWatcher.objects.filter(
            watcher__id=self.request.user.id
        ).order_by("updated_at")

        ticks = []
        for tick in ticker_watchers.all():
            ticks.append(
                {
                    "id": tick.id,
                    "ticker_id": tick.ticker.id,
                    "symbol": tick.ticker.symbol,
                    "current_price": tick.ticker.price,
                    "min_price": tick.min_price,
                    "max_price": tick.max_price,
                    "last_updated": tick.ticker.updated_at,
                }
            )

            self.ticks = ticks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.set_ticks()
        context["ticker_watchers"] = self.ticks

        return context

    def form_valid(self, form):
        query = form.cleaned_data.get("query")

        autocomplete = TickerAutocomplete(query=query)
        results = autocomplete.get_results(query)
        symbols = autocomplete.get_symbols(query)
        self.set_ticks()

        context = {"data": results, "ticker_watchers": self.ticks}

        return JsonResponse(context)


class LivePriceUpdateView(View):
    def get(self, request):
        symbol = request.GET["symbol"]

        # if self.request.user.is_superuser:
        live_update = LivePriceUpdate(symbol=symbol.upper(), yahoo_init=symbol.upper())
        price = live_update.get_quote_from_yahoo()
        # live_update.subscribe()
        # live_update.get_bars()

        return JsonResponse({"price": price})

    # else:
    #   return JsonResponse({ 'error': 'Please sign in as a superuser.' })


class WatchStockView(View):
    def get(self, request, symbol):
        symbol = request.GET["symbol"]
        price = request.GET["price"]

        request.session["symbol"] = symbol
        request.session["price"] = price

        if self.request.user.is_superuser:
            return HttpResponseRedirect(
                reverse(
                    "mainApp:watch_stock", kwargs={"symbol": symbol, "price": price}
                )
            )
        else:
            return render(
                self.request,
                template_name="./watch_stock.html",
                context={"error": "Please sign in to save a new ticker"},
            )


class WatchStockFormView(FormView):
    template_name = "./watch_stock.html"
    form_class = WatchStockForm

    def get_context_data(self, **kwargs):
        symbol = self.request.GET["symbol"]
        price = self.request.GET["price"]

        context = super().get_context_data(**kwargs)
        context["symbol"] = symbol

        ticker_watchers = TickerWatcher.objects.filter(
            watcher__id=self.request.user.id
        ).order_by("updated_at")

        ticks = []
        for tick in ticker_watchers.all():
            ticks.append(
                {
                    "id": tick.id,
                    "ticker_id": tick.ticker.id,
                    "symbol": tick.ticker.symbol,
                    "current_price": tick.ticker.price,
                    "min_price": tick.min_price,
                    "max_price": tick.max_price,
                    "last_updated": tick.ticker.updated_at,
                }
            )

        context["ticker_watchers"] = ticks

        return context

    def form_valid(self, form):
        request_symbol = self.kwargs["symbol"]
        updated_price = self.kwargs["price"]
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        print(updated_price)

        # Get ticker or create ticker
        # ticker = get_object_or_404(Ticker, symbol=request_symbol)
        # print(updated_price, request_symbol)
        # autocomplete = TickerAutocomplete(request_symbol)
        # live_update = LivePriceUpdate(request_symbol)
        # ticker_info = autocomplete.get_name_from_symbol()
        # ticker_updated_price = live_update.get_quote_from_yahoo()

        # GET/CREATE Ticker
        # ticker, new_ticker_created = Ticker.objects.get_object_or_404(
        #     symbol = request_symbol
        #   )
        current_ticker = {}

        try:
            ticker = get_object_or_404(Ticker, symbol=request_symbol)
            ticker.price = updated_price
            ticker.save()
            current_ticker = ticker
        except:
            print("No Ticker found, creating new Ticker")

            try:
                ticker = Ticker(symbol=request_symbol, price=updated_price)
                ticker.save()
                current_ticker = ticker
            except:
                print("Problem creating new ticker")
                return render(
                    self.request,
                    template_name=self.template_name,
                    context={"error": "Problem creating new ticker."},
                )

        try:
            # GET/CREATE TickerWatcher
            new_ticker_watcher = TickerWatcher(
                user=self.request.user,
                ticker=current_ticker,
                min_price=min_price,
                max_price=max_price,
            )

            new_ticker_watcher.save()

            self.request.session["success"] = True
            print("new watcher created")
        except:
            self.request.session["success"] = False
            print("new watcher failed")
            return render(
                self.request,
                template_name=self.template_name,
                context={
                    "symbol": request_symbol,
                    "price": updated_price,
                    "error": "New watcher failed to save",
                },
            )

        return HttpResponseRedirect(
            reverse(
                "mainApp:watch_stock",
                kwargs={"symbol": request_symbol, "price": updated_price},
            )
        )

    def form_invalid(self, form):
        self.request.session["success"] = False
        print("invalid form submission")
        return HttpResponseRedirect(self.request.path)


class SendMessageFormView(FormView):
    """For Testing Only"""

    template_name = "./send_message.html"
    form_class = SendMessageForm

    # def get_context_data(self, **kwargs):
    #   live_update = LivePriceUpdate()
    #   watcher_list = live_update.send_price_alert()
    #   return { 'watcher_list': watcher_list }

    def form_valid(self, form):
        to = form.cleaned_data.get("to")
        message = form.cleaned_data.get("message")

        client = MessageClient()
        client.send_message(message, to)
        # send('test')
        return HttpResponseRedirect(self.request.path)


# def TestView(request):

#     a = LivePriceUpdate()
#     b = a.send_price_alert()

#     return JsonResponse(b, safe=False)

# if request.method == "GET":
#     try:
#         tickers = ["IDEX", "BB", "CLNE", "AMC", "CCL", "JMIA", "TRCH"]
#         live_update = LivePriceUpdate(symbols=tickers, yahoo_init=tickers)
#         data = live_update.get_quotes_from_yahoo()
#         print(data)
#         return HttpResponse(content=data)

#     except:
#         return HttpResponseBadRequest(content="Error")


def AutoCompleteSearch(request):

    if request.method == "GET":
        query = request.GET.get("query", "")
        include_name_in_search = request.GET.get("include_name_in_search", False)

        autocomplete = TickerAutocomplete(query=query)
        autocomplete.autocomplete_search(
            query, include_name_in_search=include_name_in_search
        )

        context = {"status": 200, "results": autocomplete.autocomplete_results}

        return JsonResponse(context)


def StockSummary(request):
    if request.method == "GET":
        symbol = request.GET.get("symbol")
        force_update = request.GET.get("live")

        print(symbol)
        # def get_fresh_data():
        live_update = LivePriceUpdate(symbol=symbol, yahoo_init=symbol)
        stock_data = live_update.yahoo_get_summary()
        current_price = live_update.get_quote_from_yahoo()

        return JsonResponse(
            {
                "status": 200,
                **stock_data[symbol],
                "currentPrice": current_price,
            }
        )

        # if force_update:
        #   get_fresh_data()
        # else:
        #   # Check if data is recent
        #   ticker = Ticker.objects.filter(symbol=symbol)[0]
        #   serializer = TickerSerializer(ticker, many=False, context={'request': request})

        #   if ticker.is_recent():
        #     return JsonResponse({
        #       "status": 200,
        #       "ticker": serializer.data
        #     })
        #   else:
        #     get_fresh_data()


def WatchStock(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        django_user = None
        user = json_data["user"]
        symbol = json_data["symbol"]
        price = json_data["price"]
        min = json_data["min_price"]
        max = json_data["max_price"]

        current_ticker = {}

        try:
            django_user = User.objects.filter(email__exact=user)[0]
        except:

            return JsonResponse(
                {
                    "status": 500,
                    "error": "No user found",
                    "message": "No User found. Please sign In.",
                }
            )

        try:
            ticker = get_object_or_404(Ticker, symbol=symbol)
            ticker.price = price
            ticker.save()
            current_ticker = ticker
        except:
            print("No Ticker found, creating new Ticker")

            try:
                ticker = Ticker(symbol=symbol, price=price)
                ticker.save()
                current_ticker = ticker
            except:
                print("Problem creating new ticker")
                return JsonResponse(
                    {
                        "status": 500,
                        "error": "Problem creating new ticker, please try again",
                    }
                )

        try:
            # GET/CREATE TickerWatcher
            print(django_user, ticker, min, max)
            new_ticker_watcher = TickerWatcher(
                user=django_user, ticker=current_ticker, min_price=min, max_price=max
            )

            new_ticker_watcher.save()

            print("new watcher created")
            context = {
                "status": 200,
                "symbol": symbol,
                "price": price,
                "ticker": json.loads(
                    serializers.serialize(
                        "json",
                        [
                            new_ticker_watcher,
                        ],
                    )
                )[0],
            }

            return JsonResponse(context)
        except:
            print("new watcher failed")
            context = {
                "status": 500,
                "symbol": symbol,
                "price": price,
                "error": "New watcher failed to save",
            }

            return JsonResponse(context)


def Watchers(request):
    if request.method == "GET":
        email = request.GET.get("email")

        if email:
            watchers = TickerWatcher.objects.filter(watcher__email=email)

            json_watchers = json.loads(serializers.serialize("json", watchers))

            # for watcher in json_watchers:
            #   watcher_list.append(watcher.to_dict())

            return JsonResponse({"status": 200, "watchers": json_watchers}, safe=False)


def db_status(request):
    return JsonResponse({"status": "active", "timestamp": datetime.now()})
