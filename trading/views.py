from django.http import JsonResponse
from .utils import get_option_chain_data, calculate_margin_and_premium
from django.shortcuts import render

def home(request):
    return render(request, 'trading/home.html')

def option_chain_view(request, instrument_name, side):
    """
    Django view to retrieve option chain data and render it in a table format.

    Parameters:
    request (HttpRequest): The HTTP request object.
    instrument_name (str): Name of the instrument (e.g., 'NIFTY').
    side (str): Type of option ('PE' for Put, 'CE' for Call).

    Returns:
    HttpResponse: Rendered HTML response containing option chain data in a table.
    """
    try:
        data = get_option_chain_data(instrument_name=instrument_name, side=side)
        return render(request, 'trading/option_chain.html', {'data': data.to_html(index=False)})
    except (RuntimeError, ValueError) as e:
        return render(request, 'trading/option_chain.html', {'error': str(e)})
    except Exception as e:
        return render(request, 'trading/option_chain.html', {'error': "An unexpected error occurred."})

def calculate_margin_and_premium_view(request, instrument_name, side):
    """
    Django view to retrieve margin and premium calculations and render it in a table format.

    Parameters:
    request (HttpRequest): The HTTP request object.
    instrument_name (str): Name of the instrument (e.g., 'NIFTY').
    side (str): Type of option ('PE' for Put, 'CE' for Call).

    Returns:
    HttpResponse: Rendered HTML response containing margin and premium data in a table.
    """
    try:
        # Retrieve option chain data
        data = get_option_chain_data(instrument_name=instrument_name, side=side)
        
        # Calculate margin and premium
        enriched_data = calculate_margin_and_premium(data)
        
        # Render the enriched data into the calculate.html template
        return render(request, 'trading/calculate.html', {'data': enriched_data.to_html(index=False)})
    except (RuntimeError, ValueError) as e:
        return render(request, 'trading/calculate.html', {'error': str(e)})
    except Exception as e:
        return render(request, 'trading/calculate.html', {'error': "An unexpected error occurred."})
