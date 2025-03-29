from kafka import KafkaConsumer
from prometheus_client import Counter, Histogram, start_http_server

# Actualiza el tema de Kafka al correspondiente de tu equipo
topic = 'movielogN'

# Inicia el servidor HTTP para exponer las métricas en el puerto 8765
start_http_server(8765)

# Definición de métricas
# Métrica para contar el número total de solicitudes por código de estado HTTP
REQUEST_COUNT = Counter(
    'request_count_total', 'Recommendation Request Count',
    ['http_status']
)

# Métrica para medir la latencia de las solicitudes
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')


def main():
    # Configuración del consumidor de Kafka
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id=topic,
        enable_auto_commit=True,
        auto_commit_interval_ms=1000
    )

    for message in consumer:
        # Decodifica el mensaje recibido
        event = message.value.decode('utf-8')
        values = event.split(',')

        if 'recommendation request' in values[2]:
            # Extrae el código de estado HTTP del mensaje
            status = values[3].strip()  # Suponiendo que el código de estado está en la posición 3

            # Incrementa el contador de solicitudes para el código de estado correspondiente
            REQUEST_COUNT.labels(http_status=status).inc()

            # Actualiza el histograma de latencia
            time_taken = float(values[-1].strip().split(" ")[0])  # Suponiendo que el tiempo está al final
            REQUEST_LATENCY.observe(time_taken / 1000)  # Convierte milisegundos a segundos


if __name__ == "__main__":
    main()
