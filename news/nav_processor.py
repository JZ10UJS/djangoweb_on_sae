from news.models import Category

nav_display_columns = Category.objects.filter(nav_display=True)

def nav_column(request):
    return {'nav_display_columns': nav_display_columns}