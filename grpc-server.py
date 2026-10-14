import grpc
from concurrent import futures

import lab6_pb2
import lab6_pb2_grpc
import io
from PIL import Image
import base64

class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):

    def dotProduct(self, request, context):
        result = sum(
            a * b for a, b in zip(request.a, request.b)
        )

        return lab6_pb2.dotProductReply(
            dotproduct=result
        )

    def add(self, request, context):
        result = request.a + request.b

        return lab6_pb2.addReply(
            sum=result
        )
    
    def rawImage(self, request, context):
        image_bytes = request.img

        img = Image.open(io.BytesIO(image_bytes))

        return lab6_pb2.imageReply(
            width=img.width,
            height=img.height
        )
        
    def jsonImage(self, request, context):
        # Decode the Base64 string into image bytes
        image_bytes = base64.b64decode(request.img)

        # Read the image
        img = Image.open(io.BytesIO(image_bytes))

        # Return dimensions
        return lab6_pb2.imageReply(
            width=img.width,
            height=img.height
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Service(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
