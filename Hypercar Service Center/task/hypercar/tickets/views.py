from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

ticket_type = [
    'Change oil',
    'Inflate tires',
    'Get diagnostic'
]
ticket_url_path = [
    'change_oil',
    'inflate_tires',
    'diagnostic'
]
ticket_pathing = dict(zip(ticket_type, ticket_url_path))

service_line = {value:[] for value in ticket_url_path}

queue_lengths = {}
ticket_number = 0
wait_time = 0
now_serving = None

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'options': ticket_pathing})


class TicketView(View):
    def get(self, request, service, *args, **kwargs):
        if service == "change_oil":
            global wait_time
            wait_time = len(service_line["change_oil"]) * 2
        elif service == "inflate_tires":
            wait_time = len(service_line["change_oil"]) * 2 + len(service_line["inflate_tires"]) * 5
        elif service == "diagnostic":
            wait_time = len(service_line["change_oil"]) * 2 + len(service_line["inflate_tires"]) * 5 + len(service_line["diagnostic"] * 30)
        global ticket_number
        ticket_number += 1
        service_line[service].append(ticket_number)
        return render(request, 'tickets/service.html', context={"ticket": ticket_number, "wait": wait_time})


class ProcessView(View):
    def get(self, request, *args, **kwargs):
        global ticket_pathing
        global queue_lengths
        for ticket, url in ticket_pathing.items():
            queue_lengths[ticket] = len(service_line[url])
        return render(request, 'tickets/process.html', context={"queues": queue_lengths})

    def post(self, request, *args, **kwargs):
        global service_line, now_serving
        if len(service_line["change_oil"]) > 0:
            now_serving = service_line["change_oil"].pop(0)
        elif len(service_line["inflate_tires"]) > 0:
            now_serving = service_line["inflate_tires"].pop(0)
        elif len(service_line["diagnostic"]) > 0:
            now_serving = service_line["diagnostic"].pop(0)
        else:
            now_serving = None
        return redirect('/processing')

class CustomerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/customerview.html', context={"ticket_number": now_serving})