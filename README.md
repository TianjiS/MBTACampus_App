# MBTA Campus App

A real-time MBTA tracking and trip planning application for campus buildings.

## Features

- Real-time MBTA train tracking
- Building search with autocomplete
- Trip planning with rush hour considerations
- MBTA alerts and service updates
- Alternative station suggestions during peak hours

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with:
```
MBTA_API_KEY=your_api_key_here
```

3. Initialize the database:
```bash
python -m src.init_db
```

4. Run the application:
```bash
uvicorn src.main:app --reload
```

## API Endpoints

- `GET /api/v1/buildings/search?query={query}` - Search for buildings
- `GET /api/v1/trip/calculate?building_id={id}&target_time={time}&direction={direction}` - Calculate trip details
- `GET /api/v1/stations` - Get all stations
- `GET /api/v1/alerts` - Get MBTA alerts
- `GET /api/v1/predictions/{station_id}` - Get real-time predictions for a station

## Database Schema

### Buildings
- building_id (PK)
- building_name
- campus
- closest_station
- time_to_station

### Stations
- station_id (PK)
- station_name
- direction

### Rush Hours
- id (PK)
- day_of_week
- start_time
- end_time
- station_name
- congestion_level

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT 