from .models import Site_Settings



def website_settings(request):
    website_setting = Site_Settings.objects.all().first()
    return {'website_setting': website_setting}