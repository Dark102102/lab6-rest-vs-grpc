# Lab 6 — REST vs. gRPC Performance Comparison

All measurements are in **milliseconds per operation**. Benchmarks used 1,000 iterations for `add` and `dotproduct`, and 100 iterations for `rawimg` and `jsonimg`. PING values represent the average round-trip time over 10 packets.

| Method | Local | Same-Zone | Different Region |
|---|---:|---:|---:|
| REST add | 2.538 | 3.603 | 323.370 |
| gRPC add | 0.791 | 1.284 | 143.384 |
| REST rawimg | 6.178 | 10.057 | 1468.379 |
| gRPC rawimg | 12.768 | 16.461 | 206.284 |
| REST dotproduct | 3.134 | 4.231 | 338.253 |
| gRPC dotproduct | 0.874 | 1.571 | 162.069 |
| REST jsonimg | 28.728 | 31.951 | 1498.813 |
| gRPC jsonimg | 28.633 | 34.811 | 209.675 |
| PING | 0.057 | 0.493 | 159.482 |

## Observations

The results show that gRPC generally performed better than REST for smaller operations such as addition and dot product. On localhost, gRPC was approximately 3.21 times faster for addition and 3.59 times faster for dot product. However, REST performed better for raw image transfers on localhost and within the same zone. In the cross-region experiment, gRPC outperformed REST across all four operations, achieving approximately 7.12 times lower operation time for raw image transfers. Network latency played a significant role in the results: average PING round-trip time increased from 0.057 ms locally to 0.493 ms within the same zone and 159.482 ms between Oregon and Frankfurt. In our implementation, the REST client creates a new HTTP/TCP connection for requests, while the gRPC client reuses a single HTTP/2 connection for multiple requests. Repeated connection establishment may therefore contribute substantially to REST's higher cross-region latency, especially for large payloads. Other factors, including message serialization, image processing, and data transfer overhead, may also affect performance. Since each benchmark configuration was measured once, additional trials would be needed to confirm the consistency of these differences.