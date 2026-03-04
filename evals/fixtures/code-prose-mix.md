# Notifications API

The notifications API allows you to send notifications to users through multiple channels including email, SMS, and push notifications. It was designed to be simple to integrate and provides a unified interface regardless of which delivery channel you choose. The API handles rate limiting, retry logic, and delivery status tracking automatically so you don't have to implement these yourself.

## Sending a notification

To send a notification you need to create a client instance and call the send method with the appropriate parameters. The client handles authentication and connection pooling internally. You should reuse the client instance across your application rather than creating a new one for each request, as this improves performance significantly due to connection reuse and reduces the overhead of repeated TLS handshakes.

```python
from notifications import NotificationClient

client = NotificationClient(api_key="your-api-key")

response = client.send(
    channel="email",
    recipient="user@example.com",
    subject="Order confirmed",
    body="Your order #1234 has been confirmed.",
    priority="normal"
)

print(f"Notification sent: {response.notification_id}")
```

## Channel configuration

Each delivery channel has its own configuration requirements and the configuration is done through the `config.yaml` file in your project. The following table shows the required fields for each channel and the default values that are used when a field is not explicitly set.

| Channel | Required Fields | Default Priority | Rate Limit |
|---------|----------------|-----------------|------------|
| email | recipient, subject, body | normal | 100/min |
| sms | phone_number, body | high | 50/min |
| push | device_token, title, body | normal | 200/min |

## Batch sending

When you need to send notifications to multiple recipients at once, you should use the batch API instead of sending individual requests in a loop. The batch API accepts up to 1000 recipients per request and processes them asynchronously. It returns a batch ID that you can use to check the delivery status of all notifications in the batch. The batch processing is optimized for throughput and will automatically handle rate limiting across all recipients.

```python
batch = client.send_batch(
    channel="email",
    recipients=["user1@example.com", "user2@example.com"],
    subject="System maintenance",
    body="Scheduled maintenance on Saturday.",
    priority="high"
)

print(f"Batch ID: {batch.batch_id}, Status: {batch.status}")
```

## Checking delivery status

You can check the delivery status of any notification using its notification ID or batch ID. The status endpoint returns detailed information about the delivery attempt including timestamps, channel-specific metadata, and any error messages if the delivery failed. For batch notifications, you can retrieve either the overall batch status or drill down into individual notification statuses within the batch.

```bash
curl -H "Authorization: Bearer your-api-key" \
  https://api.notifications.example.com/v1/status/notif_abc123
```

## Error handling

The client library raises specific exception types for different error conditions. NetworkError is raised when the API is unreachable, RateLimitError when you exceed the rate limit for a channel, and ValidationError when the request parameters are invalid. All errors include a machine-readable error code and a human-readable message that you can use for logging and debugging purposes.
