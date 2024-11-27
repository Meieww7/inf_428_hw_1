
FROM docker.elastic.co/elasticsearch/elasticsearch:8.10.0

ENV discovery.type=single-node
ENV xpack.security.enabled=false


CMD ["elasticsearch"]
