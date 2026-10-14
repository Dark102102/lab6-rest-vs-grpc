import argparse
import random
import time

import grpc
import lab6_pb2
import lab6_pb2_grpc
import base64


def doDotProduct(stub, debug=False):
    # Generate two random vectors of length 100
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    request = lab6_pb2.dotProductMsg(a=a, b=b)
    response = stub.dotProduct(request)

    if debug:
        print("Dot product:", response.dotproduct)

def doAdd(stub, debug=False):
    request = lab6_pb2.addMsg(a=5, b=10)

    response = stub.add(request)

    if debug:
        print("Sum:", response.sum)

def doRawImage(stub, debug=False):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        image_bytes = f.read()

    request = lab6_pb2.rawImageMsg(img=image_bytes)

    response = stub.rawImage(request)

    if debug:
        print("Width:", response.width)
        print("Height:", response.height)

def doJsonImage(stub, debug=False):
    # Read the image
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        image_bytes = f.read()

    # Encode the image as a Base64 string
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    # Create the gRPC request
    request = lab6_pb2.jsonImageMsg(img=encoded_image)

    # Send the request to the server
    response = stub.jsonImage(request)

    if debug:
        print("Width:", response.width)
        print("Height:", response.height)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("cmd", choices=["add", "dotProduct", "rawImage", "jsonImage"])
    parser.add_argument("reps", type=int)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    # Connect to the gRPC server
    with grpc.insecure_channel(f"{args.host}:50051") as channel:
        stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

        start = time.perf_counter()

        for _ in range(args.reps):
            if args.cmd == "add":
                doAdd(stub, args.debug)
            elif args.cmd == "dotProduct":
                doDotProduct(stub, args.debug)
            elif args.cmd == "rawImage":
                doRawImage(stub, args.debug)
            elif args.cmd == "jsonImage":
                doJsonImage(stub, args.debug)

        end = time.perf_counter()

    elapsed_ms = (end - start) * 1000 / args.reps

    print(f"Took {elapsed_ms:.3f} ms per operation")


if __name__ == "__main__":
    main()
