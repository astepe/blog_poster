import os, json, requests, boto3
from requests.auth import HTTPBasicAuth

#API_URL = 'https://ari-blog.herokuapp.com/api'
#API_URL = 'http://127.0.0.1:5000/api'
API_URL = 'http://0.0.0.0:5000/api'

class Api:
    """
    controls outgoing and incoming api requests
    """

    def __init__(self, username, password):

        response = requests.post(API_URL + '/tokens',
                     auth=HTTPBasicAuth(username, password)).json()

        if 'error' in response:
            self.token = None
        else:
            self.token = {'Authorization': 'Bearer ' + response['token']}

    def __repr__(self):

        return(str(self.token))

    def create_blogpost(self, title, body, **kwargs):

        resource = API_URL + '/blogposts/create'
        payload = {'title': title, 'body': body}

        if 'image' in kwargs and os.path.exists(kwargs['image']):

            image_url = self.sign_and_post_s3(kwargs['image'])

            if image_url != None:
                payload.update({'image': image_url})

        response = requests.post(resource, headers=self.token, json=payload)
        return response

    def get_blogpost(self, id):

        resource = API_URL + f'/blogposts/{id}'
        response = requests.get(resource, headers=self.token)

        return response.json()

    def get_blogposts(self):

        resource = API_URL + '/blogposts'
        response = requests.get(resource, headers=self.token)
        return response.json()

    def update_blogpost(self, id, **kwargs):

        resource = API_URL + f'/blogposts/{id}/update'
        payload = {'title': kwargs['title'], 'body': kwargs['body']}

        if 'image' in kwargs and os.path.exists(kwargs['image']):

            image_url = self.sign_and_post_s3(kwargs['image'])
            if image_url != None:
                payload.update({'image': image_url})

        if payload != {}:

            response = requests.put(resource, headers=self.token, json=payload)
            return response.json()

    def delete_blogpost(self, id):

        resource = API_URL + f'/blogposts/{id}/delete'
        response = requests.delete(resource, headers=self.token)

        return response.json()

    def sign_and_post_s3(self, file_path):

        file_name = file_path.split('/')[-1]

        resource = API_URL + f'/sign_s3/{file_name}'
        response = requests.get(resource, headers=self.token)

        if response.status_code == requests.codes.ok:

            data = response.json()['data']['fields']
            s3_resource = boto3.resource('s3')

            s3_resource.Bucket('ari-blog-assets').upload_file(
                Filename=file_path, Key=data['key'],
                ExtraArgs={'ContentType': data['Content-Type'],
                           'ACL': data['acl']})

            return response.json()['url']

        return None
