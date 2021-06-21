from prometheus_client import Counter


# Metric for recording total requests API has received so far.
api_requests_total = Counter("api_requests", "Total API Requests")
