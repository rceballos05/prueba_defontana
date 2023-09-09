import json
import boto3
from decimal import Decimal
# import requests


def lambda_handler(event, context):
    method = event["httpMethod"]
    path = event["path"]
    table_user = boto3.resource('dynamodb').Table('User')
    id = ""
    
    id = path.split("/")[-1]
    if path == "/users/new":
        if method == "POST":
            try:
                datos = json.loads(event["body"])
                response = table_user.put_item(
                    Item = {
                        'userId':datos["userId"],
                        'name': datos["name"],
                        'lastname': datos["lastname"],
                        'email': datos["email"]
                    }
                )
                if response:
                    return {
                        "statusCode": 201,
                        "body": json.dumps({
                            "message": "Se guardó con éxito",
                        })
                    }
                else:
                    return {
                        "statusCode": 500,
                        "body": json.dumps({
                            "message":"Error de conexión",
                        })
                    }
            except Exception as e:
                return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "message": f"Error: {e}",
                    })
                }
    elif path == "/users":
        if method == "GET":
            try:
                items = table_user.scan()
                if items['Items']:
                    item = []
                    for i in items['Items']:
                        item.append(i)
                    return {
                        
                        "statusCode":200,
                        "body": json.dumps({
                            "message":"Consulta exitosa",
                            "Items": item,
                        })
                    }
                else:
                    return {
                        "statusCode": 500,
                        "body": json.dumps({
                            "message":"No hay registros" ,
                        })
                    }
            except Exception as e:
                return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "message":f"error: {e}",
                    })
                }
    else:
        if method == "GET":
            try:
                result = table_user.get_item(
                    Key={
                        'userId':id,
                        })
                if result:
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message":"Consulta exitosa",
                            "Items": result['Item'],
                        })
                    }
                else:
                    return {
                        "statusCode": 500,
                        "body": json.dumps({
                            "message":"No encontrado",
                        })
                    }
            except Exception as e:
                 return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "message":f"error: {e}",
                    })
                }
        elif method == "PUT":
            try:
                datos = json.loads(event["body"])
                result = table_user.update_item(
                    Key = {
                        'userId': id,
                        },
                    UpdateExpression="set #attr_name = :name, lastname = :last, email = :email",
                    ExpressionAttributeNames={"#attr_name":"name"},
                    ExpressionAttributeValues={":name" : datos["name"], ":last":datos["lastname"], ":email": datos["email"]}
                )
                if result:
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message":"Actualizado con éxito",
                        })
                    }
                else:
                    return {
                        "statusCode": 500,
                        "body": json.dumps({
                            "message":"Error de conexión",
                        })
                    }
            except Exception as e:
                 return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "message":f"Error: {e}",
                    })
                }
        elif method == "DELETE":
            try:
                result = table_user.delete_item(Key = {'userId':id})
                if result:
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message":"Eliminado con éxito",
                        })
                    }
                else:
                    return {
                        "statusCode": 500,
                        "body": json.dumps({
                            "message":"Usuario no encontrado",
                        })
                    }
            except Exception as e:
                 return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "message":f"Error: {e}",
                    })
                }

    
