# Property Insights
The goal of this project is to provide property insights based on data crawled from [Zameen.com](https://www.zameen.com).

## Nature of Data
The data crawled from Zameen is split into two categories:
- Rentals
- Properties

## Components
This project is based on the following major components:
- Zameen crawler
- Airflow pipeline for generating notebook outputs for data visualization
- Amazon Redshift for data warehousing
- Amazon Quicksight for visualizing the data
- Prometheus for monitoring services
- Grafana for analyzing the data on prometheus

### Zameen Crawler
The crawler runs everyday. Following jobs are processed:
- Crawling areas for rentals
- Crawling rentals for an area as a batch
- Crawling a single rental
- Crawling areas for properties
- Crawling properties for an area as a batch
- Crawling a single property

Each crawl job populates the database with crawled data.


### Airflow Pipeline
The pipeline runs everyday to execute the notebooks to generate visualizations for the rentals and properties.

### Amazon Redshift
Redshift queries the property database and populates summary tables.
*TODO*

### Amazon Quicksight
This is the main visualization tool for getting real-time insights about the data.

### Prometheus Server
This is the main tool for monitoring our services. All services related data will logged/recorded using prometheus.

### Grafana
Prometheus metrics are visualized in Grafana.
