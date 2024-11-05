# Options Trading Data Django Application

This Django application provides API endpoints to retrieve options trading data for Indian financial markets. It integrates with Alpha Vantage's API to fetch option chain data and calculate trading metrics.

## Features
- Retrieve option chain data for specified instruments and expiry dates.
- Calculate margin requirements and premium earned for options contracts.

## Requirements
- Python 3.8+
- Django 5.1.2
- Alpha Vantage API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kimforee/options-trading.git
   cd options-trading
   ```

2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Update the Alpha Vantage API key in `trading/utils.py`:
   ```python
   api_key = "YOUR_API_KEY"
   ```

5. Start the Django server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### 1. Retrieve Option Chain Data
**Endpoint:** `/options/chain/<instrument_name>/<side>/`

**Method:** GET

**Parameters:**
- `instrument_name` (str): Name of the instrument (e.g., 'NIFTY').
- `side` (str): Type of option ('PE' for Put, 'CE' for Call).

**Sample Request:**
```bash
curl -X GET "http://127.0.0.1:8000/options/chain/NIFTY/CE/"
```

**Sample Response:**
```json
{
    "status": "success",
    "data": [
        {"instrument_name": "NIFTY", "strike_price": 19500, "side": "PE", "bid/ask": 0.65},
        {"instrument_name": "NIFTY", "strike_price": 19500, "side": "CE", "bid/ask": 2302.25}
    ]
}
```

### 2. Calculate Margin and Premium
**Endpoint:** `/options/margin/<instrument_name>/<side>/`

**Method:** GET

**Parameters:**
- `instrument_name` (str): Name of the instrument (e.g., 'NIFTY').
- `side` (str): Type of option ('PE' for Put, 'CE' for Call).

**Sample Request:**
```bash
curl -X GET "http://127.0.0.1:8000/options/margin/NIFTY/CE/"
```

**Sample Response:**
```json
{
    "status": "success",
    "data": [
        {"instrument_name": "NIFTY", "strike_price": 19500, "side": "PE", "bid/ask": 0.65, "margin_required": 1950, "premium_earned": 780},
        {"instrument_name": "NIFTY", "strike_price": 19500, "side": "CE", "bid/ask": 2302.25, "margin_required": 3904, "premium_earned": 92090}
    ]
}
```

## Error Handling

The API includes error handling for:
- Invalid or missing data in the API response.
- Invalid parameters or missing required fields.
- API connectivity issues.

## Contributing
Please ensure any additions adhere to PEP-8 guidelines and include necessary docstrings. Test all functionality thoroughly before submission.

## License
This project is licensed under the MIT License.
```