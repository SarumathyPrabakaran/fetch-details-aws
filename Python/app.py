import boto3
import json

def fetch_aws_profile_details(profile_name):
    
    session = boto3.Session(profile_name=profile_name)
    credentials = session.get_credentials()

    if credentials is None:
        return None
    else:
        details = {
            "ProfileName": profile_name,
            "AccessKey": credentials.access_key,
            "SecretKey": credentials.secret_key,
            "SessionToken": credentials.token
        }
        return details

def iam_details_fetch(profile_name):

    session = boto3.Session(profile_name=profile_name)
    iam_client = session.client("iam")

    user_info = iam_client.get_user()

    user_name = user_info["User"]["UserName"]
    user_arn = user_info["User"]["Arn"]
    create_date = user_info["User"]["CreateDate"]

    details = {
        "UserName": user_name,
        "UserArn": user_arn,
        "CreateDate": str(create_date)
    }
    return details

def iam_list_users():
    client = boto3.client('iam')
    resp = client.list_users()

    users = []
    for user in resp["Users"]:
        user_info = {
            "Arn": user["Arn"],
            "UserName": user["UserName"],
            "UserId": user["UserId"],
            "PasswordLastUsed": str(user.get("PasswordLastUsed", "N/A"))
        }
        users.append(user_info)
    return users



if __name__ == "__main__":


    profile_name = "default"  

    aws_profile_details = fetch_aws_profile_details(profile_name)
    iam_user_details = iam_details_fetch(profile_name)
    iam_users_list = iam_list_users()

    all_details = {
        "AWSProfileDetails": aws_profile_details,
        "IAMUserDetails": iam_user_details,
        "IAMUsersList": iam_users_list
    }

    with open("aws_details.json", "w") as json_file:
        json.dump(all_details, json_file, indent=4)

    print("Details written to aws_details.json")
