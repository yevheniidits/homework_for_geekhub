from django.shortcuts import render, redirect
from django.urls import reverse

from olx_scraper_app.models import ScrapedOlxAd
from olx_scraper_app.scripts import start_olx_scraper


def main_page(request):
    if request.POST:
        category = request.POST.get('ad-category')
        ad_number = int(request.POST.get('ad-number'))
        start_olx_scraper.limiter_of_ads_number(ad_number, category)
        return redirect(reverse('scraped_data'))
    return render(request, 'main_page.html')


def scraped_data(request):
    if request.POST:
        action = request.POST.get('action')
        ScrapedOlxAd.objects.filter(id=action).delete()
    context = {'data': ScrapedOlxAd.objects.all()}
    return render(request, 'scraped_page.html', context=context)
