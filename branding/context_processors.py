def company_settings(request):
    """
    Disponibiliza as configurações da empresa em todos os templates
    """
    return {
        'company': {
            'company_name': 'Aurora Fit',
            'primary_color': '#FFB366',
            'secondary_color': '#9B59B6',
            'accent_color': '#FFF4B7',
        }
    }