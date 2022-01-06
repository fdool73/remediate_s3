import remediate_s3

def main():
    event = {
        "Region": "us-east-1",
        "Enable": True
    }
    context = {}
    remediate_s3.lambda_handler(event, context)

if __name__ == '__main__':
    main()