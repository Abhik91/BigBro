import boto3
import json

def lambda_handler(event, context):
    
    dt = event['Records'][0]['s3']['object']['key']
    client = boto3.client("rekognition", "us-west-2")
    client2 = boto3.client('sns')
    
    test_img=str(dt).strip()
    
    
    
    response2=client.compare_faces(SimilarityThreshold=90,
                                  SourceImage={'S3Object':{'Bucket':"hackarizonaasu",'Name':"1.jpg"}},
                                  TargetImage={'S3Object':{'Bucket':"hackarizonaasu",'Name':test_img}})
    s3 = boto3.resource('s3')
             
    response=client.compare_faces(SimilarityThreshold=90,
                                  SourceImage={'S3Object':{'Bucket':"hackarizonaasu",'Name':"Es1.jpg"}},
                                  TargetImage={'S3Object':{'Bucket':"hackarizonaasu",'Name':test_img}})

    if response['FaceMatches'] == [] and response2['FaceMatches'] == [] :
        print ('The two images are different')
        tosend='http://hackarizonaasu.s3-website-us-west-2.amazonaws.com/'
        message=client2.publish(TargetArn='arn:aws:sns:us-west-2:451410343613:Face-Recognition-SNS',Message=tosend,Subject="Uploaded Image Label")
        file_name = "intruder.jpg"
        s3.Object('hackarizonaasu',file_name).copy_from(CopySource='hackarizonaasu/'+test_img)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
